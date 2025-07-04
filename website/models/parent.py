from website import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta

class Parent(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    parentAccess = db.Column(db.Boolean, default=True)
    name = db.Column(db.String(150))
    password = db.Column(db.String(150))
    children = db.relationship('Child')

    def getName(self):
        return name

    def getChild(self, name):
        for child in self.children:
            if child.getName() == name:
                return child
        return None 

    def getChildren(self):
        return self.children
    
    def addChild(self, child):
        self.children.append(child)

    def removeChild(self, child):
        try:
            self.children.remove(child)
        finally:
            return None
