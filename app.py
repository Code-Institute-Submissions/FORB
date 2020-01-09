import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)

app.config["MONGO_DBNAME"] = "ror-book"
app.config["MONGO_URI"] = os.getenv("MONGO_URI")

mongo = PyMongo(app)

# presenting the books on firstpage
@app.route("/")
@app.route("/get_books")
def get_books():
    return render_template("base.html", books=list(mongo.db.books.find()), genre=list(mongo.db.genre.find()))

# redirecting to add-book form
@app.route("/add_book")
def add_book():
    
    return render_template("add_book.html", genre=list(mongo.db.genre.find()), books=mongo.db.books.find())    

#book-form handler    
@app.route("/insert_book", methods=["POST"])
def insert_book():
    books = mongo.db.books
    books.insert_one({
        'title': request.form.get('title').upper(),
        'author': request.form.get('author').upper(),
        'published': request.form.get('published'),
        'genre':request.form.getlist('genre'),
        'image_link': request.form.get('cover')})
    
    return redirect(url_for('get_books'))

#redirecting to selected book page
@app.route('/add_review/<book_id>')
def add_review(book_id):
    currentReview =  mongo.db.books.find_one({"_id": ObjectId(book_id)})
    return render_template('add_review.html', book=currentReview, genre=list(mongo.db.genre.find()))

#inserting review
@app.route('/insert_review/<book_id>', methods=["POST"])
def insert_review(book_id):
    book = mongo.db.books
    
    book.update_one({'_id': ObjectId(book_id)}, {'$push':{
            'reviews':request.form.get("reviews")
            }
        })
        

        
    return add_review(book_id)

#deleting book selected by id
@app.route('/delete_book/<book_id>')
def delete_book(book_id):
    mongo.db.books.remove({'_id':ObjectId(book_id)})
    return redirect(url_for('get_books'))
        

        
    
if __name__ == "__main__":
    app.run(host=os.environ.get("IP", "0.0.0.0"), port=int(os.environ.get("PORT", "3000")),debug=False)