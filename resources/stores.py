from flask_restful import Resource
from models.stores import StoreModel

class Store(Resource):
    def get(self, name):
        store = StoreModel.find_by_item_name(name)
        if store:
            return store.json()
        return {"Message" : "Store Not Found"}, 404

    def post(self, name):
        if StoreModel.find_by_item_name(name):
            return {"Message" : "A store with the name '{}' slready exists.".format(name)}, 400

        store = StoreModel(name)
        try:
            store.save_to_db()
        except:
            return {"Message" : "Error on adding store."}, 500

        return store.json()

    def delete(self, name):
        store = StoreModel.find_by_item_name(name)
        if store:
            store.delete_from_db()
        return {"Message" : "Store Remove successfully."}

class StoreList(Resource):
    def get(self):
        stores = StoreModel.query.all()
        return {"stores" : [store.json() for store in stores]}
            