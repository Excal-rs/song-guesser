import random
import bcrypt
import os
import pandas as pd

# Create a list of all used usernames for later refrence
accountbase = pd.read_csv("Accounts.csv")
usernames = accountbase["Username"].tolist()


#Handles Hashing and storing passwords and usernames
class UserDetail:
    def __init__(self, username, password, score):

        self.username = username
        self.hpassword = bcrypt.hashpw((password).encode("utf-8"), bcrypt.gensalt())
        self.score = score
        #hashes the passcode so it can be stored securely
        df = pd.DataFrame({"Username": [self.username],
                           "password": [self.hpassword.decode("utf-8")],
                           "score": [self.score]})

        #writes username and hashed password to the csv file
        df.to_csv("Accounts.csv", mode="a", index=False, header=True)



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


def prelogin():
    choice = str(input("Do you already have an account? ")).lower()
    while choice not in ['y','yes','no','n']:
        choice = str(input(f"Sorry but \"{choice}\" is not a valid response, please try again! \nDo you have an account? "))
    if choice in ['n', 'no']:
        createUser()
    elif choice in ['y', 'yes', '']:
        print("")
    else:
        print("Incorrect input Please try again")
        prelogin()


def Login(username, password):
    accountbase = pd.read_csv("Accounts.csv")
    usernames = accountbase["Username"].tolist()
    #refreshes list incase a new user was created

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
            x = input().lower()
            if x in ['y',"yes"]:
                createUser()

            elif x in ['','n','no']:
                print("OK, Let's try again!")
                Uname = str(input("Please enter account username: "))
                Passwd = str(input("Please enter account password: ")).encode("utf-8")

                Login(Uname, Passwd)


# Fetches the index for row of user for future refrence e.g score
def GetRow(username):
    accountbase = pd.read_csv("Accounts.csv")
    index = accountbase.index[accountbase["Username"]==username].tolist()
    index = index[0]
    return index





# Main part of program
def songguess(score):
    print("Enter \"End Now\" as a guess to end game ")
    songbase = pd.read_csv("Songbase.csv")
    total_rows = len(songbase.axes[0])

    for i in range(total_rows):
        songbase = pd.read_csv('Songbase.csv')
        song = songbase.loc[i, 'song'].lower()
        artist = songbase.loc[i, 'artist'].lower()

        songinitial = ' '.join(song[0] for song in song.split()).replace(" ", ".")

        guess = str(input(f"What song is {songinitial} - by {artist}: "))

        if guess == "end" and input("Are you sure? y/n") in ["yes", "y"]:
            break

        elif guess == song:
            score += 1
            print(f"That is correct \nYoue score is now: {score} \n")
            continue

        elif song != guess:
            print("Incorrect! You have two more attemps before you lose a point!\n")

            for x in range(2):
                guess = str(input(f"What song is {songinitial} - by {songbase.artist[i]}: "))

                if guess == "end now" and input("Are you sure? y/n") in ["yes", "y"]:
                    break

                elif guess == song:
                    score += 1
                    print(f"That is correct \nYour score is now: {score} \n")
                    break
                elif guess != song:
                    print("incorrect")

                    if x == 2:
                        score -= 1
                        print(f"You have lost one point! Your score is now: {score}\n")
                        break

        continue
    return score

def SortLeaderboard(lb):
    reverse = None
    lb.sort(reverse=True, key=lambda x: x[1])
    return lb

#Allows for choice of account creation through previous subprogram
prelogin()

Uname = str(input("Please enter account username: "))
Passwd = str(input("Please enter account password: ")).encode("utf-8")

Login(Uname, Passwd)


accountbase = pd.read_csv("Accounts.csv")
score = accountbase['score'].iloc[GetRow(Uname)]


# os.system('cls')

print(f"Welcome to the song guesser game! Your score is currectly {score} !"
      f" Lets try get it higher so u can be on the leaderboard")

score = songguess(score)

print("Thank you for playing! :) ")

accountbase.loc[GetRow('Excal-rs'), 'score'] = score
accountbase.to_csv('Accounts.csv', index=False)

print("Are you on the leaderboard? \n")

for count in range(len(accountbase.index)):
    leaderboard = []
    leaderboard = ((accountbase[['Username', 'score']]).values.tolist())


df = pd.DataFrame(SortLeaderboard(leaderboard), columns=['Username', 'Score'])
print(df)

df.to_csv('Leaderboard.csv', index=False, header=True)

