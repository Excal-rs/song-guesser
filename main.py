import random
import bcrypt
import csv
import os
import pandas as pd

with open("Accounts.csv") as accountbase:
    reader = csv.DictReader(accountbase)
    usernames = []

    for row in reader:
        usernames.append(row["Username"])

    accountbase.close()
        # creates a list of all usernames from the csv file



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





def Login(username, password):

    accountbase = csv.reader(open("Accounts.csv", "r"))
    for row in accountbase:
        if username == row[0] and bcrypt.checkpw(password, (row[1]).encode("utf-8")):
            print("You have succesfully logged in! \n")
        elif username == row[0] and (bcrypt.checkpw(password, (row[1]).encode("utf-8"))) == False:
            print("Incorrect username or password! Please try again! \n")
            Uname = str(input("Please enter account username: "))
            Passwd = str(input("Please enter account password: ")).encode("utf-8")
            Login(Uname, Passwd)
        elif username not in usernames:
            print("That user does not exist! Do you want to create a new user?")
            if input() in ['y',"yes"]:
                createUser()
            else:
                print("OK, Let's try again!")
                Login()

def GetRow(username):
    accountbase = csv.reader(open("Accounts.csv", "r"))
    for row in accountbase:
        if username == row[0]:
            return row
            break






choice = str(input("Do you already have an account? ")).lower()

while choice not in ['y','yes','no','n']:
    choice = str(input(f"Sorry but \"{choice}\" is not a valid response, please try again! \nDo you have an account? "))
if choice in ['n', 'no']:
    createUser()



Uname = str(input("Please enter account username: "))
Passwd = str(input("Please enter account password: ")).encode("utf-8")

Login(Uname, Passwd)
score = GetRow(Uname)[2]


#os.system('cls')

print(f"Welcome to the song guesser game! Your score is currectly {score}!"
      f" Lets try get it higher so u can be on the leaderboard")


def songguess(array):
    print("Enter \"End Now\" as a guess to end game ")
    songbase = pd.read_csv("Songbase.csv")
    total_rows = len(songbase.axes[0])

    for i in range(total_rows):
        song = songbase.song[i]
        songinitial = ' '.join(song[0] for song in song.split()).replace(" ", ".")

        guess = str(input(f"What song is {songinitial} - by {songbase.artist[i]}: "))

        if guess.lower() == "end" and input("Are you sure? y/n") in ["yes", "y"]:
            break
        elif guess.lower() == song.lower():
            score =+ 1
            print(f"That is correct \nYoue score is now: {score}")
            continue
        else:
            if song.lower() != guess.lower():
                print("Incorrect! You have two more attemps before you lose a point!")
                for count in range(2):
                    guess = str(input(f"What song is {songinitial} - by {songbase.artist[i]}: "))
                    if guess.lower() == "end now" and input("Are you sure? y/n") in ["yes", "y"]:
                        break
                    elif guess.lower() == song.lower():
                        score += 1
                        print(f"That is correct \nYoue score is now: {score}")
                        break
                    elif guess.lower() != song.lower():
                        print("incorrect")
                        if count == 2:
                            score -= 1
                            print(f"You have lost one point! Your score is now {score}")
                            break

            continue



array = []
songguess(array)







