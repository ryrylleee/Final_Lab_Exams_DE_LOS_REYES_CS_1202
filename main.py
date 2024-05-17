from utilities.userm import UserManager
from utilities.dicegame import DiceGame
import os

def main():
    user_manager = UserManager() 
    user_manager.load_users("users.txt")
    user_manager.load_top_scores("top_scores.txt")  

    while True:
        try: 
            print("======================================================")
            print("\t\tSTARTING MENU")
            print("======================================================")
            print("\t\t1. Register")
            print("\t\t2. Log in")
            print("\t\t3. Exit")
            print("======================================================")
            user_choice = input("Enter your choice: ") 
            if user_choice == "1":
                os.system('cls')
                user_manager.register()
            elif user_choice == "2":
                os.system('cls')
                cur_user = user_manager.login()  
                if cur_user:
                    os.system('cls')
                    dice_game = DiceGame(user_manager)  
                    dice_game.cur_user = cur_user
                    dice_game.menu()
            elif user_choice == "3":
                os.system('cls')
                user_manager.save_and_exit()  
                break  
            else:
                print("Choose number 1-3 only. Please choose again.")
        except Exception as error:  
            print(f'Error: {error}')

if __name__ == "__main__":
    main()