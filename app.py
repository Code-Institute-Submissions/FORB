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
    return render_template("base.html", books=mongo.db.books.find())








if __name__ == "__main__":
    app.run(host=os.environ.get("IP", "0.0.0.0"), port=int(os.environ.get("PORT", "5000")),debug=False)