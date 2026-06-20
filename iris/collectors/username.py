import asyncio
from typing import Dict, Any

from iris.collectors import BaseCollector
from iris.api_clients.sherlock_client import SherlockClient

class UsernameCollector(BaseCollector):
    """Collector for finding username presence across platforms."""

    def __init__(self):
        super().__init__()
        self.sherlock_client = SherlockClient()

    async def collect(self, target: str) -> Dict[str, Any]:
        """Gather intelligence on a username target using Sherlock."""
        username = target.strip()

        # Run sherlock
        results = await self.sherlock_client.search_username(username)

        raw_data = {
            "target": username,
            "accounts": results
        }

        return self.parse(raw_data)

    def parse(self, raw: Dict[str, Any]) -> Dict[str, Any]:
        """Normalize raw data into a structured report format."""
        parsed = {
            "Username": raw.get("target"),
            "Accounts Found": str(len(raw.get("accounts", [])))
        }
        
        accounts = raw.get("accounts", [])
        if accounts:
            # We can format the accounts nicely, e.g., comma separated or join with newlines
            # In Typer/Rich tables, a comma separated string or newlines work
            parsed["Profiles"] = "\n".join(accounts)

        parsed["_raw"] = raw
        return parsed
