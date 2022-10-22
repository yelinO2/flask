import sqlite3
from flask_restful import Resource, reqparse
from models.user import UserModel

class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'username',
        type = str,
        required = True,
        help = "This field can't be empty"
    )

    parser.add_argument(
        'password',
        type = str,
        required = True,
        help = "This field can't be empty"
    )

    def post(self):
        data = UserRegister.parser.parse_args()
        
        if (UserModel.find_by_username(data['username'])):
            return {"Message" : "A user with this username already exists."}, 400

        user = UserModel(data['username'], data['password'])
        user.save_to_db()

        return {"Message": "User created successfully."}, 201

        # connection = sqlite3.connect('mydatabase.db')
        # cursor = connection.cursor()

        # query = "INSERT INTO users VALUES (null, ?, ?)"
        # cursor.execute(query, (data['username'], data['password']))

        # connection.commit()
        # connection.close()

        # return {"Message" : "User created successfully."}, 201


