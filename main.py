from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from agent.gemini_agent import build_agent, ask_agent

console = Console()

def print_welcome():
    console.print(Panel(
        "[bold cyan]Welcome to LifeSync[/bold cyan]\n"
        "Your AI-powered productivity command center\n\n"
        "[dim]Type 'exit' to quit[/dim]",
        border_style="cyan"
    ))

def print_response(text: str):
    console.print(Panel(text, title="[bold green]LifeSync[/bold green]", border_style="green"))

def main():
    print_welcome()
    
    console.print("[bold green]Connecting to Gemini...[/bold green]")
    chat = build_agent()
    console.print("[bold green]✅ Ready! Ask me anything.[/bold green]\n")

    while True:
        user_input = Prompt.ask("[bold yellow]You[/bold yellow]")

        if user_input.lower() in ['exit', 'quit']:
            console.print("[bold cyan]Goodbye! 👋[/bold cyan]")
            break

        if not user_input.strip():
            continue

        response = ask_agent(chat, user_input)
        print_response(response)

if __name__ == "__main__":
    main()