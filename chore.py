from datetime import date, timedelta
from dateutil.relativedelta import relativedelta

class Chore(db.Model, UserMixin):
    def __init__(self, name, description, value=0, recurring="none"):
        self.name = name
        self.value = value
        self.recurring = recurring
        self.description = description

        if value == 0:
            mandatory = True
        else:
            mandatory = False
            
        overdue = False
    
    def __str__(self):
        string = self.name
        if self.description != '':
            string = string + " (" + description + ")"

        string = string + ": "
        if self.value > 0:
            string = string + "Earns " + self.completionValueString()
        else:
            string = string + "Mandatory"

        string = string + ", Due By " + self.getStringCompleteByDay() + "\n   "

        if self.recurring != "never":
            string = string + "Recurrs " + self.recurring
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
        return self.complete_by_date

    def getStringCompleteByDay(self):
        return self.complete_by_date.strftime("%a, %d %b")
    
    def setCompleteByDate(self):
        if (self.isWeekly()):
            self.complete_by_date = date.now() + timedelta(days=7)
        elif (self.isDaily()):
            self.complete_by_date = date.now() + timedelta(days=1)
        elif (self.isMonthly()):
            self.complete_by_date = date.now() + relativedelta(months=1)
        else:
            self.complete_by_date = date.now() + timedelta(days=7)
    
    def setCompleteByDate(self, day):
        self.complete_by_date = day

    def advanceCompleteByDate(self):
        if (self.isWeekly()):
            complete_by_date = complete_by_date + timedelta(days=7)
        elif (self.isDaily()):
            complete_by_date = complete_by_date + timedelta(days=1)
        elif (self.isMonthly()):
            complete_by_date = complete_by_date + relativedelta(months=1)
        
    def checkOverdue(self):
        if complete_by_date > date.now():
            return True
        else:
            return False

    def hasDueDate(self, date):
        return self.complete_by_date == date
    

    def dueDateBefore(self, date):
        return self.complete_by_date < date

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


