def register_tasks(app):
    @app.task
    def example_task():
        print("Running example task")
