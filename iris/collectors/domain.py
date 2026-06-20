import asyncio
from typing import Dict, Any

from iris.collectors import BaseCollector
from iris.api_clients.free_sources import FreeSourcesClient



class DomainCollector(BaseCollector):
    """Collector for domain-related intelligence."""

    def __init__(self):
        super().__init__()
        self.client = FreeSourcesClient()

    async def collect(self, target: str) -> Dict[str, Any]:
        """Gather intelligence on a domain target."""
        domain = target.strip().lower()


        # Run everything concurrently, including WHOIS via executor
        loop = asyncio.get_running_loop()
        results = await asyncio.gather(
            self.client.get_subdomains_crtsh(domain),
            self.client.get_dns_records(domain),
            self.client.get_ssl_cert(domain),
            loop.run_in_executor(None, self.client.get_whois, domain),
            return_exceptions=True
        )

        subdomains  = results[0] if not isinstance(results[0], Exception) else []
        dns_records = results[1] if not isinstance(results[1], Exception) else {}
        ssl_cert    = results[2] if not isinstance(results[2], Exception) else {}
        whois_data  = results[3] if not isinstance(results[3], Exception) else {}

        raw_data = {
            "domain":      domain,
            "whois_data":  whois_data,
            "dns_records": dns_records,
            "subdomains":  subdomains,
            "ssl_cert":    ssl_cert,
        }



        return self.parse(raw_data)

    def parse(self, raw: Dict[str, Any]) -> Dict[str, Any]:
        """Normalize raw data into a structured report format."""
        dns   = raw.get("dns_records", {})
        whois = raw.get("whois_data", {})
        ssl   = raw.get("ssl_cert", {})

        def join(lst, limit=80):
            return ", ".join(lst)[:limit] if lst else "None"

        parsed = {
            # WHOIS
            "Domain":     raw.get("domain"),
            "Registrar":  whois.get("registrar", "Unknown"),
            "Created":    whois.get("creation_date", "Unknown"),
            "Expires":    whois.get("expiration_date", "Unknown"),
            "Updated":    whois.get("updated_date", "Unknown"),
            "Status":     join(whois.get("status", []), 80),
            "Name Servers": join(whois.get("name_servers", []), 100),
            # DNS
            "A Records":  join(dns.get("A", []), 100),
            "MX Records": join(dns.get("MX", []), 100),
            "NS Records": join(dns.get("NS", []), 100),
            "TXT Records": join(dns.get("TXT", []), 100),
            "SPF":        join(dns.get("SPF", []), 120),
            "DMARC":      join(dns.get("DMARC", []), 120),
            # SSL
            "SSL Issuer":    ssl.get("issuer_cn", "Unknown"),
            "SSL Expires":   ssl.get("expires", "Unknown"),
            "SSL Alt Names": join(ssl.get("alt_names", []), 120),
            # Summary
            "Subdomains Found": len(raw.get("subdomains", [])),
        }

        parsed["_raw"] = raw
        return parsed
