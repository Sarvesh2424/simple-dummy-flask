from flask import Flask, request
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient("mongodb+srv://10650sarvesh_db_user:samp24@cluster0.xvaqyve.mongodb.net/?appName=Cluster0")
db = client["userpost"]
usercollection = db["userpost"]
postcollection = db["posts"]
commentcollection = db["comments"]


@app.route("/")
def hello_world():
    return "Hello, World, good morning"


@app.route("/add_post", methods=["POST"])
def add_post():
    data = request.json
    new_post = {
        "user": data["user"],
        "title": data["title"],
        "content": data["content"],
    }
    postcollection.insert_one(new_post)
    return "Post added successfully", 201

@app.route("/get_posts", methods=["GET"])
def get_posts():
    posts = list(postcollection.find({}, {"_id": 0}))
    return {"posts": posts}, 200

@app.route("/update_post/<post_id>", methods=["PUT"])
def update_post(post_id):
    data = request.json
    postcollection.update_one(
        {"_id": post_id}, {"$set": {"title": data["title"], "content": data["content"]}}
    )
    return "Post updated successfully", 200


@app.route("/add_comment", methods=["POST"])
def add_comment():
    data = request.json
    if len(data["comment"]) > 300:
        return "Comment exceeds 300 characters limit", 400
    if len(data["comment"]) < 0:
        return "Comment cannot be empty", 400
    new_comment = {
        "user": data["user"],
        "post": data["post"],
        "comment": data["comment"],
    }
    commentcollection.insert_one(new_comment)
    return "Comment added successfully", 200


if __name__ == "__main__":
    app.run(debug=True)
