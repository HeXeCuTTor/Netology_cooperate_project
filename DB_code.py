import sqlalchemy
from sqlalchemy.orm import sessionmaker
from models import create_tables, User, Photos, UserPhoto
import json
import psycopg2
from config import login, password, db_name


DSN = f'postgresql://{login}:{password}@localhost:5432/{db_name}'
engine = sqlalchemy.create_engine(DSN)

Session = sessionmaker(bind=engine)
session = Session()


def fill_DB():
    create_tables(engine)
    with open('database.json', 'r', encoding='utf8') as f:
        data = json.load(f)

    for record in data:
        first_name = record['first_name']
        last_name = record['last_name']
        profile_link = f"https://vk.com/id{record['user_id']}"
        user1 = User(first_name=first_name, last_name=last_name, profile_link=profile_link)
        session.add(user1)
        session.commit()
        id_u = user1.user_id

        if 'photo_id 1' in record:
            photo1 = Photos(photo=f"photo{record['user_id']}_{record['photo_id 1']}")
            session.add(photo1)
            session.commit()
            id_f1 = photo1.photo_id

            userphoto1 = UserPhoto(user_id=id_u, photo_id=id_f1)
            session.add(userphoto1)
            session.commit()

        if 'photo_id 2' in record:
            photo2 = Photos(photo=f"photo{record['user_id']}_{record['photo_id 2']}")
            session.add(photo2)
            session.commit()
            id_f2 = photo2.photo_id

            userphoto1 = UserPhoto(user_id=id_u, photo_id=id_f2)
            session.add(userphoto1)
            session.commit()

        if 'photo_id 3' in record:
            photo3 = Photos(photo=f"photo{record['user_id']}_{record['photo_id 3']}")
            session.add(photo3)
            session.commit()
            id_f3 = photo3.photo_id

            userphoto1 = UserPhoto(user_id=id_u, photo_id=id_f3)
            session.add(userphoto1)
            session.commit()
    print('БД заполнена')



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
def print_selected_list():
    with conn.cursor() as cur:
        cur.execute('''
            SELECT first_name, last_name, profile_link FROM "user" WHERE selected = %s;
            ''', (True,))
        us_list = cur.fetchall()
        return us_list


# Вывести фотки из БД
def print_photos(profile_link):
    with conn.cursor() as cur:
        cur.execute('''
            SELECT f.photo FROM "photos" f 
            JOIN "userphoto" up ON f.photo_id=up.photo_id
            JOIN "user" u ON up.user_id=u.user_id
            WHERE u.profile_link = %s;
            ''', (profile_link,))
        f_list = cur.fetchall()
        return f_list


# Вывод людей из БД
def print_man(man_id):
    with conn.cursor() as cur:
        cur.execute('''
            SELECT first_name, last_name, profile_link FROM "user" WHERE user_id = %s;
            ''', (man_id,))
        return cur.fetchone()
