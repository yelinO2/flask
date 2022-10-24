import sqlite3
from flask_jwt import jwt_required
from flask_restful import Resource, reqparse
from flask import Flask, jsonify, request
from models.item import ItemModel


class Item(Resource):
   parser = reqparse.RequestParser()
   parser.add_argument(
    'price',
    type = float,
    required = True,
    help = "This field is required."
   )

   parser.add_argument(
    'name',
    type = str,
    required = True,
    help = "This field is required."
   )

   parser.add_argument(
    'store_id',
    type = int,
    required = True,
    help = "This field can't be empty and every item should have a store_id"
   )


#    @ jwt_required()
   def post(self):

    data = Item.parser.parse_args()
    
    item = ItemModel.find_by_item_name(data['name'])
 
    if item:
        return { "Message" : "Item with this name {} already exists.".format(data['name'])}, 400

    item = ItemModel(data['name'], data['price'], data["store_id"])

    try:
        item.save_to_db()
    except:
        return { "Message" : "An error occured while inserting data."}, 500

    return item.json(), 201
    
    

    # if (ItemModel.find_by_item_name(data['name'])):
    #     return { "Message" : "Item with this name {} already exists.".format(data['name'])}

    # item = {'name' : data ['name'], 'price' : data ['price']}

    # return item, 201
   
#    @ jwt_required()
   def get(self):
        
        data = request.get_json()
        item = ItemModel.find_by_item_name(data['name'])
        
        if item:
            return item.json()
        return {'Message' : 'Item Not Found'}, 401

#    @jwt_required()
   def delete(self):

        data = request.get_json()
        item = ItemModel.find_by_item_name(data['name'])
        if item:
            item.delete_from_db()
        return {"Message" : "Item removed successfully."}, 201

#    @ jwt_required()
   def put(self):
    
    data = Item.parser.parse_args()
    print("<<<<<<<<<<")

    print(data)

    item = ItemModel.find_by_item_name(data['name'])

    print(">>>>>>>>>")

    print(item)
    

    if item is None:
        item = ItemModel(data["name"], data["price"], data["store_id"])
    else:
        item.price = data['price']
             
    item.save_to_db()

    return {"Message" : "update successfully"}


class ItemList(Resource):
    def get(self):
        items = ItemModel.query.all()
        return {"items" : [ item.json() for item in items ]}

   


