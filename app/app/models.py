from app import Config

if Config.USE_CORE_DB:
    print('loading project with SqlAlchemyCore')
    from sqlalchemy import (Column, BigInteger, String, DateTime, Table, ForeignKey)
    from sqlalchemy.orm import (relationship)
    from .database import Base

else:
    print('loading project with Flask-SqlAlchemy')
    from app import db

    Table = db.Table
    Column = db.Column
    BigInteger = db.BigInteger
    String = db.String
    DateTime = db.DateTime
    ForeignKey = db.ForeignKey
    relationship = db.relationship
    Base = db.Model


# using the association table pattern to allow many-to-many relationships
# tho this enforces unique entries. playlists can't hold duplicate media
# cleaning is done by the relationship
# https://docs.sqlalchemy.org/en/13/orm/basic_relationships.html#deleting-rows-from-the-many-to-many-table

users_articles_association = Table('users_articles', Base.metadata,
                                   Column('user_id', BigInteger, ForeignKey('users.id')),
                                   Column('article_id', BigInteger, ForeignKey('articles.id'))
                                   )


class User(Base):
    __tablename__ = 'users'

    id = Column(BigInteger, primary_key=True)
    email = Column(String(120), index=True, unique=True, nullable=False)
    first_name = Column(String(50), nullable=True)
    last_name = Column(String(50), nullable=True)

    articles = relationship('Article',
                           secondary=users_articles_association,
                           back_populates='users',
                           lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.email)


class Article(Base):
    __tablename__ = 'articles'

    id = Column(BigInteger, primary_key=True)

    title = Column(String(50), nullable=False)
    publish_date = Column(DateTime, nullable=True)

    users = relationship('User',
                         secondary=users_articles_association,
                         back_populates='articles',
                         lazy='dynamic')
