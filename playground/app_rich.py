from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt
from rich.panel import Panel
import os

class TodoApp:
    def __init__(self):
        self.console = Console()
        self.tasks = []

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def display_tasks(self):
        self.clear_screen()
        table = Table(title="Todo List")
        table.add_column("ID", justify="center", style="cyan")
        table.add_column("Task", style="magenta")

        for idx, task in enumerate(self.tasks):
            table.add_row(str(idx + 1), task)

        self.console.print(Panel(table))

    def add_task(self):
        task = Prompt.ask("Enter a new task")
        self.tasks.append(task)
        self.display_tasks()

    def remove_task(self):
        self.display_tasks()
        task_id = Prompt.ask("Enter the task ID to remove", default="0")
        if task_id.isdigit() and 0 < int(task_id) <= len(self.tasks):
            self.tasks.pop(int(task_id) - 1)
        else:
            self.console.print("Invalid task ID!", style="bold red")
        self.display_tasks()

    def run(self):
        while True:
            self.display_tasks()
            action = Prompt.ask("Choose an action (add/remove/exit)", choices=["add", "remove", "exit"])
            if action == "add":
                self.add_task()
            elif action == "remove":
                self.remove_task()
            elif action == "exit":
                self.clear_screen()
                break

if __name__ == "__main__":
    app = TodoApp()
    app.run()
