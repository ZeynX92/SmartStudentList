import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin
from .db_session import SqlAlchemyBase


class Student(SqlAlchemyBase, SerializerMixin):
    """Класс модели ученика"""
    __tablename__ = 'students'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    surname = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    lastname = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    telephone_number = sqlalchemy.Column(sqlalchemy.String, index=True, nullable=True,
                                         default='Номер отсутствует...')
    email = sqlalchemy.Column(sqlalchemy.String, index=True, nullable=True,
                              default='E-mail отсутствует...')
    note = sqlalchemy.Column(sqlalchemy.String, nullable=True, default='Заметка отсутствует...')

    def __repr__(self):
        return f'Student <{self.id}> {self.surname} {self.name}'
