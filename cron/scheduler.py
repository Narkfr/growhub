import os
import importlib.util
from celery import Celery

# Initialisation de l'application Celery
app = Celery('scheduler', broker='redis://localhost:6379/0')

def import_jobs_from_file(file_path):
    spec = importlib.util.spec_from_file_location("jobs", file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def schedule_jobs():
    devices_dir = os.path.join(os.path.dirname(__file__), '../devices')
    
    for folder_name in os.listdir(devices_dir):
        folder_path = os.path.join(devices_dir, folder_name)

        if os.path.isdir(folder_path) and folder_name.startswith('device_'):
            jobs_file = os.path.join(folder_path, 'src', 'jobs.py')

            if os.path.exists(jobs_file):
                print(f"Loading jobs from: {jobs_file}")
                jobs_module = import_jobs_from_file(jobs_file)
                
                if hasattr(jobs_module, 'register_tasks'):
                    jobs_module.register_tasks(app)
                else:
                    print(f"Warning: No 'register_tasks' function found in {jobs_file}")

if __name__ == "__main__":
    print("Scheduling jobs...")
    schedule_jobs()
    print("All jobs scheduled.")
