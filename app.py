
from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from resources.stores import Store, StoreList
from resources.user import UserRegister
from security import authenticate, identity
from resources.item import Item,ItemList

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///mydatabase.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 

# app.config['SQLALCHEMY_DATABASE_URI'] = "mysql:///username:password@server/dbname"

api = Api(app)
app.secret_key = 'my-gf-is-my-life'
jwt = JWT(app, authenticate, identity)

@app.before_first_request
def create_table():
    db.create_all()

api.add_resource(UserRegister, '/register')
api.add_resource(Item, '/item')
api.add_resource(ItemList, '/items/list_all')
api.add_resource(StoreList, '/stores')
api.add_resource(Store, '/stores/<string:name>')





if __name__ == "__main__":

    from db import db
    db.init_app(app)

    app.run(debug=True)