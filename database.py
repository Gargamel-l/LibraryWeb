import os
import random
import string
from pickle import FALSE
import psycopg2
from config import host, user, password, db_name, db_name2
from werkzeug.security import generate_password_hash, check_password_hash




try:
    conn = psycopg2.connect(
        user=user,
        password=password,
        host=host,
        database=db_name)

    conn.autocommit = True

    cur = conn.cursor()

    cur.execute('DROP TABLE IF EXISTS users;')
    hash = generate_password_hash('1234')
    print(hash)
    input('next')

    with conn.cursor() as cursor:
        cur.execute(
             """CREATE TABLE users(id serial PRIMARY KEY,
                                 login varchar (150) NOT NULL,
                                 email varchar (150) NOT NULL,
                                 password varchar (800) NOT NULL,
                                 status varchar (150) NOT NULL,
                                 books_id integer NOT NULL,
                                 books_count integer NOT NULL);"""
        )
    

    cur.execute('INSERT INTO users (login, email, password, status, books_id, books_count)'
            'VALUES (%s, %s, %s, %s, %s, %s)',
             ('Anton',
             'anton@yandex.ru',
             'pbkdf2:sha256:260000$gGT19AjqXD37PW2S$93e4ed7b8e2aafea10302da9b6dfa87aa95dd780e81018f6d7e491d4e014ce40',
             'admin',
             '0',
             '0')
            )
    print("[INFO] succses")

    with conn.cursor() as cursor:
        cur.execute('DROP TABLE IF EXISTS top_users;')
        cur.execute(
             """CREATE TABLE top_users(id serial PRIMARY KEY,
                                 login varchar (150) NULL,
                                 place integer NULL,
                                 books_count integer NULL);"""
        )
    cur.execute('DROP TABLE IF EXISTS top_donators;')
    cur.execute(
             """CREATE TABLE top_donators(id serial PRIMARY KEY,
                                 login varchar (150) NULL,
                                 place integer NULL,
                                 donate_count integer NULL);"""
        )
    

except Exception as _ex:
    print("[INFO] Error", _ex)

finally:
        if conn:
            conn.close()
            print()

