from website import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta


class Goal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Integer)
    name = db.Column(db.String(100))
    description = db.Column(db.String(250))
    dueDate = db.Column(db.Date())
    child_id = db.Column(db.Integer, db.ForeignKey('child.id'))

    def __str__(self):
        string = name
        if (description != ""):
            string = string + " (" + description + "):    "
        else:
            string = string + ":    "
        if (dueDate is not None):
            string = string + self.getStringDate() + "    "
        return string + self.getValueString()
    


    def setDate(self, date):
        self.dueDate = date
    

    def changeValue(self, value):
        self.value = value
    

    def setDescription(self, description):
        self.description = description
    

    def changeName(self, name):
        self.name = name
    

    def getDueDate(self):
        return dueDate
    

    def hasDueDate(self, date):
        if self.dueDate is None:
            return self.dueDate == date
        
        return False
    

    def dueDateBefore(self, date):
        if self.dueDate is not None:
            return self.dueDate < date
        
        return False
    

    def dueDateAfter(self, date):
        if self.dueDate is not None:
            return self.dueDate > date
        
        return False
    

    def dueDateBetween(self, firstDate, secondDate):
        if (self.dueDate is not None):
            if (firstDate.isBefore(secondDate)):
                return self.dueDateAfter(firstDate) and self.dueDateBefore(secondDate)
            else:
                return self.dueDateAfter(secondDate) and self.dueDateBefore(firstDate)
        return False
    

    def getStringDate(self):
        if self.dueDate is None:
            return dueDate.strftime("%a, %d %b")
        
        return ""
    

    def getName(self):
        return name
    

    def isName(self, name):
        return name == self.name
    

    def getDescription(self):
        return description
    

    def getGoalValue(self):
        return value
    

    def getValueString(self):
        dollars = str(abs(self.value) // 100)
        cents = str(abs(self.value) % 100)
        if (self.value < 0):
            return "-$" + dollars + "." + cents
        
        return "$" + dollars + "." + cents
    

    def valueGreaterThan(value):
        return (self.value > value)
    

    def valueLessThan(self, value):
        return (self.value < value)
    
    
    def valueBetween(self, min, max):
        return self.valueGreaterThan(min) and self.valueLessThan(max)