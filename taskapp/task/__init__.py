from taskapp.task.resource import TasksResource


def task_routes(api):
    api.add_resource(TasksResource, '/api/task', '/api/task/<int:task_id>')
    