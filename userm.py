import datetime
from utilities.score import Score
from utilities.user import User
import os

class UserManager:
    def __init__(self):
        self.users = {}
        self.top_scores = []

    def load_users(self, filename):
        try:
            with open(filename, 'r') as file:
                for line in file:
                    username, password = line.strip().split(',')
                    self.users[username] = password
        except FileNotFoundError:
            with open(filename, 'w') as file:
                pass
    
    def load_top_scores(self, filename):
        try:
            with open(filename, 'r') as file:
                for line in file:
                    username, points, wins = line.strip().split(',')
                    score = Score(username, int(points), int(wins))
                    self.top_scores.append(score)
        except FileNotFoundError:
            with open(filename, 'w') as file:
                pass

    def save_users(self, filename):
        with open(filename, 'w') as file:
            for username, password in self.users.items():
                file.write(f"{username},{password}\n")

    def save_top_scores(self, filename):
        with open(filename, 'w') as file:
            for score in self.top_scores:
                file.write(f"{score.username},{score.points},{score.wins}\n")

    def check_username(self, username):
        if len(username) < 4:
            print("Username must be at least 4 characters long.")
            return False
        elif username in self.users:
            print("Username already exists.")
            return False
        return True
            
    def check_password(self, password):
        if len(password) < 8:
            print("Password must be at least 8 characters long.")
            return False
        return True

    def register(self):
        print("================================================================")
        print("\t\t\tRegistration Menu")
        print("================================================================")
        while True:
            username = input("Enter your username (at least 4 characters) or leave blank to cancel: ")
            if not username:
                print("Registration cancelled.")
                return
            if self.check_username(username):
                break
        while True:
            password = input("Enter your password (at least 8 characters) or leave blank to cancel: ")
            if not password:
                print("Registration cancelled.")
                return
            if self.check_password(password):
                break
            
        self.users[username] = password
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"Registration successful at {timestamp}.")
        self.save_users("users.txt")
        
    def login(self):
        while True:
            print("================================================================")
            print("\t\t\tLogin Menu")
            print("================================================================")
            username = input("Enter username: ")
            password = input("Enter password: ")
            if username in self.users and self.users[username] == password:
                print("Login successful.")
                return User(username, password)
            else:
                print("Invalid username or password.")

    def save_and_exit(self):
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"Exiting program at {timestamp}")
        self.save_top_scores("top_scores.txt")
        exit()
