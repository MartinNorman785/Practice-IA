from website import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from datetime import date, timedelta, datetime
from dateutil.relativedelta import relativedelta
from sqlalchemy.orm import joinedload
from sqlalchemy.orm import object_session

class Child(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    password = db.Column(db.String(150))
    dob = db.Column(db.Date, default=date.today())
    balance = db.Column(db.Integer)
    starting_balance = db.Column(db.Integer)
    transactions = db.relationship('Transaction')
    chores = db.relationship('Chore')
    overdue_chores = db.relationship('Chore')
    goals = db.relationship('Goal')
    parent_id = db.Column(db.Integer, db.ForeignKey('parent.id'))
    parentAccess = db.Column(db.Boolean, default=False)

    def __init__(self, name, password, dob, balance=0):
        print(dob)
        self.name = name
        self.dob = self.stringToDOB(dob)
        self.balance = balance
        self.password = password

        self.STARTING_BANK_BALANCE = balance
        self.parentAccess = False



    def __str__(self):
        self._rebind_if_detached()
        string = self.name + ": " + str(self.getAge()) + "years old\n " + self.getBalanceString() + "\n"
        
        string = string + "Past Transactions:"
        for t in self.transactions[-5:]:
            string = string + "\n" + str(t)
        

        string = string + "\nGoals:"
        for g in self.goals:
            string = string + "\n" + str(g)
        

        string = string + "\nChores Todo:"
        for c in self.chores:
            string = string + "\n" + str(c)
        

        string = string + "\nOverdue Chores:"
        for c in self.overdue_chores:
            string = string + "\n" + str(c)
        return string 
    

    # Basic Getters

    def getName(self):
        self._rebind_if_detached()
        return self.name
    
    def getPassword(self):
        return self.password

    def getDOBString(self):
        self._rebind_if_detached()
        return self.dobToString(self.dob)
    

    def getDOB(self):
        self._rebind_if_detached()
        return self.dob
    

    def getAge(self):
        self._rebind_if_detached()
        today = date.today()
        age = today.year - self.dob.year
        if (today.month, today.day) < (self.dob.month, self.dob.day):
            age -= 1
        return age
    

    def getBankBalance(self):
        self._rebind_if_detached()
        return self.balance
    

    def getBalanceString(self):
        self._rebind_if_detached()
        dollars = str(abs(self.balance)//100)
        cents = str(abs(self.balance) % 100)
        if (self.balance < 0):
            return "-$" + dollars + "." + cents
        
        return "$" + dollars + "." + cents
    

    def getStartingBalance(self):
        self._rebind_if_detached()
        return self.STARTING_BANK_BALANCE
    

    def getStartingBalanceString(self):
        self._rebind_if_detached()
        dollars = str(self.STARTING_BANK_BALANCE // 100)
        cents = str(self.STARTING_BANK_BALANCE % 100)
        return dollars + "." + cents
    

    # Basic Setters

    def changeName(self, name):
        self._rebind_if_detached()
        self.name = name
    

    def changeDOB(self, dob):
        self._rebind_if_detached()
        try:
            dob = stringToDOB(dob)
        finally:
            self.dob = dob
    

    def changeBalance(self, value, description=None, localDate=None):
        self._rebind_if_detached()
        if description is None:
            if localDate is None:
                new_transaction = Transaction(value)
            else:
                new_transaction = Transaction(value, localDate)
        else:
            if localDate is None:
                new_transaction = Transaction(value, description)
            else:
                new_transaction = Transaction(value, description, localDate)
        transactions.append(new_transaction)
        self.balance = self.balance + value
        return new_transaction
    

    # Transaction Methods

    def getTransactions(self):
        self._rebind_if_detached()
        return self.transactions
    

    def removeTransaction(self, t):
        self._rebind_if_detached()
        self.transactions.remove(t)
        self.balance = self.balance - t.getValue()
    

    def getLastNTransactions(self, n):
        self._rebind_if_detached()       
        return self.transactions[-5:]
    

    def getDeposits(self):
        self._rebind_if_detached()
        return [x for x in self.transactions if x.getValue() > 0]
    

    def getWithdrawals(self):
        self._rebind_if_detached()
        return [x for x in self.transactions if x.getValue() < 0]
    

    def getDepositsGreaterThan(self, value):
        self._rebind_if_detached()
        return [x for x in self.getDeposits() if x.getValue() > value]
    

    def getDepositsLessThan(self, value):
        self._rebind_if_detached()
        return [x for x in self.getDeposits() if x.getValue() < value]
    

    def getDepositsBetween(self, min, max):
        self._rebind_if_detached()
        return [x for x in self.getDeposits() if x.getValue() > min and x.getValue() < max]

    def getWithdrawalsGreaterThan(self, value):
        self._rebind_if_detached()
        return [x for x in self.getWithdrawals() if x.getValue() < value]
    

    def getWithdrawalsLessThan(self, value):
        self._rebind_if_detached()
        return [x for x in self.getWithdrawals() if x.getValue() > value]
    

    def getWithdrawalsBetween(self, min, max):
        self._rebind_if_detached()
        return [x for x in self.getWithdrawals() if x.getValue() < min and x.getValue() > max]
    

    # Chore Methods

    def getChores(self):
        self._rebind_if_detached()
        return chores
    

    def getOverdueChores(self):
        self._rebind_if_detached()
        return self.chores
    

    def addChore(self, name, description, value, recurring):
        self._rebind_if_detached()
        self.chores.append(Chore(name, description, value, recurring))
    

    def addChore(self, name, description, recurring):
        self._rebind_if_detached()
        self.hores.append(Chore(name, description, recurring))
    

    def addChore(self, c):
        self._rebind_if_detached()
        self.chores.append(c)
    

    def checkChoresOverdue(self):
        self._rebind_if_detached()
        for chore in self.chores:
            if chore.checkOverdue():
                self.makeChoreOverdue(chore)
            
        
    

    def removeChore(self, chore):
        self._rebind_if_detached()
        self.chores.remove(chore)
    
        
    def removeOverdueChore(self, chore):
        self._rebind_if_detached()
        self.overdue_chores.remove(chore)
    

    def makeChoreOverdue(self, chore):
        self._rebind_if_detached()
        if chore in self.chores:
            self.chores.remove(chore)
            chore.makeOverdue()
            self.overdue_chores.append(chore)
        
    

    def makeChoreNonOverdue(self, chore):
        self._rebind_if_detached()
        if chore in self.overdue_chores:
            self.overdue_chores.remove(chore)
            chore.makeNotOverdue()
            self.chores.append(chore)
        
    

    def completeChore(self, chore):
        self._rebind_if_detached()
        chore.complete(self)
    

    def choresDueWithin(self, days):
        self._rebind_if_detached()
        return [x for x in chores if x.day <= date.today().day + days]
    

    def mandatoryChores(self):
        self._rebind_if_detached()
        return [x for x in chores if x.isMandatory()]
    

    def optionalChores(self):
        self._rebind_if_detached()
        return [x for x in chores if not x.isMandatory()]
    

    def choresWorthMoreThan(self, value):
        self._rebind_if_detached()
        return [x for x in chores if x.value() > value]
    

    def choresWorthLessThan(self, value):
        self._rebind_if_detached()
        return [x for x in chores if x.value() < value]
    

    def choresWorthBetween(self, min, max):
        self._rebind_if_detached()
        return [x for x in chores if x.value() > min and x.value() < max]
    

    def onceOffChores(self):
        self._rebind_if_detached()
        return [x for x in chores if x.doesntRecurre()]
    

    def weeklyChores(self):
        self._rebind_if_detached()
        return [x for x in chores if x.isWeekly()]
    

    def dailyChores(self):
        self._rebind_if_detached()
        return [x for x in chores if x.isDaily()]
    

    def monthlyChores(self):
        self._rebind_if_detached()
        return [x for x in chores if x.isMonthly()]
    

    # Goal Methods

    def getGoals(self):
        self._rebind_if_detached()
        return self.goals
    

    def addGoal(self, name="", value="", date=None, description=None, goal=None):
        self._rebind_if_detached()
        if goal is None:
            if date is None:
                if description is None:
                    goal = Goal(name, value)
                else:
                    goal = Goal(name, value, description)
            else:
                if description is None:
                    goal = Goal(name, value, date)
                else:
                    goal = Goal(name, value, description, date)
        self.goals.append(goal)
        return goal
    

    def completeGoal(self, goal, subtract_money=False):
        self._rebind_if_detached()
        self.goals.remove(goal)
        if (subtract_money):
            self.changeBalance(-goal.getGoalValue(), goal.getName(), LocalDate.now())
        
    

    def findGoal(self, name):
        self._rebind_if_detached()
        for goal in self.goals:
            if (goal.getName() == name):
                return goal
        return None
    
    
    def closeGoals(self, days):
        self._rebind_if_detached()
        return [x for x in self.goals if x.getDueDate.day < date.today().day + days]
    

    def goalsBefore(self, date):
        self._rebind_if_detached()
        return [x for x in self.goals if x.getDueDate.day < date.today().day + days]
    

    def goalsAfter(self, date):
        self._rebind_if_detached()
        return [x for x in self.goals if x.getDueDate.day > date.today().day + days]
    

    def goalsWorthMoreThan(self):
        self._rebind_if_detached()
        return [x for x in self.goals if x.valueGreaterThan(value)]
    

    def goalsWorthLessThan(self, value):
        self._rebind_if_detached()
        return [x for x in self.goals if x.valueLessThan(value)]
    

    def goalsWorthBetween(self, min, max):
        self._rebind_if_detached()
        return [x for x in self.goals if x.valueBetween(min, max)]
        

    # Other Methods

    def stringToDOB(self, dob):
        self._rebind_if_detached()
        return datetime.strptime(dob, "%Y-%m-%d").date()
    

    def dobToString(self, dob):
        self._rebind_if_detached()
        return str(dob)
    

    def _rebind_if_detached(self):
        return
