from website import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta


class Chore(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Integer)
    name = db.Column(db.String(100))
    description = db.Column(db.String(250))
    dueDate = db.Column(db.Date())
    recurring = db.Column(db.String(20))
    mandatory = db.Column(db.Boolean)
    overdue = db.Column(db.Boolean)
    child_id = db.Column(db.Integer, db.ForeignKey('child.id'))

    def __str__(self):
        string = self.name
        if self.description != '':
            string = string + " (" + self.description + ")"

        string = string + ": "
        if self.value > 0:
            string = string + "Earns " + self.getValueString()
        else:
            string = string + "Mandatory"
        if self.dueDate is not None:
            string = string + ", Due By " + self.getStringCompleteByDay() + ""

        if self.recurring != "never":
            string = string + ", Recurrs " + self.recurring
        return string
    
    def changeName(self, name, description):
        self.name = name
        self.description = description
    
    def changeName(self, name):
        self.name = name
    
    def changeDescription(self, description):
        self.description = description
    
    def changeValue(self, value):
        self.value = value
    
    def makeMandatory(self):
        self.value = 0
        self.mandatory = true

    def makeOptional(self, value):
        self.value = value
        self.mandatory = false

    def makeOptional(self):
        self.mandatory = false
    
    def makeOverdue(self):
        self.overdue = true
    
    def makeNotOverdue(self):
        self.overdue = false

    def getCompleteByDay(self):
        return self.dueDate

    def getStringCompleteByDay(self):
        return self.dueDate.strftime("%a, %d %b")
    
    def setCompleteByDate(self):
        if (self.isWeekly()):
            self.dueDate = date.now() + timedelta(days=7)
        elif (self.isDaily()):
            self.dueDate = date.now() + timedelta(days=1)
        elif (self.isMonthly()):
            self.dueDate = date.now() + relativedelta(months=1)
        else:
            self.dueDate = date.now() + timedelta(days=7)
    
    def setCompleteByDate(self, day):
        self.dueDate = day

    def advanceCompleteByDate(self):
        if (self.isWeekly()):
            dueDate = dueDate + timedelta(days=7)
        elif (self.isDaily()):
            dueDate = dueDate + timedelta(days=1)
        elif (self.isMonthly()):
            dueDate = dueDate + relativedelta(months=1)
        
    def checkOverdue(self):
        if dueDate > date.now():
            return True
        else:
            return False

    def hasDueDate(self, date):
        return self.dueDate == date
    

    def dueDateBefore(self, date):
        return self.dueDate < date

    def complete(self, account, day=""):
        if (not self.mandatory):
            account.changeBalance(self.value, self.name + " (" + self.description + ")", day)
        else:
            account.makeChoreNonOverdue(self)
        
        if (self.doesntRecurre()):
            account.removeChore(self)
        else:
            self.advanceCompleteByDate()

    def getName(self, ):
        return self.name
    
    def getDescription(self, ):
        return self.description
    
    def isMandatory(self, ):
        return self.mandatory
    
    def getMandatory(self, ):
        if (self.mandatory):
            return "Mandatory"
        else:
            return "Optional"
        
    def isWeekly(self):
        return self.recurring == "weekly"

    def isMonthly(self):
        return self.recurring == "monthly"
    
    def isDaily(self):
        return self.recurring == "daily"
    
    def doesntRecurre(self):
        return self.recurring == "never"

    def getRecurring(self):
        return self.recurring

    def completionValue(self):
        return self.value

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
    
    def valueBetween(self, min, max):
        return self.value > min and self.value < max


