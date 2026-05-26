import json
import os
from datetime import datetime
 
TODO_FILE = "todos.json"
 
def load_todos():
    """Load todos from file. Returns empty list if file doesn't exist."""
    if not os.path.exists(TODO_FILE):
        return []
    try:
        with open(TODO_FILE, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        print("Warning: todo file was corrupted. Starting fresh.")
        return []
    except IOError as e:
        print(f"Error reading file: {e}")
        return []
 
def save_todos(todos):
    """Save todos list to file."""
    try:
        with open(TODO_FILE, "w") as f:
            json.dump(todos, f, indent=2)
    except IOError as e:
        print(f"Error saving todos: {e}")
 
def add_todo(todos, title):
    todo = {
        "id": len(todos) + 1,
        "title": title,
        "done": False,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
    }
    todos.append(todo)
    save_todos(todos)
    print(f"Added: {title}")
 
def list_todos(todos):
    if not todos:
        print("No todos yet.")
        return
    print(f"\n{'ID':<5} {'Status':<10} {'Title':<40} {'Created'}")
    print("-" * 70)
    for t in todos:
        status = "[done]" if t["done"] else "[    ]"
        print(f"{t['id']:<5} {status:<10} {t['title']:<40} {t['created_at']}")
 
def complete_todo(todos, todo_id):
    for t in todos:
        if t["id"] == todo_id:
            if t["done"]:
                print(f"Todo #{todo_id} is already marked as done.")
            else:
                t["done"] = True
                save_todos(todos)
                print(f"Marked done: {t['title']}")
            return
    print(f"Todo with ID {todo_id} not found.")
 
def delete_todo(todos, todo_id):
    for i, t in enumerate(todos):
        if t["id"] == todo_id:
            removed = todos.pop(i)
            save_todos(todos)
            print(f"Deleted: {removed['title']}")
            return
    print(f"Todo with ID {todo_id} not found.")
 
def main():
    todos = load_todos()
    print("CLI Todo App")
    print("Commands: add, list, done, delete, quit")
 
    while True:
        command = input("\n> ").strip().lower()
        if command == "quit":
            print("Goodbye.")
            break
        elif command == "list":
            list_todos(todos)
        elif command.startswith("add "):
            title = command[4:].strip()
            if title:
                add_todo(todos, title)
            else:
                print("Usage: add <task title>")
        elif command.startswith("done "):
            try:
                todo_id = int(command[5:].strip())
                complete_todo(todos, todo_id)
            except ValueError:
                print("Usage: done <id>  (id must be a number)")
        elif command.startswith("delete "):
            try:
                todo_id = int(command[7:].strip())
                delete_todo(todos, todo_id)
            except ValueError:
                print("Usage: delete <id>  (id must be a number)")
        else:
            print("Unknown command. Try: add, list, done, delete, quit")
 
if __name__ == "__main__":
    main()
