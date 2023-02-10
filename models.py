import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship
from config import login, password, db_name

Base = declarative_base()

DSN = f'postgresql://{login}:{password}@localhost:5432/{db_name}'
engine = sq.create_engine(DSN)


class Parameters(Base):
    __tablename__ = 'parameters'

    search_id = sq.Column(sq.Integer, primary_key=True)
    country = sq.Column(sq.String, nullable=False)
    region = sq.Column(sq.String, nullable=False)
    city = sq.Column(sq.String, nullable=False)
    sex = sq.Column(sq.String, nullable=False)
    age_from = sq.Column(sq.String, nullable=False)
    age_to = sq.Column(sq.String, nullable=False)

    def __str__(self):
        return f'User {self.search_id} : ({self.country}, {self.region}, {self.city}, {self.sex}, {self.age_from}, {self.age_to})'


class User(Base):
    __tablename__ = 'user'

    user_id = sq.Column(sq.Integer, primary_key=True)
    first_name = sq.Column(sq.String, nullable=False)
    last_name = sq.Column(sq.String, nullable=False)
    profile_link = sq.Column(sq.String, nullable=False)
    search_id = sq.Column(sq.Integer, sq.ForeignKey('parameters.search_id'), nullable=False)
    selected = sq.Column(sq.Boolean, default=False)

    user = relationship(Parameters, backref='user')

    def __str__(self):
        return f'User {self.user_id} : ({self.first_name}, {self.last_name}, {self.profile_link}, {self.search_id}, {self.selected})'


class Photos(Base):
    __tablename__ = 'photos'

    photo_id = sq.Column(sq.Integer, primary_key=True)
    photo = sq.Column(sq.String, nullable=False)  # Данные о фотографии

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