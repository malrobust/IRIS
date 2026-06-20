import asyncio
from typing import List

class HoleheClient:
    """Client for running holehe to find registered accounts across 120+ sites."""
    
    async def get_registered_accounts(self, email: str) -> List[str]:
        """Runs the holehe CLI tool as a subprocess and parses the output."""
        try:
            # We run the command with --only-used and --no-color to make parsing easy
            process = await asyncio.create_subprocess_exec(
                "holehe", email, "--only-used", "--no-color",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await process.communicate()
            
            if process.returncode != 0:
                return []
                
            output = stdout.decode("utf-8", errors="ignore").splitlines()
            accounts = []
            
            for line in output:
                line = line.strip()
                if line.startswith("[+]"):
                    site = line.replace("[+]", "").strip()
                    accounts.append(site)
                    
            return accounts
        except Exception:
            return []
