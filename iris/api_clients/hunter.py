import aiohttp
from typing import Dict, Any, Optional
from iris import config

class HunterClient:
    """Client for fetching professional email OSINT from Hunter.io."""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or config.get_api_key("HUNTER_API_KEY")

    async def verify_email(self, email: str) -> Dict[str, Any]:
        """Fetch email verification and associated identity details."""
        if not self.api_key:
            return {"error": "HUNTER_API_KEY not configured."}
            
        url = f"https://api.hunter.io/v2/email-verifier?email={email}&api_key={self.api_key}"
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=5) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        d = data.get("data", {})
                        # Hunter returns some identity info if found
                        return {
                            "status": d.get("status"),
                            "score": d.get("score"),
                            "sources": len(d.get("sources", [])),
                            "first_name": d.get("first_name"),
                            "last_name": d.get("last_name"),
                            "linkedin": d.get("linkedin"),
                            "twitter": d.get("twitter"),
                            "company": d.get("company")
                        }
                    elif resp.status == 401:
                        return {"error": "Invalid Hunter.io API key"}
                    else:
                        return {"error": f"Hunter API returned {resp.status}"}
        except Exception as e:
            return {"error": str(e)}
