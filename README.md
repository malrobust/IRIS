<p align="center">
  <img src="assets/logo-dark.png" width="200" alt="IRIS — Unified OSINT Platform">
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
3. Is it an IP?     → Ping Geolocation, ASN, ISP tracking, and Shodan for open ports/vulnerabilities.
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

You can configure premium APIs (like Shodan, GitHub, or HaveIBeenPwned) directly inside the CLI:
```bash
iris > /config set SHODAN_API_KEY=your_key_here
```
No need to mess with `.env` files. IRIS will store your keys securely in `~/.iris/config.json`. If you don't have keys, IRIS gracefully falls back to free scraping and simulations.

## Commands

Drop into the interactive loop:
```bash
iris
```

Inside the loop:

| Command | What it does |
|---------|--------------|
| `<target>` | Profile a domain, IP, or email (e.g. `example.com`, `admin@example.com`, `1.1.1.1`) |
| `/code <target>` | Search GitHub for repositories and secrets related to an organization or domain. |
| `/export` | Cycle through export modes (`none`, `html`, `json`, `csv`). |
| `/history` | Show recently profiled targets. |
| `/config set <K>=<V>`| Set an API key securely (e.g. `HIBP_API_KEY=123`). |
| `/status` | Check which API keys are configured and active. |
| `clear` | Wipe the console. |
| `quit` | Exit the matrix. |

Or use it as a classic single-shot tool for scripting and CI pipelines:

```bash
iris profile example.com --export html
```

## FAQ

**Does it need API keys?**
No. It works out of the box with free OSINT sources. You can add keys for premium lookups (Shodan, GitHub, HIBP) directly inside the CLI using the `/config set` command.

**Is it a full-screen TUI?**
No, it's a CLI that acts like an interactive REPL. It uses `prompt_toolkit` to give you a clean, beautiful chat-like interface without hijacking your entire terminal buffer, allowing you to scroll back naturally.

**Where is the data stored?**
Everything is automatically cached in a local SQLite database (`iris.db`) to prevent redundant lookups. 

**Why "IRIS"?**
Because it sees everything.

---

## License

[MIT](LICENSE). The clearest license there is.
