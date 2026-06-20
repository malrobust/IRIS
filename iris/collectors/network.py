import ipaddress
import socket
from typing import Dict, Any

from iris.collectors import BaseCollector
from iris.db import cache


class NetworkCollector(BaseCollector):
    """Collector for network-related intelligence (IPs, Geolocation, ASN)."""

    async def collect(self, target: str) -> Dict[str, Any]:
        """Gather intelligence on an IP target."""
        target = target.strip()

        # Resolve hostname to IP if needed
        ip_address = target
        try:
            ipaddress.ip_address(target)
        except ValueError:
            try:
                loop_ip = socket.gethostbyname(target)
                ip_address = loop_ip
            except socket.gaierror:
                return self.parse({"target": target, "error": "Could not resolve to an IP address."})

        # Check cache
        cached_data = cache.get_cached_ip(target)
        if cached_data:
            return self.parse({
                "target": cached_data["target"],
                "ip": cached_data["ip_address"],
                "geo": cached_data["geo"]
            })

        url = (
            f"http://ip-api.com/json/{ip_address}"
            f"?fields=status,message,country,regionName,city,zip,lat,lon,isp,org,as,reverse,mobile,proxy,hosting"
        )
        data = await self._fetch(url)

        if not data or data.get("status") != "success":
            msg = data.get("message", "API query failed") if data else "Network error"
            return self.parse({"target": target, "ip": ip_address, "error": msg})

        raw_data = {
            "target":  target,
            "ip":      ip_address,
            "geo":     data,
        }

        cache.save_ip(
            target=target,
            ip_address=ip_address,
            geo_data=data
        )

        return self.parse(raw_data)

    def parse(self, raw: Dict[str, Any]) -> Dict[str, Any]:
        """Normalize raw data into a structured report format."""
        if "error" in raw:
            return {"Target": raw.get("target"), "Error": raw.get("error"), "_raw": raw}

        geo = raw.get("geo", {})
        flags = []
        if geo.get("proxy"):
            flags.append("Proxy")
        if geo.get("hosting"):
            flags.append("Hosting/VPN")
        if geo.get("mobile"):
            flags.append("Mobile")

        parsed = {
            "Target":       raw.get("target"),
            "Resolved IP":  raw.get("ip"),
            "Hostname":     geo.get("reverse", "—"),
            "Location":     f"{geo.get('city', '?')}, {geo.get('regionName', '?')}, {geo.get('country', '?')}",
            "Coordinates":  f"{geo.get('lat', '?')}, {geo.get('lon', '?')}",
            "ISP":          geo.get("isp", "Unknown"),
            "Organization": geo.get("org", "Unknown"),
            "ASN":          geo.get("as", "Unknown"),
            "Flags":        ", ".join(flags) if flags else "None",
        }
        parsed["_raw"] = raw
        return parsed
