#!/usr/bin/env python3


import json
from pathlib import Path
import argparse
import datetime
import sys


def get_all_tasks(filename):
    if not filename.exists():
        return []
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError:
        print(f"Error: {filename} is corrupted or not valid JSON", file=sys.stderr)
        sys.exit(1)


def write_all_tasks(filename, tasks):
    with open(filename, 'w') as f:
        json.dump(tasks, f, indent=2)


def get_actual_time():
    return datetime.datetime.now().isoformat()


def update_task(filename, tasks, task_id, key, value):
    for task in tasks:
        if task['id'] == task_id:
            task[key] = value
            task['updatedAt'] = get_actual_time()
            write_all_tasks(filename, tasks)
            print(f"Task: {task_id} {key} updated successfully")
            return 

    print(f"Error: Task with ID {task_id} does not exist", file=sys.stderr)
    sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="A simple CLI tool.")
    
    group = parser.add_mutually_exclusive_group(required=True)

    group.add_argument('-a', '--add', type=str, help='Add new task')
    group.add_argument('-l', '--list', nargs='?', const='all', choices=['all', 'todo', 'in-progress', 'done'], help='List tasks (default: all)')
    group.add_argument('-d', '--delete', type=int, help='Delete a task by ID')
    group.add_argument('-u', '--update', nargs=2, metavar=('ID', 'DESCRIPTION'), help="Update description of task with the given ID" )
    group.add_argument('--mark-in-progress', type=int, help='Update status of a task to "in progress"')
    group.add_argument('--mark-done', type=int, help='Update status of a task to "done"')

    args = parser.parse_args()

    json_file = Path.home() / ".task-cli.json"
    tasks = get_all_tasks(json_file)

    if args.add is not None:
        description = args.add.strip()
        if not description:
            print("Error: description cannot be empty", file=sys.stderr)
            sys.exit(1)

        new_id = max((task["id"] for task in tasks), default=0) + 1        
        now = get_actual_time()

        task = {
            "id": new_id,
            "description": description,
            "status": "todo",
            "createdAt": now,
            "updatedAt": now
        }
        
        tasks.append(task)
        write_all_tasks(json_file, tasks)
        print(f"Task added successfully (ID: {new_id})")

    elif args.delete is not None:        

        orig_len = len(tasks)
        tasks = [task for task in tasks if task["id"] != args.delete]
        
        if orig_len == len(tasks):
            print(f"Error: task with ID: {args.delete} does not exist", file=sys.stderr)
            sys.exit(1)

        write_all_tasks(json_file, tasks)
        print(f"Task {args.delete} deleted successfully")
    
    elif args.list is not None:
        for task in tasks:
            if args.list == 'all' or args.list == task["status"]:
                print(f"Task id: {task['id']}")
                print(f"Task description: {task['description']}")
                print(f"Task status: {task['status']}")
                print(f"Task createdAt: {task['createdAt']}")
                print(f"Task updatedAt: {task['updatedAt']}")
                print()

    
    elif args.update is not None:
        try:
            update_id = int(args.update[0])
        except ValueError:
            print("Error: Task ID must be a number.", file=sys.stderr)
            sys.exit(1)
        
        new_description = args.update[1].strip()
        if not new_description:
            print("Error: description cannot be empty", file=sys.stderr)
            sys.exit(1)

        update_task(json_file, tasks, update_id, "description", new_description)

    elif args.mark_in_progress is not None:
        update_task(json_file, tasks, args.mark_in_progress, "status", "in-progress")
    
    elif args.mark_done is not None:
        update_task(json_file, tasks, args.mark_done, "status", "done")
    
            
if __name__ == "__main__":
    main()