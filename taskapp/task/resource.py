from datetime import datetime
from taskapp.models import Task
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource, reqparse

from taskapp.schemas.app_schemas import TaskSchema

todo_schema = TaskSchema()
todos_schema = TaskSchema(many=True)

# Todos Resource
class TasksResource(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()

    @jwt_required()
    def post(self):
        self.parser.add_argument('Task_name', type=str, required=True, help='Description cannot be blank')
        self.parser.add_argument('due_date', type=str, required=True, help='Due date cannot be blank')

        data = self.parser.parse_args()

        # create date object from string => needed by sqlite db
        data['due_date'] = datetime.strptime(data['due_date'], '%Y-%m-%d')

        user_id = get_jwt_identity()

        new_todo = Todo(**data, created_by=user_id)
        new_todo.save()
        return {'message': 'task created successfully'}, 201

    @jwt_required()
    def get(self, task_id=None):
        if task_id:
            task = Task.get_task_by_id(task_id)
            if task:
                return task_schema.dump(task), 200
            return {'message': 'task not found'}, 404

        user_id = get_jwt_identity()
        user_task = Task.get_user_todos(user_id)
        return todos_schema.dump(user_task), 200

    
    @jwt_required()
    def put(self, todo_id):
        # While updating a todo, all fields are optional
        self.parser.add_argument('Task_name', type=str)
        self.parser.add_argument('due_date', type=str)
        self.parser.add_argument('Task_status', type=bool)
        
        task = Task.get_task_by_id(task_id)

        if not task:
            return {'message': 'Task not found'}, 404

        # check for ownership
        if task.created_by != get_jwt_identity():
            return {'message': 'You are not authorized to update this task'}, 401

        data = self.parser.parse_args()

        # update todo if there is new data else keep the old data
        task.Task_name = data['Task_name'] if data['Task_name'] else task.Task_name
        task.due_date = datetime.strptime(data['due_date'], '%Y-%m-%d') if data['due_date'] else task.due_date
        task.Task_status = data['Task_status'] if data['Task_status'] else task.Task_status
        task.update()

        # return updated todo
        return task_schema.dump(task), 200


    @jwt_required()
    def delete(self, task_id):
        todo = Task.get_task_by_id(task_id)

        if not task:
            return {'message': 'Task not found'}, 404

        # check for ownership
        if task.created_by != get_jwt_identity():
            return {'message': 'You are not authorized to delete this task'}, 401

        todo.delete()
        return {'message': 'Task deleted successfully'}, 200

        