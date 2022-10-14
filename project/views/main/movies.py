from flask_restx import Namespace, Resource
from flask import request
from project.container import movie_service
from project.setup.api.models import movie


api = Namespace('movies')


@api.route('/')
class MoviesView(Resource):
    @api.marshal_with(movie, as_list=True, code=200, description='OK')
    def get(self):
        """
        Get all movies.
        """
        return movie_service.get_all(request.args)


@api.route('/<int:mid>/')
class MovieView(Resource):
    @api.response(404, 'Not Found')
    @api.marshal_with(movie, code=200, description='OK')
    def get(self, mid: int):
        """
        Get movie by id.
        """
        return movie_service.get_item(mid)
