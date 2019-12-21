import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)

app.config["MONGO_DBNAME"] = "ror-book"
app.config["MONGO_URI"] = "mongodb+srv://task_manager_by_rawa:Script9090@myfirstcluster-2baum.mongodb.net/ror-book?retryWrites=true&w=majority"

mongo = PyMongo(app)

@app.route("/")
@app.route("/get_books")
def get_books():
    return render_template("base.html", books=list(mongo.db.books.find()), genre=list(mongo.db.genre.find()))


@app.route("/add_book")
def add_book():
    
    return render_template("add_book.html", genre=list(mongo.db.genre.find()), books=mongo.db.books.find())    
    
@app.route("/insert_book", methods=["POST"])
def insert_book():
    books = mongo.db.books
    books.insert_one(request.form.to_dict(flat=False))
    
    return redirect(url_for('get_books'))


@app.route('/add_review/<book_id>')
def add_review(book_id):
    currentReview =  mongo.db.books.find_one({"_id": ObjectId(book_id)})
    return render_template('add_review.html', book=currentReview, genre=list(mongo.db.genre.find()))

@app.route('/insert_review/<book_id>', methods=["POST"])
def insert_review(book_id):
    book = mongo.db.books
    book.insert_one( {"reviews":"revrev"},{'_id'== ObjectId(book_id)})
    return redirect(url_for('get_books'))




if __name__ == "__main__":
    app.run(host=os.environ.get("IP", "0.0.0.0"), port=int(os.environ.get("PORT", "3000")),debug=True)