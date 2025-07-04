import pickle
from users import Parent, Child
from website import create_app

class Main:

    def __init__(self):
        try:
            with open("save.pickle", "rb") as f:
                m = pickle.load(f)
            self.parents = m.parents
            self.children = m.children
        except:
            self.parents = []
            self.children = []

    
    def main(self):

        self.saveMain();

        app = create_app()
        app.run(debug=True, port=5004)
        
        
    


    

    def saveMain(self):
        with open("save.pickle", "ab") as f:
            pickle.dump(self, f)

    def encryptData(self, data):
        encrypted = "";

        for x in data:
            a = ord(x);
            a = a + 41;
            encrypted = encrypted + chr(a);
        
        return encrypted;

    def decryptData(self, data):
        decrypted = "";

        for x in data:
            a = ord(x);
            a = a - 41;
            decrypted = decrypted + chr(a);
        
        return decrypted;

    def removeUser(self, name):
        users = self.loadUsers()
        users = [x for x in users if x.split(": ")[0] != name]
        self.saveUsers("\n".join(users))
    
    def addUser(self, name, password):
        users = "\n".join(self.loadUsers())
        users = users + "\n" + name + ": " + password
        self.saveUsers(users)


    def saveUsers(self, users):
        with open("logins.txt", "w") as f:
            for line in users:
                f.write(self.encryptData(line))

    def loadUsers(self):
        with open("logins.txt", "r") as f:
            users = []
            for x in f.readlines():
                for y in self.decryptData(x).split("\n"):
                    users.append(y)
            return users

    def login(self, username, password):
        authorised = False
        for user in self.loadUsers():
            if user.split(": ")[0] == username:
                if user.split(": ")[1] == password:
                    authorised = True
        if not authorised:
            return None

        for child in self.children:
            if child.name == username:
                return child
        
        for parent in self.parents:
            if parent.name == username:
                return parent
        
 
if __name__ == "__main__":
    mn = Main()
    mn.main()

