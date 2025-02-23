import json


def register_tasks():
    # Create the task list
    tasks = [
        {"topic": "chicken/door", "message": "open", "delay": 60},
        {"topic": "chicken/door", "message": "close", "delay": 120},
    ]

    return tasks

# Execute the script
if __name__ == "__main__":
    tasks = register_tasks()
    print(json.dumps(tasks, indent=2))
