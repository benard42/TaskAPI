from taskapp.models import User,Task
from flask_marshmallow import Schema
from flask_marshmallow.sqla import SQLAlchemyAutoSchema


class UserSchema(Schema):
    class Meta:
        fields = ('id', 'name', 'email')


class TaskSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Task
        include_fk = True