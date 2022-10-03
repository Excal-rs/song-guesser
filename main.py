import bcrypt
import csv
import os

class UserDetail:
    def __init__(self, username, password, score):

        accountbase = open("Accounts.csv", "a", newline="")
        writer = csv.writer(accountbase)

        self.username = username
        self.hpassword = bcrypt.hashpw((password).encode("utf-8"), bcrypt.gensalt())
        self.score = score
        #hashes the passcode so it can be stored securely
        usertuple = (self.username, self.hpassword.decode("utf-8"), self.score)

        writer.writerow(usertuple)
        #writes username and hashed password to the csv file

        accountbase.close()


with open("Accounts.csv") as accountbase:
    reader = csv.DictReader(accountbase)
    usernames = []

    for row in reader:
        usernames.append(row["Username"])

    accountbase.close()
        # creates a list of all usernames from the csv file


# Subprogram to create a new user if needed
def createUser():
        print("\nOK! Let's make an account for you!")
        username = str(input("What do you want to be called? "))

        while username in usernames:
            username = str(input("Sorry, that username is already taken! \nPlease enter another username: "))
        #Ensures there are no duplicate usernames by checking all usernames in use

        password = str(input("Please enter password: "))
        #os.system('cls')  #only works on windows machines (cant test as I am using Arch)
        passwordconf = str(input("Please confirm password: "))

        while password != passwordconf:
                #os.system('cls')
                print("Sorry those passwords don't match! Try again. ")

                password = str(input("Please enter password: "))
                #os.system('cls')
                passwordconf = str(input("Please confirm password: "))


        print("Thank you for making an account, you can now log in! \n")
        newuser = UserDetail(username, password, 0)

        accountbase.close()



def GetRow(username):
    accountbase = csv.reader(open("Accounts.csv", "r"))
    for row in accountbase:
        if username == row[0]:
            break
    return row


def Login(username, password):

    accountbase = csv.reader(open("Accounts.csv", "r"))
    for row in accountbase:
        if username == row[0] and (bcrypt.checkpw(password, (row[1]).encode("utf-8"))):
            print("You have logged in succesfully! \n ")





choice = str(input("Do you already have an account? ")).lower()

while choice not in ['y','yes','no','n']:
    choice = str(input(f"Sorry but \"{choice}\" is not a valid response, please try again! \nDo you have an account? "))
if choice in ['n', 'no']:
    createUser()




Uname = str(input("Please enter account username: "))
Passwd = str(input("Please enter account password: ")).encode("utf-8")

Login(Uname, Passwd)
score = GetRow(Uname)[2]


#Once you have logged in you need to get you're score!







