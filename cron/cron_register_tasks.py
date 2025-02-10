import sys
import importlib.util
import pathlib
import json
import requests

# Path to the devices folder (relative to this script)
DEVICES_PATH = pathlib.Path(__file__).parent.parent / "devices"

# URL to the Flask API endpoint
FLASK_API_URL = "http://localhost:5000/schedule_tasks"

def load_and_execute_tasks():
    """Load and execute register_tasks() from each device's tasks.py file."""
    all_tasks = []

    # Find all matching device directories
    for device_path in DEVICES_PATH.glob("device_*"):
        tasks_file = device_path / "src/tasks.py"
        if tasks_file.exists():
            try:
                # Import tasks.py dynamically
                spec = importlib.util.spec_from_file_location("tasks", str(tasks_file))
                tasks_module = importlib.util.module_from_spec(spec)
                sys.modules["tasks"] = tasks_module
                spec.loader.exec_module(tasks_module)

                # Execute register_tasks() and collect tasks
                if hasattr(tasks_module, "register_tasks"):
                    tasks = tasks_module.register_tasks()
                    all_tasks.extend(tasks)
                    print(f"✅ Loaded {len(tasks)} tasks from {device_path.name}")
                else:
                    print(f"⚠️ No register_tasks() function in {device_path.name}/tasks.py")
            
            except Exception as e:
                print(f"❌ Error loading {device_path.name}/tasks.py: {e}")
    
    if all_tasks:
        try:
            response = requests.post(FLASK_API_URL, json={"tasks": all_tasks})
            if response.status_code == 200:
                print("🚀 Tasks successfully sent to API")
            else:
                print(f"⚠️ API response error: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"❌ Failed to send tasks to API: {e}")

    # Print the final aggregated tasks
    print("\n📋 Final Task List:")
    print(json.dumps(all_tasks, indent=2))

if __name__ == "__main__":
    load_and_execute_tasks()
