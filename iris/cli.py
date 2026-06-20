import asyncio
import os
import typer
from rich.console import Console
from rich.columns import Columns
from rich.text import Text
from rich.table import Table
from prompt_toolkit import PromptSession
from prompt_toolkit.formatted_text import FormattedText
from prompt_toolkit.styles import Style

from iris.collectors.domain import DomainCollector
from iris.collectors.email import EmailCollector
from iris.collectors.network import NetworkCollector
from iris import exporters
from iris.db import cache

app = typer.Typer(
    name="iris",
    help="Unified OSINT intelligence platform.",
    no_args_is_help=False,
)
console = Console()

def print_banner():
    # Geometric Origami-style Logo
    logo = Text()
    logo.append("               ▄▄               \n", style="bold #d7a8ff")
    logo.append("              ████              \n", style="bold #c380ff")
    logo.append("             ██████             \n", style="bold #a855f7")
    logo.append("            ████████            \n", style="bold #a855f7")
    logo.append("           ██████████           \n", style="bold #a855f7")
    logo.append("▄▄▄▄▄▄▄▄▄▄████████████▄▄▄▄▄▄▄▄▄▄\n", style="bold #9333ea")
    logo.append("████████████████████████████████\n", style="bold #9333ea")
    logo.append("▀▀▀▀▀▀▀▀▀██████████████▀▀▀▀▀▀▀▀▀\n", style="bold #7e22ce")
    logo.append("              ████              \n", style="bold #6b21a8")
    logo.append("             ██████             \n", style="bold #6b21a8")
    logo.append("              ████              \n", style="bold #581c87")
    logo.append("               ▀▀               ", style="bold #581c87")
    
    info = Text()
    info.append("\n\n\nIRIS OSINT Platform ", style="bold white")
    info.append("v0.1.0\n", style="dim")
    info.append("See everything. Know everyone.\n", style="dim")
    info.append(os.getcwd(), style="dim")
    
    console.print("\n")
    console.print(Columns([logo, info], padding=(0, 2)))
    console.print("\n")

def run_profile(target: str, export: str = "none") -> None:
    if "@" in target:
        collector = EmailCollector()
    elif target.replace(".", "").isdigit():
        collector = NetworkCollector()
    else:
        collector = DomainCollector()
    
    try:
        data = asyncio.run(collector.collect(target))
        
        table = Table(box=None, show_header=False, padding=(0, 2))
        table.add_column("Attribute", style="bold #00ff88")
        table.add_column("Value", style="white")
        
        for k, v in data.items():
            if k != "_raw":
                val_str = str(v)
                table.add_row(f"● {k}", val_str[:150] + ("..." if len(val_str) > 150 else ""))

        console.print("\n")
        console.print(table)
        console.print("\n")

        if export != "none":
            filename = f"iris_{target.replace('.', '_').replace('@', '_at_')}.{export}"
            if export == "json":
                exporters.json_export(data, filename)
            elif export == "html":
                exporters.html_export(data, filename)
            elif export == "csv":
                exporters.csv_export(data, filename)
            console.print(f"[dim]Export saved to {filename}[/dim]\n")
    except Exception as e:
        console.print(f"\n[red]❌ Error gathering data: {e}[/red]\n")
    finally:
        asyncio.run(collector.close())

style = Style.from_dict({
    'prompt': 'bold #ffffff',
    'bottom-toolbar': 'bg:#1e1e1e #888888',
})

def interactive_shell():
    print_banner()
    
    session = PromptSession(style=style)
    export_mode = "none"
    
    def get_bottom_toolbar():
        export_text = f"Export: {export_mode.upper()} (type /export to change)"
        return FormattedText([
            ('class:bottom-toolbar', f' ? for help                                {export_text}')
        ])

    while True:
        try:
            # Top boundary line for prompt
            console.print("─" * console.width, style="dim")
            
            text = session.prompt('> ', bottom_toolbar=get_bottom_toolbar).strip()
            
            # Bottom boundary line after input is submitted
            console.print("─" * console.width, style="dim")
            
            if not text:
                continue
                
            if text.lower() in ["exit", "quit", "/quit"]:
                break
            if text.lower() in ["clear", "cls", "/clear"]:
                console.clear()
                print_banner()
                continue
            if text.lower() == "?":
                console.print("\n[bold]Commands:[/bold]")
                console.print("  [cyan]<target>[/cyan]   Profile a domain, IP, or email")
                console.print("  [cyan]/export[/cyan]    Toggle export mode (none, html, json, csv)")
                console.print("  [cyan]clear[/cyan]      Clear the terminal screen")
                console.print("  [cyan]quit[/cyan]       Exit IRIS\n")
                continue
            if text.lower() == "/export":
                modes = ["none", "html", "json", "csv"]
                idx = modes.index(export_mode)
                export_mode = modes[(idx + 1) % len(modes)]
                console.print(f"\n[dim]● Export mode set to {export_mode.upper()}[/dim]\n")
                continue
            
            console.print(f"\n● [dim]Gathering intelligence on {text}...[/dim]")
            run_profile(text, export_mode)
            
        except KeyboardInterrupt:
            # Handle Ctrl+C gracefully
            console.print("─" * console.width, style="dim")
            continue
        except EOFError:
            # Handle Ctrl+D
            break

@app.callback(invoke_without_command=True)
def root(ctx: typer.Context):
    if ctx.invoked_subcommand is None:
        cache.init_db()
        interactive_shell()

@app.command()
def profile(
    target: str = typer.Argument(..., help="Domain, email, or IP to profile"),
    export: str = typer.Option("none", help="Export format: json|html|csv"),
):
    """Profile a target across all OSINT sources."""
    cache.init_db()
    print_banner()
    console.print(f"\n● [dim]Gathering intelligence on {target}...[/dim]")
    run_profile(target, export)

if __name__ == "__main__":
    app()
