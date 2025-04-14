# models.py
from extensions import db
from sqlalchemy import Column, Integer, Float, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.schema import Table
from sqlalchemy.sql.expression import quoted_name

class Catalogue(db.Model):
    __tablename__ = 'Catalogue'
    CatName = db.Column(db.String, primary_key=True)
    CID = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<Catalogue {self.CatName}>'

class CustomerAcct(db.Model):
    __tablename__ = 'CustomerAcct'
    CID = db.Column(db.Integer, primary_key=True)
    GID = db.Column(db.Integer, nullable=False)
    SalesRep = db.Column(db.String, nullable=False)
    DefaultShip = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f'<CustomerAcct {self.CID}>'

class Item(db.Model):
    __tablename__ = 'Item'
    IID = db.Column(db.Integer, primary_key=True)
    CatName = db.Column(db.String, db.ForeignKey('Catalogue.CatName'))
    PID = db.Column(db.Integer, nullable=False)
    SID = db.Column(db.Integer, nullable=False)
    ItemName = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f'<Item {self.ItemName}>'

class Order(db.Model):
    __tablename__ = 'Order'  # 👈 escape the table name
    OID = db.Column(db.Integer, primary_key=True)
    CID = db.Column(db.Integer, nullable=False)
    GID = db.Column(db.Integer, nullable=False)
    UID = db.Column(db.Integer, nullable=False)
    Date = db.Column(db.String, nullable=False)
    TotalCost = db.Column(db.Float, nullable=False)
    TotalShipping = db.Column(db.Float, nullable=False)
    ShippingAdr = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f'<Order {self.OID}>'

class Product(db.Model):
    __tablename__ = 'Product'
    PID = db.Column(db.Integer, primary_key=True)
    PDesc = db.Column(db.String, nullable=False)
    Type = db.Column(db.String, nullable=False)
    Price = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f'<Product {self.PDesc}>'

class User(db.Model):
    __tablename__ = 'User'
    UID = db.Column(db.Integer, primary_key=True)
    CID = db.Column(db.Integer, nullable=False)
    Name = db.Column(db.String, nullable=False)
    Email = db.Column(db.String, nullable=False)
    AccessLv = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<User {self.Name}>'
