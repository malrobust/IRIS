<p align="center">
  <img src="assets/logo.png" width="200" alt="IRIS — Unified OSINT Platform">
</p>

<h1 align="center">IRIS</h1>

<p align="center">
  <em>See everything. Know everyone. Intelligence, unified.</em>
</p>

<p align="center">
  <img src="https://img.shields.io/github/stars/malrobust/IRIS?style=flat-square&color=111111&label=stars" alt="Stars">
  <img src="https://img.shields.io/github/v/release/malrobust/IRIS?style=flat-square&color=111111&label=release" alt="Release">
  <img src="https://img.shields.io/badge/targets-Domain%20|%20Email%20|%20IP-111111?style=flat-square" alt="Supported targets">
  <img src="https://img.shields.io/badge/license-MIT-111111?style=flat-square" alt="MIT license">
</p>

<p align="center">
  <strong>WHOIS &middot; DNS &middot; Subdomains &middot; Breaches &middot; Code &middot; Network</strong>
</p>

---

You know the drill. Five different terminal tabs open. Running `whois` in one, `dig` in another, checking `crt.sh` in the browser, and hunting for secrets on GitHub. 

IRIS puts it all into one prompt.

## Before / after

You want to profile a target domain. You manually script together five tools, figure out how to parse their XML/JSON, store the output in ten different text files, and then try to manually correlate the IP addresses to the mail servers.

With IRIS:

```bash
iris > example.com
```

Everything else is done for you. The caching, the correlation, the beautiful neon reporting. One command.

## How it works

Before making you manually verify anything, IRIS runs the target through a multi-tier collection ladder:

```
1. Is it a domain?  → Pull WHOIS, DNS (A, MX, TXT), Subdomains, and live SSL data.
2. Is it an email?  → Run SMTP validation and check the Have I Been Pwned ledger.
3. Is it an IP?     → Ping Geolocation, ASN, and ISP tracking.
4. Code / GitHub?   → Hunt for repository mentions and exposed secrets.
5. Correlate        → Automatically graph the relationships in a local SQLite cache.
```

Lazy, but precise: APIs are cached locally. You aren't burning rate limits. Everything is exported exactly how you want it, instantly.

## Install

Clone it and run the setup.

```bash
git clone https://github.com/malrobust/iris.git
cd iris
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

Copy `.env.example` to `.env` if you have API keys (like GitHub or HIBP). If you don't? It gracefully falls back to simulations and free scraping. It works out of the box anyway.

That was it. One setup.

## Commands

Drop into the interactive loop:
```bash
iris
```

Inside the loop:

| Command | What it does |
|---------|--------------|
| `<target>` | Profile a domain, IP, or email (e.g. `example.com`, `admin@example.com`, `1.1.1.1`) |
| `/export` | Cycle through export modes (`none`, `html`, `json`, `csv`). |
| `clear` | Wipe the console. |
| `quit` | Exit the matrix. |

Or use it as a classic single-shot tool for scripting and CI pipelines:

```bash
iris profile example.com --export html
```

## FAQ

**Does it need API keys?**
No. An optional `.env` file can hold keys for premium lookups, but IRIS defaults to free OSINT sources and simulations if they aren't present.

**Is it a full-screen TUI?**
No, it's a CLI that acts like an interactive REPL. It uses `prompt_toolkit` to give you a clean, beautiful chat-like interface without hijacking your entire terminal buffer, allowing you to scroll back naturally.

**Where is the data stored?**
Everything is automatically cached in a local SQLite database (`iris.db`) to prevent redundant lookups. 

**Why "IRIS"?**
Because it sees everything.

---

## License

[MIT](LICENSE). The clearest license there is.
