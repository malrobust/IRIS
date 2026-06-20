import asyncio
import sys
import os
from typing import List

class SherlockClient:
    """Client for running sherlock to find usernames across social networks."""
    
    async def search_username(self, username: str) -> List[str]:
        """Runs the sherlock CLI tool as a subprocess and parses the output."""
        try:
            sherlock_path = os.path.join(os.path.dirname(sys.executable), "sherlock")
            # We run the command with --print-found to only show successful hits
            process = await asyncio.create_subprocess_exec(
                sherlock_path, username, "--print-found",
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
                    # The format is typically "[+] SiteName: URL"
                    parts = line.replace("[+]", "").strip().split(":", 1)
                    if len(parts) == 2:
                        site = parts[0].strip()
                        accounts.append(site)
                    else:
                        accounts.append(line.replace("[+]", "").strip())
                        
            return accounts
        except Exception:
            return []
