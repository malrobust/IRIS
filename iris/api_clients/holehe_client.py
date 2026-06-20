import asyncio
from typing import List

import sys
import os

class HoleheClient:
    """Client for running holehe to find registered accounts across 120+ sites."""
    
    async def get_registered_accounts(self, email: str) -> List[str]:
        """Runs the holehe CLI tool as a subprocess and parses the output."""
        try:
            holehe_path = os.path.join(os.path.dirname(sys.executable), "holehe")
            # We run the command with --only-used and --no-color to make parsing easy
            process = await asyncio.create_subprocess_exec(
                holehe_path, email, "--only-used", "--no-color",
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
                if line.startswith("[+]") and "Email used" not in line:
                    site = line.replace("[+]", "").strip()
                    accounts.append(site)
                    
            return accounts
        except Exception:
            return []
