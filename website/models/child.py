from website import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from datetime import date, timedelta, datetime
from dateutil.relativedelta import relativedelta

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

        self.transactions = []
        self.chores = []
        self.overdue_chores = []
        self.goals = []


    def __str__(self):
        print(self.dob, self.name)
        string = self.name + ": " + str(self.getAge()) + "years old\n " + self.getBalanceString() + "\n"
        
        string = string + "Past Transactions:"
        for t in self.transactions[-5:]:
            string = string + "\n" + str(transactions[i])
        

        string = string + "\nGoals:"
        for g in goals:
            string = string + "\n" + str(goals[i])
        

        string = string + "\nChores Todo:"
        for c in chores:
            string = string + "\n" + str(chores[i])
        

        string = string + "\nOverdue Chores:"
        for c in overdue_chores:
            string = string + "\n" + str(c)
        return string 
    

    # Basic Getters

    def getName(self):
        return self.name
    

    def getDOBString(self):
        return self.dobToString(self.dob)
    

    def getDOB(self):
        return self.dob
    

    def getAge(self):
        today = date.today()
        age = today.year - self.dob.year
        if (today.month, today.day) < (self.dob.month, self.dob.day):
            age -= 1
        return age
    

    def getBankBalance(self):
        return self.balance
    

    def getBalanceString(self):
        dollars = str(abs(self.balance)//100)
        cents = str(abs(self.balance) % 100)
        if (self.balance < 0):
            return "-$" + dollars + "." + cents
        
        return "$" + dollars + "." + cents
    

    def getStartingBalance(self):
        return self.STARTING_BANK_BALANCE
    

    def getStartingBalanceString(self):
        dollars = str(self.STARTING_BANK_BALANCE // 100)
        cents = str(self.STARTING_BANK_BALANCE % 100)
        return dollars + "." + cents
    

    # Basic Setters

    def changeName(self, name):
        self.name = name
    

    def changeDOB(self, dob):
        try:
            dob = stringToDOB(dob)
        finally:
            self.dob = dob
    

    def changeBalance(self, value, description=None, localDate=None):
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
        transactions.add(new_transaction)
        self.balance = self.balance + value
        return new_transaction
    

    # Transaction Methods

    def getTransactions(self):
        return self.transactions
    

    def removeTransaction(self, t):
        self.transactions.remove(t)
        self.balance = self.balance - t.getValue()
    

    def getLastNTransactions(n):
        
        return self.transactions[-5:]
    

    def getDeposits(self):
        return [x for x in self.transactions if x.getValue() > 0]
    

    def getWithdrawals(self):
        return [x for x in self.transactions if x.getValue() < 0]
    

    def getDepositsGreaterThan(value):
        return [x for x in self.getDeposits() if x.getValue() > value]
    

    def getDepositsLessThan(value):
        return [x for x in self.getDeposits() if x.getValue() < value]
    

    def getDepositsBetween(min, max):
        return [x for x in self.getDeposits() if x.getValue() > min and x.getValue() < max]

    def getWithdrawalsGreaterThan(value):
        return [x for x in self.getWithdrawals() if x.getValue() < value]
    

    def getWithdrawalsLessThan(value):
        return [x for x in self.getWithdrawals() if x.getValue() > value]
    

    def getWithdrawalsBetween(min, max):
        return [x for x in self.getWithdrawals() if x.getValue() < min and x.getValue() > max]
    

    # Chore Methods

    def getChores(self):
        return chores
    

    def getOverdueChores(self):
        return self.chores
    

    def addChore(name, description, value, recurring):
        self.chores.append(Chore(name, description, value, recurring))
    

    def addChore(name, description, recurring):
        self.hores.add(Chore(name, description, recurring))
    

    def addChore(c):
        self.chores.add(c)
    

    def checkChoresOverdue(self):
        for chore in self.chores:
            if chore.checkOverdue():
                self.makeChoreOverdue(chore)
            
        
    

    def removeChore(chore):
        self.chores.remove(chore)
    
        
    def removeOverdueChore(chore):
        self.overdue_chores.remove(chore)
    

    def makeChoreOverdue(chore):
        if chore in self.chores:
            self.chores.remove(chore)
            chore.makeOverdue()
            self.overdue_chores.add(chore)
        
    

    def makeChoreNonOverdue(chore):
        if chore in self.overdue_chores:
            self.overdue_chores.remove(chore)
            chore.makeNotOverdue()
            self.chores.add(chore)
        
    

    def completeChore(chore):
        chore.complete(self)
    

    def choresDueWithin(days):
        return [x for x in chores if x.day <= date.today().day + days]
    

    def mandatoryChores(self):
        return [x for x in chores if x.isMandatory()]
    

    def optionalChores(self):
        return [x for x in chores if not x.isMandatory()]
    

    def choresWorthMoreThan(value):
        return [x for x in chores if x.value() > value]
    

    def choresWorthLessThan(value):
        return [x for x in chores if x.value() < value]
    

    def choresWorthBetween(min, max):
        return [x for x in chores if x.value() > min and x.value() < max]
    

    def onceOffChores(self):
        return [x for x in chores if x.doesntRecurre()]
    

    def weeklyChores(self):
        return [x for x in chores if x.isWeekly()]
    

    def dailyChores(self):
        return [x for x in chores if x.isDaily()]
    

    def monthlyChores(self):
        return [x for x in chores if x.isMonthly()]
    

    # Goal Methods

    def getGoals(self):
        return self.goals
    

    def addGoal(self, name="", value="", date=None, description=None, goal=None):
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
        self.goals.add(goal)
        return goal
    

    def completeGoal(self, goal, subtract_money=False):
        self.goals.remove(goal)
        if (subtract_money):
            self.changeBalance(-goal.getGoalValue(), goal.getName(), LocalDate.now())
        
    

    def findGoal(self, name):
        for goal in self.goals:
            if (goal.getName() == name):
                return goal
        return None
    
    
    def closeGoals(self, days):
        return [x for x in self.goals if x.getDueDate.day < date.today().day + days]
    

    def goalsBefore(self, date):
        return [x for x in self.goals if x.getDueDate.day < date.today().day + days]
    

    def goalsAfter(self, date):
        return [x for x in self.goals if x.getDueDate.day > date.today().day + days]
    

    def goalsWorthMoreThan(self):
        return [x for x in self.goals if x.valueGreaterThan(value)]
    

    def goalsWorthLessThan(self, value):
        return [x for x in self.goals if x.valueLessThan(value)]
    

    def goalsWorthBetween(self, min, max):
        return [x for x in self.goals if x.valueBetween(min, max)]
        

    # Other Methods

    def stringToDOB(self, dob):
        return datetime.strptime(dob, "%Y-%m-%d").date()
    

    def dobToString(dob):
        return str(dob)