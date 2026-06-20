import hashlib
import aiohttp
from typing import Dict, Any

class GravatarClient:
    """Client for fetching Gravatar profile details using an email address."""
    
    def __init__(self):
        self.headers = {"User-Agent": "IRIS-OSINT"}

    async def get_profile(self, email: str) -> Dict[str, Any]:
        """Fetch the public Gravatar profile for a given email address."""
        email_hash = hashlib.md5(email.strip().lower().encode()).hexdigest()
        url = f"https://en.gravatar.com/{email_hash}.json"
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=self.headers, timeout=5) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        entry = data.get("entry", [])
                        if entry:
                            profile = entry[0]
                            return {
                                "name": profile.get("name", {}).get("formatted", profile.get("displayName")),
                                "username": profile.get("preferredUsername"),
                                "profile_url": profile.get("profileUrl"),
                                "photos": [p.get("value") for p in profile.get("photos", [])],
                                "accounts": [a.get("domain") for a in profile.get("accounts", [])]
                            }
                    return {}
        except Exception:
            return {}
