from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, Itemlist

app = Flask(__name__)
app.secret_key = 'aheafaenf'
api = Api(app)

#create an end point (/auth)
jwt = JWT(app, authenticate, identity) # /auth


#adding the Item & Itemlist Resources
api.add_resource(Item, '/item/<string:name>')
api.add_resource(Itemlist, "/items")
api.add_resource(UserRegister, '/register')


if __name__ == "__main__":
    
    app.run(debug=True)
