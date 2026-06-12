import argparse
import sys
from rich.console import Console
from rich.table import Table

from utils.storage_handler import load_data, save_data
from models.user import User
from models.project import Project
from models.task import Task

console = Console()

def handle_add_user(args, users, projects):
    if any(u.name.lower() == args.name.lower() for u in users):
        console.print(f"[bold red]Error: User '{args.name}' already exists.[/bold red]")
        return
    try:
        new_user = User(name=args.name, email=args.email)
        users.append(new_user)
        save_data(users, projects)
        console.print(f"[bold green]Successfully registered user: {new_user}[/bold green]")
    except ValueError as e:
        console.print(f"[bold red]Validation Error: {e}[/bold red]")

def handle_add_project(args, users, projects):
    # Enforce relationship check 
    if not any(u.name.lower() == args.user.lower() for u in users):
        console.print(f"[bold red]Error: Assigned User '{args.user}' does not exist. Create them first.[/bold red]")
        return
    if any(p.title.lower() == args.title.lower() for p in projects):
        console.print(f"[bold red]Error: Project Title '{args.title}' already exists.[/bold red]")
        return

    new_project = Project(title=args.title, description=args.desc, due_date=args.due, owner=args.user)
    projects.append(new_project)
    save_data(users, projects)
    console.print(f"[bold green]Successfully created project: {new_project}[/bold green]")

def handle_add_task(args, users, projects):
    project = next((p for p in projects if p.title.lower() == args.project.lower()), None)
    if not project:
        console.print(f"[bold red]Error: Project '{args.project}' not found.[/bold red]")
        return
    
    new_task = Task(title=args.title, assigned_to=args.assigned_to)
    project.add_task(new_task)
    save_data(users, projects)
    console.print(f"[bold green]Task added to '{project.title}' successfully![/bold green]")

def handle_complete_task(args, users, projects):
    project = next((p for p in projects if p.title.lower() == args.project.lower()), None)
    if not project:
        console.print(f"[bold red]Error: Project '{args.project}' not found.[/bold red]")
        return

    task = next((t for t in project.tasks if t.title.lower() == args.task.lower()), None)
    if not task:
        console.print(f"[bold red]Error: Task '{args.task}' not found in project '{args.project}'.[/bold red]")
        return

    task.status = "Completed"
    save_data(users, projects)
    console.print(f"[bold green]Task '{task.title}' updated to Completed![/bold green]")

def render_projects_table(title, projects_list):
    """Utility helper to render a list of projects into a rich UI table."""
    table = Table(title=title, show_lines=True)
    table.add_column("Project Title", style="cyan", no_wrap=True)
    table.add_column("Owner", style="magenta")
    table.add_column("Due Date", style="yellow")
    table.add_column("Description", style="white")
    table.add_column("Tasks Status Breakdown (Title [Status] -> Assignee)", style="green")

    for proj in projects_list:
        task_str = ""
        if not proj.tasks:
            task_str = "[dim italic]No tasks assigned[/dim italic]"
        for t in proj.tasks:
            status_color = "green" if t.status == "Completed" else "orange3"
            task_str += f"• {t.title} [[{status_color}]{t.status}[/{status_color}]] → {t.assigned_to}\n"
        
        table.add_row(proj.title, proj.owner, proj.due_date, proj.description, task_str.strip())

    console.print(table)

def handle_list_projects(args, users, projects):
    # Filter projects based on user flag if supplied
    filtered_projects = projects
    title = "Project Management Overview"
    
    if args.user:
        filtered_projects = [p for p in projects if p.owner.lower() == args.user.lower()]
        title = f"Projects Managed by {args.user}"

    if not filtered_projects:
        console.print("[yellow]No tracked projects found matching target criteria.[/yellow]")
        return

    render_projects_table(title, filtered_projects)

def handle_search_projects(args, users, projects):
    """Searches for keyword matches across project titles, descriptions, and owners."""
    query = args.query.lower()
    matched_projects = [
        p for p in projects
        if query in p.title.lower() or query in p.description.lower() or query in p.owner.lower()
    ]

    if not matched_projects:
        console.print(f"[yellow]No projects found matching the search query: '{args.query}'[/yellow]")
        return

    render_projects_table(f"Search Results for: '{args.query}'", matched_projects)


def main():
    users, projects = load_data()

    parser = argparse.ArgumentParser(description="Multi-User Project CLI Management Infrastructure Engine.")
    subparsers = parser.add_subparsers(dest="command", help="Available subcommands")

    # Add User Command
    parser_user = subparsers.add_parser("add-user", help="Register a system user profile")
    parser_user.add_argument("--name", required=True, help="Explicit Unique Name Identifier")
    parser_user.add_argument("--email", required=True, help="Contact Email Registration Point")

    # Add Project Command
    parser_proj = subparsers.add_parser("add-project", help="Spin up a target user managed project tracking pipeline")
    parser_proj.add_argument("--title", required=True, help="Unique Title string identifier")
    parser_proj.add_argument("--user", required=True, help="System User Name to claim core architecture ownership")
    parser_proj.add_argument("--desc", default="No description provided", help="Short overview write up context context")
    parser_proj.add_argument("--due", default="N/A", help="Target Final Project Execution Deadline")

    # Add Task Command
    parser_task = subparsers.add_parser("add-task", help="Inject contextual operational milestone into project pipeline")
    parser_task.add_argument("--project", required=True, help="Target project collection node title")
    parser_task.add_argument("--title", required=True, help="Distinct task operation objective name")
    parser_task.add_argument("--assigned-to", default="Unassigned", help="Team resource username targeted for workload execution")

    # Complete Task Command
    parser_comp = subparsers.add_parser("complete-task", help="Flag task item execution phase as completed")
    parser_comp.add_argument("--project", required=True, help="Parent project system tracking container node title")
    parser_comp.add_argument("--task", required=True, help="The contextual task title explicitly targeted for compilation completion")

    # List Projects Command
    parser_list = subparsers.add_parser("list-projects", help="Output runtime project table metrics summaries visualizer matrix")
    parser_list.add_argument("--user", help="Optional parameter query string used to isolate tracking metrics data vectors by specific user node")

    # Search Projects Command
    parser_search = subparsers.add_parser("search-projects", help="Search projects by keyword (title, description, or owner)")
    parser_search.add_argument("--query", required=True, help="Search string keyword query")

    args = parser.parse_args()

    # Route execution logic
    if args.command == "add-user":
        handle_add_user(args, users, projects)
    elif args.command == "add-project":
        handle_add_project(args, users, projects)
    elif args.command == "add-task":
        handle_add_task(args, users, projects)
    elif args.command == "complete-task":
        handle_complete_task(args, users, projects)
    elif args.command == "list-projects":
        handle_list_projects(args, users, projects)
    elif args.command == "search-projects":
        handle_search_projects(args, users, projects)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()