try:

    conn2 = psycopg2.connect(
        user=user,
        password=password,
        host=host,
        database=db_name2)

    conn2.autocommit = True

    cur = conn2.cursor()


    cur.execute('DROP TABLE IF EXISTS librarys;')
    cur.execute(
        """CREATE TABLE librarys (id serial PRIMARY KEY,
                                 name varchar (150) NOT NULL,
                                 reputation integer NOT NULL,
                                 adress varchar (250) NOT NULL);"""
                )
    cur.execute('INSERT INTO librarys (name, reputation, adress)'
                'VALUES (%s, %s, %s)',
               ('Российская государственная библиотека',
               5,
              'ул. Воздвиженка, 3/5, Москва')
             )
    cur.execute('INSERT INTO librarys (name, reputation, adress)'
                'VALUES (%s, %s, %s)',
               ('Дом Пашкова',
               5,
              'ул. Воздвиженка, 3/5с1, Москва')
             )
    cur.execute('INSERT INTO librarys (name, reputation, adress)'
                'VALUES (%s, %s, %s)',
               ('Библиотека-читальня им. И.С. Тургенева',
               5,
              'Бобров пер., 6, стр. 1, Москва')
             )


    cur.execute('DROP TABLE IF EXISTS books;')
    cur.execute(
        """CREATE TABLE books (id serial PRIMARY KEY,
                                 title varchar (150) NOT NULL,
                                 author varchar (150) NOT NULL,
                                 pages_num varchar (50) NOT NULL,
                                 review text,
                                 date_added date DEFAULT CURRENT_TIMESTAMP);"""
                )
    cur.execute('INSERT INTO books (title, author, pages_num, review)'
                'VALUES (%s, %s, %s, %s)',
               ('A Tale of Two Cities',
                'Charles Dickens',
               489,
              'A great classic!')
             )
    cur.execute('INSERT INTO books (title, author, pages_num, review)'
               'VALUES (%s, %s, %s, %s)',
              ('Anna Karenina',
               'Leo Tolstoy',
              864,
               'Another great classic!')
               )
    cur.execute('INSERT INTO books (title, author, pages_num, review)'
                'VALUES (%s, %s, %s, %s)',
               ('A Tale of Two Cities',
                'Charles Dickens',
               489,
              'A great classic!')
             )
    cur.execute('INSERT INTO books (title, author, pages_num, review)'
               'VALUES (%s, %s, %s, %s)',
              ('Anna Karenina',
               'Leo Tolstoy',
              864,
               'Another great classic!')
               )
    cur.execute('INSERT INTO books (title, author, pages_num, review)'
                'VALUES (%s, %s, %s, %s)',
               ('A Tale of Two Cities',
                'Charles Dickens',
               489,
              'A great classic!')
             )
    cur.execute('INSERT INTO books (title, author, pages_num, review)'
               'VALUES (%s, %s, %s, %s)',
              ('Anna Karenina',
               'Leo Tolstoy',
              864,
               'Another great classic!'))

    cur.execute('INSERT INTO books (title, author, pages_num, review)'
             'VALUES (%s, %s, %s, %s)',
              ('Anna Karenina',
               'Leo Tolstoy',
              864,
               'Another great classic!'))

    def populate_table():
            title = ''.join(random.choice(string.ascii_letters) for _ in range(10))
            author = ''.join(random.choice(string.ascii_letters) for _ in range(10))
            pages_num = str(random.randint(100, 1000))
            review = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(50))

            cur.execute("INSERT INTO books (title, author, pages_num, review) VALUES (%s, %s, %s, %s)",
                    (title, author, pages_num, review))
    for _ in range(500):
        populate_table()
    
    input('next')

    print("[INFO] succsesssssssssssssssssssssss")
    


    ###Russian state library
    cur.execute('DROP TABLE IF EXISTS RSL_BooksHorror;')
    cur.execute(
        """CREATE TABLE RSL_BooksHorror (id serial PRIMARY KEY,
                                 title varchar (150) NOT NULL,
                                 author varchar (150) NOT NULL,
                                 pages_num varchar (50) NOT NULL,
                                 review text,
                                 date_added date DEFAULT CURRENT_TIMESTAMP);"""
                )
    cur.execute('INSERT INTO RSL_BooksHorror (title, author, pages_num, review)'
                'VALUES (%s, %s, %s, %s)',
               ('A Tale of Two Cities',
                'Charles Dickens',
               489,
              'A great classic!')
             )
    cur.execute('INSERT INTO RSL_BooksHorror (title, author, pages_num, review)'
               'VALUES (%s, %s, %s, %s)',
              ('Anna Karenina',
               'Leo Tolstoy',
              864,
               'Another great classic!')
)
    cur.execute('DROP TABLE IF EXISTS RSL_BooksComedy;')
    cur.execute(
        """CREATE TABLE RSL_BooksComedy (id serial PRIMARY KEY,
                                 title varchar (150) NOT NULL,
                                 author varchar (150) NOT NULL,
                                 pages_num varchar (50) NOT NULL,
                                 review text,
                                 date_added date DEFAULT CURRENT_TIMESTAMP);"""
                )
    cur.execute('INSERT INTO RSL_BooksComedy (title, author, pages_num, review)'
                'VALUES (%s, %s, %s, %s)',
               ('A Tale of Two Cities',
                'Charles Dickens',
               489,
              'A great classic!')
             )
    cur.execute('INSERT INTO RSL_BooksComedy (title, author, pages_num, review)'
               'VALUES (%s, %s, %s, %s)',
              ('Anna Karenina',
               'Leo Tolstoy',
              864,
               'Another great classic!')
)
    cur.execute('DROP TABLE IF EXISTS RSL_BooksFantasy;')
    cur.execute(
        """CREATE TABLE RSL_BooksFantasy (id serial PRIMARY KEY,
                                 title varchar (150) NOT NULL,
                                 author varchar (150) NOT NULL,
                                 pages_num varchar (50) NOT NULL,
                                 review text,
                                 date_added date DEFAULT CURRENT_TIMESTAMP);"""
                )
    cur.execute('INSERT INTO RSL_BooksFantasy (title, author, pages_num, review)'
                'VALUES (%s, %s, %s, %s)',
               ('A Tale of Two Cities',
                'Charles Dickens',
               489,
              'A great classic!')
             )
    cur.execute('INSERT INTO RSL_BooksFantasy (title, author, pages_num, review)'
               'VALUES (%s, %s, %s, %s)',
              ('Anna Karenina',
               'Leo Tolstoy',
              864,
               'Another great classic!')
)

    #Peshkov house
    cur.execute('DROP TABLE IF EXISTS PH_BooksHorror;')
    cur.execute(
        """CREATE TABLE PH_BooksHorror (id serial PRIMARY KEY,
                                 title varchar (150) NOT NULL,
                                 author varchar (150) NOT NULL,
                                 pages_num varchar (50) NOT NULL,
                                 review text,
                                 date_added date DEFAULT CURRENT_TIMESTAMP);"""
                )
    cur.execute('INSERT INTO PH_BooksHorror (title, author, pages_num, review)'
                'VALUES (%s, %s, %s, %s)',
               ('A Tale of Two Cities',
                'Charles Dickens',
               489,
              'A great classic!')
             )
    cur.execute('INSERT INTO PH_BooksHorror (title, author, pages_num, review)'
               'VALUES (%s, %s, %s, %s)',
              ('Anna Karenina',
               'Leo Tolstoy',
              864,
               'Another great classic!')
)
    cur.execute('DROP TABLE IF EXISTS PH_BooksComedy;')
    cur.execute(
        """CREATE TABLE PH_BooksComedy (id serial PRIMARY KEY,
                                 title varchar (150) NOT NULL,
                                 author varchar (150) NOT NULL,
                                 pages_num varchar (50) NOT NULL,
                                 review text,
                                 date_added date DEFAULT CURRENT_TIMESTAMP);"""
    )
    cur.execute('INSERT INTO PH_BooksComedy (title, author, pages_num, review)'
                'VALUES (%s, %s, %s, %s)',
               ('A Tale of Two Cities',
                'Charles Dickens',
               489,
              'A great classic!')
             )
    cur.execute('INSERT INTO PH_BooksComedy (title, author, pages_num, review)'
               'VALUES (%s, %s, %s, %s)',
              ('Anna Karenina',
               'Leo Tolstoy',
              864,
               'Another great classic!')
)
    cur.execute('DROP TABLE IF EXISTS PH_BooksFantasy;')
    cur.execute(
        """CREATE TABLE PH_BooksFantasy (id serial PRIMARY KEY,
                                 title varchar (150) NOT NULL,
                                 author varchar (150) NOT NULL,
                                 pages_num varchar (50) NOT NULL,
                                 review text,
                                 date_added date DEFAULT CURRENT_TIMESTAMP);"""
    )
    cur.execute('INSERT INTO PH_BooksFantasy (title, author, pages_num, review)'
                'VALUES (%s, %s, %s, %s)',
               ('A Tale of Two Cities',
                'Charles Dickens',
               489,
              'A great classic!')
             )
    cur.execute('INSERT INTO PH_BooksFantasy (title, author, pages_num, review)'
               'VALUES (%s, %s, %s, %s)',
              ('Anna Karenina',
               'Leo Tolstoy',
              864,
               'Another great classic!')
)

    #Turgeniev library
    cur.execute('DROP TABLE IF EXISTS TL_BooksHorror;')
    cur.execute(
        """CREATE TABLE TL_BooksHorror (id serial PRIMARY KEY,
                                 title varchar (150) NOT NULL,
                                 author varchar (150) NOT NULL,
                                 pages_num varchar (50) NOT NULL,
                                 review text,
                                 date_added date DEFAULT CURRENT_TIMESTAMP);"""
                )
    cur.execute('INSERT INTO TL_BooksHorror (title, author, pages_num, review)'
                'VALUES (%s, %s, %s, %s)',
               ('A Tale of Two Cities',
                'Charles Dickens',
               489,
              'A great classic!')
             )
    cur.execute('INSERT INTO TL_BooksHorror (title, author, pages_num, review)'
               'VALUES (%s, %s, %s, %s)',
              ('Anna Karenina',
               'Leo Tolstoy',
              864,
               'Another great classic!')
)
    cur.execute('DROP TABLE IF EXISTS TL_BooksComedy;')
    cur.execute(
        """CREATE TABLE TL_BooksComedy (id serial PRIMARY KEY,
                                 title varchar (150) NOT NULL,
                                 author varchar (150) NOT NULL,
                                 pages_num varchar (50) NOT NULL,
                                 review text,
                                 date_added date DEFAULT CURRENT_TIMESTAMP);"""
                )
    cur.execute('INSERT INTO TL_BooksComedy (title, author, pages_num, review)'
                'VALUES (%s, %s, %s, %s)',
               ('A Tale of Two Cities',
                'Charles Dickens',
               489,
              'A great classic!')
             )
    cur.execute('INSERT INTO TL_BooksComedy (title, author, pages_num, review)'
               'VALUES (%s, %s, %s, %s)',
              ('Anna Karenina',
               'Leo Tolstoy',
              864,
               'Another great classic!')
)
    cur.execute('DROP TABLE IF EXISTS TL_BooksFantasy;')
    cur.execute(
        """CREATE TABLE TL_BooksFantasy (id serial PRIMARY KEY,
                                 title varchar (150) NOT NULL,
                                 author varchar (150) NOT NULL,
                                 pages_num varchar (50) NOT NULL,
                                 review text,
                                 date_added date DEFAULT CURRENT_TIMESTAMP);"""
            )
    cur.execute('INSERT INTO TL_BooksFantasy (title, author, pages_num, review)'
                'VALUES (%s, %s, %s, %s)',
               ('A Tale of Two Cities',
                'Charles Dickens',
               489,
              'A great classic!')
             )
    cur.execute('INSERT INTO TL_BooksFantasy (title, author, pages_num, review)'
               'VALUES (%s, %s, %s, %s)',
              ('Anna Karenina',
               'Leo Tolstoy',
              864,
               'Another great classic!')
            )

    cur.execute('DROP TABLE IF EXISTS TL_BooksFantasy;')
    print("[INFO] succses")
    
except Exception as _ex1:
    print("[INFO] Error", _ex1)

finally:
        if conn2:
            conn2.close()
            print()
