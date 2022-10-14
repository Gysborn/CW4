from flask import request
from flask_restx import Namespace, Resource

from project.container import user_service
from project.setup.api.models import user

api = Namespace('auth')


@api.route('/register')
class RegisterView(Resource):

    @api.marshal_with(user, as_list=True, code=200, description='OK')
    def post(self): # Регистрация с помощью пароля и имейл
        data = request.json
        if data.get('email') and data.get('password'):
            return user_service.create_user(data.get('email'), data.get('password')), 201
        else:
            return 'error', 401


@api.route('/login')
class LoginView(Resource):

    @api.response(404, 'Not found')
    def post(self): # Получения токенов по паролю логину

        data = request.json
        if data.get('email') and data.get('password'):
            return user_service.check(data.get('email'), data.get('password')), 201

    @api.response(404, 'Not found')
    def put(self): # Обновление токенов

        data = request.json
        if data.get('refresh_token'):
            return user_service.update_token(data.get('refresh_token')), 201
        else:
            return 'error', 401

