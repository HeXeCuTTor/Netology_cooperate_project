import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship
from config import login, password, db_name

Base = declarative_base()

DSN = f'postgresql://{login}:{password}@localhost:5432/{db_name}'
engine = sq.create_engine(DSN)


class User(Base):
    __tablename__ = 'user'

    user_id = sq.Column(sq.Integer, primary_key=True)
    first_name = sq.Column(sq.String, nullable=False)
    last_name = sq.Column(sq.String, nullable=False)
    profile_link = sq.Column(sq.String, nullable=False)
    selected = sq.Column(sq.Boolean, default=False)

    def __str__(self):
        return f'User {self.user_id} : ({self.first_name}, {self.last_name}, {self.profile_link}, {self.selected})'


class Photos(Base):
    __tablename__ = 'photos'

    photo_id = sq.Column(sq.Integer, primary_key=True)
    photo = sq.Column(sq.String, nullable=False) # Данные о фотографии

    def __str__(self):
        return f'Photos {self.photo_id} : {self.photo}'


class UserPhoto(Base):
    __tablename__ = 'userphoto'

    id = sq.Column(sq.Integer, primary_key=True)
    user_id = sq.Column(sq.Integer, sq.ForeignKey('user.user_id'), nullable=False)
    photo_id = sq.Column(sq.Integer, sq.ForeignKey('photos.photo_id'), nullable=False)

    user = relationship(User, backref='userphoto')
    photos = relationship(Photos, backref='userphoto')

    def __str__(self):
        return f'UserPhoto {self.id} : ({self.user_id}, {self.photo_id})'


def create_tables(engine):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
