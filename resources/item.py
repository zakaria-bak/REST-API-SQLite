import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

# create an Item Resource containt get & post requests
class Item(Resource):

    #creating a parser to allow just some element to be passed in
    parser = reqparse.RequestParser()  # every item must have a price
    parser.add_argument('price',
            type = float,
            required = True,
            help = "this field cannot be left blank")

    @jwt_required()
    def get(self, name): # get item by name
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        else:
            return {"message" : 'item no found'}, 404

    def post(self, name): # post to add an item to the list
    
        if ItemModel.find_by_name(name):
            return {"message" : f'An Item with name {name} is already exists'}

        data = Item.parser.parse_args()
        item = ItemModel(name, data['price'])
        #item = {'name' : name, 'price' : data['price']}

        try:
            item.insert()
            return item.json()
        except:
            return {"message" : "An error occured inserting the item"}, 500

    def delete(self, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "DELETE FROM items WHERE name=?"
        cursor.execute(query, (name,))

        connection.commit()
        connection.close()

        return {"message" : "item deleted"}

    def put(self, name):
        data = ItemModel.parser.parse_args()

        item = ItemModel.find_by_name(name)
        updated_item = ItemModel(name, data['price'])
        
        if item:
            try:
                updated_item.update()
            except:
                return {"message" : 'A error occured updating the item'}, 500
        else:
            try:
                updated_item.insert()
            except:
                return {"message" : "An error occured insertig the item"}, 500

        return updated_item.json()

# create an Itemlist
class Itemlist(Resource):
    def get(self): # get all items 
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * from items"
        result = cursor.execute(query)

        items = []
        for row in result:
            items.append({'name' : row[0], 'price' : row[1]})

        connection.close()
        return {'items' : items}