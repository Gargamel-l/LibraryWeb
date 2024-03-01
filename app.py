from calendar import c
import os
import psycopg2
from psycopg2.extensions import register_type, new_array_type
from flask import Flask, render_template, request, url_for, redirect, flash, session
from config import host, user, password, db_name, db_name2
import re 
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'A.S.Belyaev BSBO-07-20'

def get_db_connection():
    conn = psycopg2.connect(
        user=user,
        password=password,
        host=host,
        database=db_name
        )
    return conn

def get_db_connection2():
    conn2 = psycopg2.connect(
        user=user,
        password=password,
        host=host,
        database=db_name2
        )
    return conn2

@app.route("/")
def index():
    if 'loggedin' in session:
        return render_template('profile.html', username=session['login'])
    return render_template('index.html')

@app.route('/showSignUp')
def showSignUp():
    return render_template('auth.html')

@app.route('/profile')
def profile():
    user_id = session['id'];
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM users WHERE id = %s', (user_id,))
    users = cur.fetchone()
    cur.execute('SELECT books_id FROM users WHERE id = %s', (user_id,))
    myBook = cur.fetchone()
    cur.close()
    conn.close()
    if int(myBook[0]) > 0:
            conn2 = get_db_connection2()
            cur = conn2.cursor()
            cur.execute('SELECT * FROM books WHERE id = %s', (myBook,))
            books = cur.fetchone()
            cur.close()
            conn2.close()
            return render_template('profile.html', show_hidden=True, users = users, books = books)
    else:
            return render_template('profile.html', show_hidden=False, users = users)


@app.route('/signUp',methods=['GET', 'POST'])
def signUp():
    if request.method == 'POST':
        login = request.form['login']
        email = request.form['email']
        password = request.form['password']
        _hashed_password = generate_password_hash(password)
            
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute('SELECT * FROM users WHERE login = %s', (login,))
        account = cur.fetchone() 
        if account:
            flash('Аккаунт уже существует!')
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            flash('Недопустимый адрес электронной почты!')
        elif not re.match(r'[A-Za-z0-9]+', login):
            flash('Логин может содержать только буквы и цифры')
        elif not login or not password or not email:
            flash('Заполните форму!')
        else:
            cur.execute('INSERT INTO users (login, email, password,status,books_id,books_count)'
                        'VALUES (%s, %s, %s, %s, %s, %s)',
                        (login, email, _hashed_password, 'Читатель', 0, 0))
            cur.execute('SELECT * FROM users WHERE login = %s', (login,))
            account = cur.fetchone() 
            session['loggedin'] = True
            session['id'] = account[0]
            session['login'] = account[1]
            conn.commit()
            cur.close()
            conn.close()
            return redirect(url_for('profile'))
    return render_template('auth.html')

@app.route('/login',methods=['GET', 'POST'])
def login():
    if request.method == 'POST' and 'login' in request.form and 'password' in request.form:
        login = request.form['login']
        password = request.form['password']
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT * FROM users WHERE login = %s', (login,))
        account = cur.fetchone() 
  
        
        if account:
            password_rs = account[3]
            if check_password_hash(password_rs, password):
                session['loggedin'] = True
                session['id'] = account[0]
                session['login'] = account[1]
                return redirect(url_for('profile'))
            else:
                flash('inncorrect password')
        else:
            flash('inncorrect username')
    
        conn.commit()
        cur.close()
        conn.close()
    return render_template('login.html')

@app.route('/logout')
def logout():
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   return redirect(url_for('index'))

@app.route('/donation/', methods=('GET', 'POST'))
def donation():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        pages_num = int(request.form['pages_num'])
        review = request.form['review']

        conn2 = get_db_connection2()
        cur = conn2.cursor()
        cur.execute('INSERT INTO books (title, author, pages_num, review)'
                    'VALUES (%s, %s, %s, %s)',
                    (title, author, pages_num, review))
        conn2.commit()
        cur.close()
        conn2.close()

        user_id = session['id'];
        new_status = 'Щедрая душа';
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('UPDATE users set status = %s WHERE id = %s', (new_status ,user_id),)
        conn.commit()
        cur.close()
        conn.close()

        return redirect(url_for('showcaseBooks'))
    return render_template('donation.html')

@app.route("/addToList", methods=('GET', 'POST'))
def addToList():

    if request.method == 'POST':
        user_id = session['id'];
        books_id = request.form['book_id']
        books_genre = request.form['book_id']
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('UPDATE users set books_id = %s WHERE id = %s', (books_id ,user_id),)
        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for('profile'))
    return render_template('showcaseBooks.html')

@app.route("/readenBooks")
def readenBooks():
        user_id = session['id'];
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT books_count FROM users WHERE id = %s', (user_id,))
        books_count = cur.fetchone()
        cur.execute('SELECT books_id FROM users WHERE id = %s', (user_id,))
        readenBook_id = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()
        if int(books_count[0]) > 0:
            conn2 = get_db_connection2()
            cur = conn2.cursor()
            cur.execute('SELECT * FROM books WHERE id = %s', (readenBook_id,))
            books = cur.fetchone()
            cur.close()
            conn2.close()
            return render_template('readenBooks.html', show_hidden=True,  books = books, books_count = books_count)
        else:
            return render_template('readenBooks.html', show_hidden=False)
        return render_template('readenBooks.html')

@app.route("/passTheBook")
def passTheBook():
        user_id = session['id'];
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT books_id FROM users WHERE id = %s', (user_id,))
        readenBook_id = cur.fetchone()
        if int(readenBook_id[0]) > 0:
            cur.execute('UPDATE users set books_count = books_count + 1 WHERE id = %s', (user_id,))
            cur.execute('UPDATE users set books_id = %s WHERE id = %s', (0,user_id),)
        cur.execute('SELECT books_count FROM users WHERE id = %s', (user_id,))
        books_count = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()
        conn2 = get_db_connection2()
        cur = conn2.cursor()
        cur.execute('SELECT * FROM books WHERE id = %s', (readenBook_id,))
        books = cur.fetchone()
        cur.close()
        conn2.close()
        if int(books_count[0]) > 0:
            return render_template('readenBooks.html', show_hidden=True,  books = books, books_count = books_count)
        else:
            return render_template('readenBooks.html', show_hidden=False)


@app.route("/chooseLibrary")
def chooseLibrary():
    conn2 = get_db_connection2()
    cur = conn2.cursor()
    cur.execute('SELECT * FROM librarys')
    librarys = cur.fetchall()
    cur.close()
    conn2.close()
    return render_template('chooseLibrary.html', librarys = librarys)

@app.route('/showcaseBooks')
def showcaseBooks():
    conn2 = get_db_connection2()
    cur = conn2.cursor()
    cur.execute('SELECT * FROM books')
    books = cur.fetchall()
    cur.close()
    conn2.close()
    return render_template('showcaseBooks.html', books=books)

@app.route('/RSL_Books')
def RSL_Books():
    conn2 = get_db_connection2()
    cur = conn2.cursor()
    cur.execute('SELECT * FROM rsl_bookscomedy')
    book_comedy = cur.fetchall()
    cur.execute('SELECT * FROM rsl_bookshorror')
    book_horror = cur.fetchall()
    cur.execute('SELECT * FROM rsl_booksfantasy')
    book_fantasy = cur.fetchall()
    cur.close()
    conn2.close()
    return render_template('RSL_Books.html', book_comedy=book_comedy, book_horror=book_horror, book_fantasy=book_fantasy)

if __name__ == '__main__':
    app.run(debug=True)

