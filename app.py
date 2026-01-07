from flask import Flask, request
from config import Config
from extensions import db

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

from models import User   

@app.route("/")
def home():
    return {"message": "Flask CRUD API Running"}


@app.route("/users", methods=["POST"])
def create_user():
    data = request.json
    user = User(name=data["name"], email=data["email"])
    db.session.add(user)
    db.session.commit()
    return {"message": "User created"}


@app.route("/users", methods=["GET"])
def get_users():
    users = User.query.all()
    return [user.to_dict() for user in users]


@app.route("/users/<int:id>", methods=["GET"])
def get_user(id):
    user = User.query.get_or_404(id)
    return user.to_dict()


@app.route("/users/<int:id>", methods=["PUT"])
def update_user(id):
    user = User.query.get_or_404(id)
    data = request.json
    user.name = data["name"]
    user.email = data["email"]
    db.session.commit()
    return {"message": "User updated"}


@app.route("/users/<int:id>", methods=["DELETE"])
def delete_user(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return {"message": "User deleted"}


if __name__ == "__main__":
    app.run(debug=True)
