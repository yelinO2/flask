
from db import db

class ItemModel(db.Model):

    __tablename__ = "items"
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String)
    price = db.Column(db.Float(precision=3))

    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))
    store = db.relationship('StoreModel')

    def __init__(self, name, price, store_id):
        self.name = name 
        self.price = price
        self.store_id = store_id

    def json(self):
        return { 'name' : self.name, 'price' : self.price, 'store_id' : self.store_id}

    @classmethod
    def find_by_item_name(cls, name):
        return cls.query.filter_by(name=name).first()

        # connection = sqlite3.connect('mydatabase.db')
        # cursor = connection.cursor()

        # query = "SELECT * FROM items where name=?"
        # result = cursor.execute(query, (name, ))
        # row = result.fetchone()
        # connection.close()

        # if row: 
        #     return cls(*row)

    
    # def insert(self):

    #     db.session.add(self)
    #     db.session.commit()

        # connection = sqlite3.connect('mydatabase.db')
        # cursor = connection.cursor()

        # query = "INSERT INTO items VALUES(?, ?)"
        # cursor.execute(query, (self.name, self.price))

        # connection.commit()
        # connection.close()


    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    # def update(self):
    #     connection = sqlite3.connect('mydatabase.db')
    #     cursor = connection.cursor()

    #     query = "UPDATE items SET price = ? WHERE name = ?"
    #     cursor.execute(query, (self.name, self.price))

    #     connection.commit()
    #     connection.close()
