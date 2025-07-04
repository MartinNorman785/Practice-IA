from datetime import date, timedelta
from dateutil.relativedelta import relativedelta

class User():
    def __init__(self, name):
        self.name = name

class Parent(User):
    USERTYPE = "Parent"

    
    def __init__(self, name, children=[]):
         self.name = name
         self.children = children

    def getName(self):
        return name

    def getChild(self, name):
        for child in self.children:
            if child.getName() == name:
                return child
        return None 

    def getChildren(self):
        return children
    
    def addChild(self, child):
        children.append(child)

    def removeChild(self, child):
        try:
            children.remove(child)
        finally:
            return None

class Child(User):
    USERTYPE = "Child"


    def __init__(self, name, dob, bank_balance=0):
        self.name = name
        self.dob = self.stringToDOB(dob)
        self.bank_balance = bank_balance

        self.STARTING_BANK_BALANCE = bank_balance

        self.transaction_history = []
        self.chores = []
        self.overdue_chores = []
        self.goals = []
    

    def __str__(self):
        string = name + ": " + str(self.getAge()) + "years old\n " + self.getBalanceString() + "\n"
        
        string = string + "Past Transactions:"
        for t in self.transaction_history[-5:]:
            string = string + "\n" + str(last_transactions[i])
        

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
        return bank_balance
    

    def getBalanceString(self):
        dollars = str(abs(bank_balance)//100)
        cents = str(abs(bank_balance) % 100)
        if (bank_balance < 0):
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
        transaction_history.add(new_transaction)
        self.bank_balance = self.bank_balance + value
        return new_transaction
    

    # Transaction Methods

    def getTransactions(self):
        return self.transaction_history
    

    def removeTransaction(self, t):
        self.transaction_history.remove(t)
        self.bank_balance = self.bank_balance - t.getValue()
    

    def getLastNTransactions(n):
        
        return self.transaction_history[-5:]
    

    def getDeposits(self):
        return [x for x in self.transaction_history if x.getValue() > 0]
    

    def getWithdrawals(self):
        return [x for x in self.transaction_history if x.getValue() < 0]
    

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
    

    def addGoal(name="", value="", date=None, description=None, goal=None):
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
    

    def completeGoal(goal, subtract_money=False):
        self.goals.remove(goal)
        if (subtract_money):
            self.changeBalance(-goal.getGoalValue(), goal.getName(), LocalDate.now())
        
    

    def findGoal(name):
        for goal in self.goals:
            if (goal.getName() == name):
                return goal
        return None
    
    
    def closeGoals(days):
        return [x for x in self.goals if x.getDueDate.day < date.today().day + days]
    

    def goalsBefore(date):
        return [x for x in self.goals if x.getDueDate.day < date.today().day + days]
    

    def goalsAfter(date):
        return [x for x in self.goals if x.getDueDate.day > date.today().day + days]
    

    def goalsWorthMoreThan():
        return [x for x in self.goals if x.valueGreaterThan(value)]
    

    def goalsWorthLessThan(value):
        return [x for x in self.goals if x.valueLessThan(value)]
    

    def goalsWorthBetween(min, max):
        return [x for x in self.goals if x.valueBetween(min, max)]
        

    # Other Methods

    def stringToDOB(dob):
        return date.strftime(dob, "%d/%m/%Y")
    

    def dobToString(dob):
        return str(dob)
    
    


