import sqlalchemy
from sqlalchemy.orm import sessionmaker
from models import create_tables, User, Photos, UserPhoto, Parameters
import psycopg2
from config import login, password, db_name


DSN = f'postgresql://{login}:{password}@localhost:5432/{db_name}'
engine = sqlalchemy.create_engine(DSN)
create_tables(engine)

Session = sessionmaker(bind=engine)
session = Session()


# Заполнение таблицы Parameters
def fill_params(country, region, city, sex, age_from, age_to):
    params_line = Parameters(country=country, region=region, city=city, sex=sex, age_from=age_from, age_to=age_to)
    session.add(params_line)
    session.commit()
    id_search = params_line.search_id
    return id_search


# Заполнение таблицы User
def fill_user_info(first_name, last_name, profile_link, search_id):
    user1 = User(first_name=first_name, last_name=last_name, profile_link=profile_link, search_id=search_id)
    session.add(user1)
    session.commit()
    id_u = user1.user_id
    return id_u


# Заполнение таблиц Photos и UserPhoto
def fill_photo_info(photo, id_u):
    photo1 = Photos(photo=photo)
    session.add(photo1)
    session.commit()
    id_f1 = photo1.photo_id

    userphoto1 = UserPhoto(user_id=id_u, photo_id=id_f1)
    session.add(userphoto1)
    session.commit()


session.close()

conn = psycopg2.connect(database=db_name, user=login, password=password)


# Добавление в избранное
def add_to_selected(user_id):
    with conn.cursor() as cur:
        cur.execute('''
        UPDATE "user" SET selected=%s WHERE "user".user_id = %s;
        ''', (True, user_id))
        conn.commit()


# Вывести список избранных
def print_selected_list(search_id):
    with conn.cursor() as cur:
        cur.execute('''
            SELECT u.first_name, u.last_name, u.profile_link FROM "user" u
            JOIN "parameters" p ON u.search_id=p.search_id
            WHERE selected = %s AND p.search_id = %s;
            ''', (True, search_id))
        us_list = cur.fetchall()
        return us_list