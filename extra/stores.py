from flask import Flask, jsonify, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

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


class StoreList(Resource):
    def get(self):
        return {"all_stores": stores} , 200

    def post(self):
        store_to_create = request.get_json()
        new_store = {
            "name": store_to_create["name"],
            "items": store_to_create["items"]
        }
        stores.append(new_store)
        return {"added_store" : new_store}

    def delete(self):
        req = request.get_json()
        store_to_remove = req['store']
        for store in stores:
            if store_to_remove == store['name']:
                to_remove = {'name' : store['name'], 'items' : store['items']}
                stores.remove(to_remove)
                return {'message': f'{store_to_remove} have been removed.'}
        return{'Message' : 'Store not found'}

class Store(Resource):

    def get(self):
        req = request.get_json()
        req_store = req['store_name']
        for store in stores:
            if req_store == store['name']:
                
                return {"store": store}
        return {'Message': 'Not found'}

    def post(self):
        req = request.get_json()
        req_store = req['store_name']
        item_to_create = req["items"]
        for store in stores:
            if req_store == store['name']:
                store["items"].append(item_to_create)
                return{"new_item": item_to_create}

    




class Item(Resource):
    def get(self):
        req = request.get_json()
        req_store = req['store_name']
        req_item = req['item_name']
        for store in stores:
            if req_store == store['name']:
                for item in store['items']:
                    if req_item == item['name']:
                        return {'item' : item} , 200
                return {'Message': f'{req_item} not found'} , 401
        return {'Message': f'{req_store} not found'} , 401

api.add_resource(StoreList, '/stores')
api.add_resource(Store, '/stores/')
api.add_resource(Item, '/stores/item')

app.run(debug=True)
