import sqlite3
from flask import Flask, jsonify, request
from flask_restful import Resource, Api
from flask_jwt import JWT
from security import authenticate, identity

app = Flask(__name__)

app.secret_key = 'my-gf-is-my-life'

api = Api(app)

jwt = JWT(app, authenticate, identity)




users = [
    {
        "userid": "001",
        "password": "password001",
        "role": "admin"
    },
    {
        "userid": "002",
        "password": "password001",
        "role": "user"
    },
]

stores = [
    {
        "name": "Apple",
        "items": [
            {
                "name": "iphone13",
                "price": 1299.99
            }
        ]
    },
    {
        "name": "Microsoft",
        "items": [
            {
                "name": "SurfacePro",
                "price": 1399.99
            }
        ]
    },
]


class User(Resource):
    def get(self):
        return {"users": users}

    def post(self):
        added_user = request.get_json()
        new_user = {
            "userid": added_user["userid"],
            "password": added_user["password"],
            "role": added_user["role"]
        }
        if added_user == {} or added_user["userid"] == "" or added_user["password"] == "" or added_user["role"] == "":
            return {"Message": "Fields can't be empty"}
        users.append(new_user)
        return {"new_user": new_user}


class StoreList(Resource):
    def get(self):
        return {"all_stores": stores}, 200

    def post(self):
        req = request.get_json()
        user_id = req["user_id"]
        new_store = {
            "name": req["name"],
            "items": req["items"]
        }
        # print(user_id)
        for user in users:
            # print(user["userid"])
            # print(user['role'])
            if user_id == user['userid']:
                if user["role"] == "admin":        
                    if req == {} or req["name"] == "" or req["items"] == "":
                        return {"Message " : "Fields can't be empty"}
                    for store in stores:
                        if req['name'] == store['name']:
                            return {"Message": "Store already exist"}
                    
                    stores.append(new_store)
                    return {"added_store": new_store}
                return {"Message":"Unauthourized"}
        return {"message" : "User doesn't exist."}

    def delete(self):
        req = request.get_json()
        store_to_remove = req['store']
        userid = req['userid']
        for user in users:
            if userid == user['userid']:
                if user['role'] == 'admin':
                    for store in stores:
                        if store_to_remove == store['name']:
                            to_remove = {'name' : store['name'], 'items' : store['items']}
                            stores.remove(to_remove)
                            return {'message': f'{store_to_remove} have been removed.'}
                    return{'Message' : 'Store not found'}
                return {"Message": "Unauthourized"}
        return {'Message': "User Not found"}
    


class Store(Resource):
    def get(self):

        req = request.get_json()

        req_store = req['store_name']

        for store in stores:
            if req_store == store['name']:
                print(req_store)
                return {"store": store}
        return {'Message': 'Not found'}

    def post(self):
        req = request.get_json()
        req_store = req['store_name']
        item_to_create = req["items"]
        for store in stores:
            if req_store == store['name']:
                store["items"].append(item_to_create)
                return {"new_item": item_to_create}





class Item(Resource):
    def get(self):
        req = request.get_json()
        req_store = req['store_name']
        req_item = req['item_name']
        for store in stores:
            if req_store == store['name']:
                for item in store['items']:
                    if req_item == item['name']:
                        return {'item': item}, 200
                return {'Message': f'{req_item} not found'}, 401
        return {'Message': f'{req_store} not found'}, 401

class ItemsByName(Resource):
    def get(self):
        req = request.get_json()
        req_item = req['name']
        for store in stores:
            for item in store['items']:
                if req_item == item['name']:
                    return {'item': item}, 200
            
        return {"Message": f"{req_item} not found"}

    def delete(self):
        req = request.get_json()
        req_item = req['name']
        for store in stores:
            for items in store["items"]:
                if req_item == items['name']:
                    item_to_remove = {'name': items['name'], 'price': items['price']}
                    store['items'].remove(item_to_remove)
                    return {'Message': f'{req_item} have been removed'}
        return {'Message': f'{req_item} is not found'}

class UserRegister(Resource):
    def post(self):
        data = request.get_json()
        
        connection = sqlite3.connect("mydatabase.db")
        cursor = connection.cursor()

        query = "INSERT INTO users VALUES (null, ?, ?)"
        cursor.execute(query, (data['username'], data['password']))

        connection.commit()
        connection.close()
        return {"Message": "User created successfully"}

api.add_resource(User, '/users') # get and update user list
api.add_resource(StoreList, '/stores') # get and edit store list
api.add_resource(Store, '/stores/') # add item to store
api.add_resource(Item, '/stores/item') # search store and item
api.add_resource(ItemsByName, '/items') # search by item name and remove item
api.add_resource(UserRegister, '/register')

app.run(debug=True)
