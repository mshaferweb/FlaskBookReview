import os
import requests

from flask import Flask, session, render_template, request
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from werkzeug.security import check_password_hash, generate_password_hash


app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

if not os.getenv("GOOD_READS_KEY"):
    raise RuntimeError("GOOD_READS_KEY is not set")
good_reads_key = os.getenv("GOOD_READS_KEY")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

@app.route("/")
def index():

    try:
        if session['user_id']:
            return render_template("books.html", logged_in=True)
    except:
        return render_template("index.html")


@app.route("/api/<isbn>")
def api(isbn):
    res = requests.get("https://www.goodreads.com/book/review_counts.json",
                       params={"key": good_reads_key, "isbns": isbn})
    return res.json()

@app.route("/login", methods=["POST"])
def login():

    username = request.form['name']
    password = request.form['password']

    user = db.execute("select * from users where username like :username",
               {"username": username}).fetchone()

    if user is None:
        return render_template("error.html", message="invalid username or password")
    if check_password_hash(user.password,password):
        session.clear()
        session['user_id'] = user.username
        return render_template("books.html",logged_in = True)
    else:
        return render_template("error.html",message="invalid username or password")

@app.route("/books", methods=["GET", "POST"])
def books():

    try:
        if session['user_id']:
            logged_in = True
    except:
        return render_template("index.html")

    bookname = request.form['bookname']

    books = db.execute("select * from books where title like :bookname OR author like :bookname or isbn like :bookname",
               {"bookname": '%' + bookname + '%'})

    if books.rowcount == 0:
        return render_template("error.html", message="No book found")
    else:
        return render_template("books.html",books = books)


@app.route("/books/<isbn>")
def book(isbn):
    """Lists details about a single book."""

    try:
        if session['user_id']:
            logged_in = True
    except:
        return render_template("index.html")

    # Make sure book exists.
    book = db.execute("SELECT * FROM books WHERE isbn = :isbn", {"isbn": isbn}).fetchone()
    if book is None:
        return render_template("error.html", message="No such book.")

    book_id = db.execute("select id from books where isbn like :isbn",
                         {"isbn": isbn}).fetchone()

    # Get list of reviews
    ireviews = db.execute("SELECT * FROM reviews WHERE book_id = :book_id", {"book_id": book_id[0]})

    import requests
    res = requests.get("https://www.goodreads.com/book/review_counts.json",
                       params={"key": good_reads_key, "isbns": isbn})

    out = res.json()
    good_reads = out["books"][0]
    return render_template("book.html", book=book, ireviews = ireviews, good_reads = good_reads)


@app.route("/review", methods=["POST"])
def review():
    # username = request.form['name']
    # password = request.form['password']

    try:
        if session['user_id']:
            logged_in = True
    except:
        return render_template("index.html")

    # password_secure = generate_password_hash(password)

    username = request.form['username']
    isbn = request.form['isbn']
    review = request.form['review']
    rating = request.form['rating']

    if review == "":
        return render_template("error.html", message="Review can't be empty")
    elif rating == "":
        return render_template("error.html", message="Rating can't be empty")
    elif int(rating) > 5 or int(rating) < 1:
        return render_template("error.html", message="Rating needs to be between 1 and 5")

    user_id = db.execute("select id from users where username = :username",
               {"username": username}).fetchone()

    book_id = db.execute("select id from books where isbn = :isbn",
                         {"isbn": isbn}).fetchone()


    # app.logger.info(message)
    existing_review_count = db.execute("SELECT count(*) FROM reviews WHERE book_id = :book_id and user_id = :user_id",
                                 {"book_id": book_id[0],"user_id": user_id[0]}).fetchone()

    db.commit()
    if (existing_review_count[0] > 0):
        return render_template("error.html", message="User cant submit two reviews for the same book")

    db.execute("INSERT INTO reviews (user_id, book_id,review,rating) VALUES (:user_id, :book_id, :review,:rating)",
            {"user_id": user_id[0], "book_id": book_id[0], "review":review , "rating":rating})

    book = db.execute("SELECT * FROM books WHERE isbn = :isbn", {"isbn": isbn}).fetchone()
    ireviews = db.execute("SELECT * FROM reviews WHERE book_id = :book_id", {"book_id": book_id[0]})

    db.commit()

    import requests
    key = "47rkiBSFHxWjMgqGv6pd3A"
    res = requests.get("https://www.goodreads.com/book/review_counts.json",
                       params={"key": key, "isbns": isbn})

    out = res.json()
    good_reads = out["books"][0]

    return render_template("book.html", book=book, ireviews = ireviews, good_reads = good_reads)

@app.route("/logout")
def logout():
    session.clear()
    return render_template("index.html", logged_in=False)

@app.route("/register", methods=["POST"])
def register():
    username = request.form['name']
    password = request.form['password']

    password_secure = generate_password_hash(password)

    user = db.execute("select * from users where username like :username",
               {"username": username}).fetchone()
    db.commit()
    if user is not None:
        return render_template("error.html", message="User already exists")

    db.execute("INSERT INTO users (username, password,session_id) VALUES (:username, :password, :session_id)",
            {"username": username, "password": password_secure, "session_id":123123123})
    db.commit()

    return render_template("register.html", name=username, password = password)