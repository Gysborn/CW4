from sqlalchemy import desc

from project.dao.base import BaseDAO
from project.models import Genre, Director, Movie, User
from project.tools.security import generate_password_hash


class GenresDAO(BaseDAO[Genre]):
    __model__ = Genre


class DirectorsDAO(BaseDAO[Director]):
    __model__ = Director


class MoviesDAO(BaseDAO[Movie]):
    __model__ = Movie

    def get_all_filter_by(self, filters):
        stmt = self._db_session.query(self.__model__)
        if "director_id" in filters:
            if filters['director_id'].isdigit():
                stmt = stmt.filter(Movie.director_id == filters.get("director_id"))
        if "genre_id" in filters:
            if filters['genre_id'].isdigit():
                stmt = stmt.filter(Movie.genre_id == filters.get("genre_id"))
        if "status" in filters:
            if filters['status'].lower() == 'new':
                stmt = stmt.order_by(desc(Movie.year))
        if "page" in filters:
            try:
                return stmt.paginate(page=int(filters['page']), per_page=12).items
            except Exception as e:
                print(e)
                return stmt.all()

        return stmt.all()


class UsersDAO(BaseDAO[User]):
    __model__ = User

    def create(self, login, password):
        try:
            self._db_session.add(User(email=login, password=generate_password_hash(password)))
            self._db_session.commit()

        except Exception as e:
            print(e)
            self._db_session.rollback()

    def get_user_by_login(self, login):

        try:
            stmt = self._db_session.query(self.__model__).filter(self.__model__.email == login).one()
            return stmt

        except Exception as e:
            print(e)
            return {}

    def update(self, login, data):

        try:
            self._db_session.query(self.__model__).filter(self.__model__.email == login).update(data)
            self._db_session.commit()

        except Exception as e:
            print(e)
            self._db_session.rollback()