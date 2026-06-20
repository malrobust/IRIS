import pytest
from iris.collectors.domain import DomainCollector
from iris.collectors.network import NetworkCollector
from iris.collectors.email import EmailCollector

def test_domain_collector_parse():
    collector = DomainCollector()
    raw = {
        "domain": "example.com",
        "whois_data": {"registrar": "Test Registrar"},
        "dns_records": {"A": ["1.2.3.4"]},
        "subdomains": ["www.example.com", "api.example.com"],
        "ssl_cert": {"issuer_cn": "Let's Encrypt"}
    }
    
    parsed = collector.parse(raw)
    
    assert parsed["Domain"] == "example.com"
    assert parsed["Registrar"] == "Test Registrar"
    assert parsed["A Records"] == "1.2.3.4"
    assert parsed["Subdomains Found"] == 2
    assert parsed["SSL Issuer"] == "Let's Encrypt"
    assert "_raw" in parsed

def test_network_collector_parse():
    collector = NetworkCollector()
    raw = {
        "target": "1.2.3.4",
        "ip": "1.2.3.4",
        "geo": {
            "country": "US",
            "city": "New York",
            "isp": "Test ISP",
            "proxy": True
        }
    }
    
    parsed = collector.parse(raw)
    
    assert parsed["Resolved IP"] == "1.2.3.4"
    assert parsed["ISP"] == "Test ISP"
    assert "New York" in parsed["Location"]
    assert "US" in parsed["Location"]
    assert "Proxy" in parsed["Flags"]

def test_email_collector_parse():
    collector = EmailCollector()
    raw = {
        "email": "test@example.com",
        "breached": True,
        "has_smtp": True,
        "sources": ["LinkedIn", "MySpace"]
    }
    
    parsed = collector.parse(raw)
    
    assert parsed["Email"] == "test@example.com"
    assert "YES" in parsed["Breached"]
    assert "YES" in parsed["Valid SMTP"]
    assert "LinkedIn, MySpace" == parsed["Breach Sources"]
