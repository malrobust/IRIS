import asyncio
import dns.resolver
from typing import Dict, Any

from iris.collectors import BaseCollector
from iris.api_clients.hibp import HIBPClient
from iris.api_clients.github import GitHubClient
from iris.api_clients.gravatar import GravatarClient
from iris.db import cache

class EmailCollector(BaseCollector):
    """Collector for email-related intelligence."""
    
    def __init__(self):
        super().__init__()
        self.hibp_client = HIBPClient()
        self.github_client = GitHubClient()
        self.gravatar_client = GravatarClient()

    async def check_smtp(self, domain: str) -> bool:
        """Perform a basic check to see if the domain has MX records."""
        try:
            resolver = dns.resolver.Resolver()
            resolver.timeout = 2.0
            resolver.lifetime = 2.0
            loop = asyncio.get_running_loop()
            answers = await loop.run_in_executor(None, resolver.resolve, domain, "MX")
            return len(answers) > 0
        except Exception:
            return False

    async def collect(self, target: str) -> Dict[str, Any]:
        """Gather intelligence on an email target."""
        email = target.strip().lower()
        
        # Check cache first
        cached_data = cache.get_cached_email(email)
        if cached_data:
            return self.parse(cached_data)

        domain_part = email.split("@")[1] if "@" in email else ""
        
        # Collect data concurrently
        results = await asyncio.gather(
            self.hibp_client.check_email_breached(email),
            self.hibp_client.get_breaches(email),
            self.check_smtp(domain_part),
            self.gravatar_client.get_profile(email),
            self.github_client.search_users_by_email(email),
            return_exceptions=True
        )
        
        is_breached = results[0] if not isinstance(results[0], Exception) else False
        breaches = results[1] if not isinstance(results[1], Exception) else []
        has_smtp = results[2] if not isinstance(results[2], Exception) else False
        gravatar_profile = results[3] if not isinstance(results[3], Exception) else {}
        github_users = results[4] if not isinstance(results[4], Exception) else []
        
        sources = [b.get("Name", "Unknown") for b in breaches]
        
        profile_data = {
            "gravatar": gravatar_profile,
            "github": github_users
        }
        
        cache.save_email(
            email_address=email,
            breached=is_breached,
            sources=sources,
            profile_data=profile_data
        )

        raw_data = {
            "email": email,
            "breached": is_breached,
            "breach_details": breaches,
            "has_smtp": has_smtp,
            "sources": sources,
            "profile_data": profile_data
        }
        
        return self.parse(raw_data)

    def parse(self, raw: Dict[str, Any]) -> Dict[str, Any]:
        """Normalize raw data into a structured report format."""
        parsed = {
            "Email": raw.get("email"),
            "Valid SMTP": "✓ YES" if raw.get("has_smtp") else "✗ NO",
            "Breached": "⚠️ YES" if raw.get("breached") else "✅ NO",
            "Breach Sources": ", ".join(raw.get("sources", [])) if raw.get("sources") else "None found"
        }
        
        profile_data = raw.get("profile_data", {})
        
        gravatar = profile_data.get("gravatar", {})
        if gravatar:
            parsed["Display Name"] = gravatar.get("name") or gravatar.get("username", "Unknown")
            if gravatar.get("accounts"):
                parsed["Associated Accounts"] = ", ".join(gravatar.get("accounts"))
                
        github = profile_data.get("github", [])
        if github:
            parsed["GitHub Users"] = ", ".join([f"{u.get('login')} ({u.get('type')})" for u in github])
            
        parsed["_raw"] = raw
        return parsed
