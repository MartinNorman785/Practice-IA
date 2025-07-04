from website import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta


class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Integer)
    description = db.Column(db.String(250))
    day = db.Column(db.Date())
    child_id = db.Column(db.Integer, db.ForeignKey('child.id'))

    def setDescription(self, description):
        self.description = description

    def changeValue(self, value):
        self.value = value

    def changeAccount(self, account):
        self.account = account

    def changeDate(self, day):
        self.day = day

    def setDateToday(self):
        self.day = date.now()

    def __str__(self):
        string = self.getStringDay() + ": " + self.getValueString()
        if self.description != "":
            string = string + " " + self.description
        
        return string

    def getValue(self):
        return value

    def getValueString(self):
        dollars = str(abs(self.value) // 100)
        cents = str(abs(self.value) % 100)
        if (self.value < 0):
            return "-$" + dollars + "." + cents
        
        return "$" + dollars + "." + cents
    
    def valueGreaterThan(self, value):
        return (self.value > value)

    def valueLessThan(self, value):
        return (self.value < value)
    
    def valueBetween(selfmin, max):
        return self.valueGreaterThan(min) and self.valueLessThan(max)
    
    def getDay(self, ):
        return self.day
    

    def getStringDay(self):
        return self.day.strftime("%a, %d %b")
    

    def isDate(self, date):
        return (self.day == date)
    

    def dateBefore(self, date):
        return (self.day <  date)
    

    def dateAfter(self, date):
        return (self.day > date)
    

    def dateBetween(self, firstDate, secondDate):
        if (firstDate.isBefore(secondDate)):
            return self.dateAfter(firstDate) and self.dateBefore(secondDate)
        else:
            return self.dateAfter(secondDate) and self.dateBefore(firstDate)
    

    def getDescription(self):
        return self.description