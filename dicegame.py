import os
import random
import time
from utilities.score import Score

class DiceGame:
    def __init__(self, user_manager):
        self.user_manager = user_manager
        self.cur_user = {}
        self.top_scores = []
        self.stage_won = False

    def menu(self):
        while True:
            self.loading("Loading Menu")
            os.system('cls' if os.name == 'nt' else 'clear')
            if self.cur_user:
                print("====================================================================")
                print(f"\t\t=== Welcome to the Dice Game, {self.cur_user.username} ===")
                print("====================================================================")
                print("\t\t1. Start Game")
                print("\t\t2. View Top Scores")
                print("\t\t3. Log out")
                print("====================================================================")
                choice = input("Enter your choice: ")
                if choice == "1":
                    os.system('cls')
                    self.start_game()
                elif choice == "2":
                    os.system('cls')
                    self.display_top_scores()
                elif choice == "3":
                    os.system('cls')
                    self.cur_user = None
                    print("================================================================")
                    print("\t\tLogged out successfully.")
                    print("================================================================")
                    break
                else:
                    print("Invalid choice. Please choose again.")

    def start_game(self):
        if not self.cur_user:
            print("Error: No user logged in.")
            return
        self.loading("\t\tStarting Game")
        print("\n================================================================")
        print("\t\t=== Game Started ===")
        print("================================================================")
        self.cur_user.points = 0
        self.cur_user.stages_won = 0
        self.stage_won = False  
        time.sleep(1)  
        while True:
            stage_result = self.play_stage()
            if stage_result == "lost":
                if not self.stage_won:
                    print("Game over. You didn’t win any stages.")
                else:
                    print(f"Stage lost. Total points: {self.cur_user.points}, Stages won: {self.cur_user.stages_won}")
                if self.stage_won:  
                    self.record_score()
                break
            elif stage_result == "won":
                self.stage_won = True
                print(f"Stage won! Total points: {self.cur_user.points}")
                time.sleep(1)  
                continue_game = input("Do you want to continue to the next stage? (1: Yes, 0: No): ")
                if continue_game == "1":
                    continue
                elif continue_game == "0":
                    self.record_score()
                    break
                else:
                    print("Invalid input. Ending game.")
                    self.record_score()
                    break

        
        input("Press Enter to continue...")
        os.system('cls' if os.name == 'nt' else 'clear')
        self.menu()

    def play_stage(self):
        player_wins = 0
        computer_wins = 0
        while player_wins < 2 and computer_wins < 2:
            self.loading("\n\t\tPlaying Stage")
            print("\n================================================================")
            player_roll = random.randint(1, 6)
            computer_roll = random.randint(1, 6)
            print(f"\nYou rolled: {player_roll}")
            print(f"CPU rolled: {computer_roll}")
            time.sleep(1)  
            if player_roll > computer_roll:
                player_wins += 1
                if not self.stage_won:  
                    self.cur_user.points += 1
                print("You win this round!")
            elif player_roll < computer_roll:
                computer_wins += 1
                print("CPU wins this round!")
            else:
                print("It's a tie! No points awarded.")
        
        if player_wins == 2:
            self.cur_user.stages_won += 1
            self.cur_user.points += 3
            return "won"
        else:
            return "lost"

    def display_top_scores(self):
        self.loading("\t\tLoading Top Scores")
        print("\n================================================================")
        print("\t\t\tTOP SCORES")
        print("================================================================")
        if not self.user_manager.top_scores: 
            print("No scores available yet.")
            input("Press Enter to continue...")
            return
        print("\t\tTop-10 Highest Scores:")
        for score in self.user_manager.top_scores:
            print(f"\t\tUsername: {score.username} \n\t\tPoints: {score.points} \n\t\tStages Won: {score.wins}")
        input("Press Enter to continue...")
        os.system('cls' if os.name == 'nt' else 'clear')
        self.menu()

    def record_score(self):
        self.loading("\t\tRecording Score\n")
        print("\n================================================================")
        print("\t\t\tRECORD SCORE")
        print("================================================================")
        if self.cur_user and self.cur_user.stages_won > 0: 
            new_score = Score(self.cur_user.username, self.cur_user.points, self.cur_user.stages_won)
            self.user_manager.top_scores.append(new_score)
            self.user_manager.top_scores.sort(key=lambda x: x.points, reverse=True)
            if len(self.user_manager.top_scores) > 10:
                self.user_manager.top_scores = self.user_manager.top_scores[:10]
            self.user_manager.save_top_scores("top_scores.txt")  

    def loading(self, message):
        print(f"{message} ", end='', flush=True)
        for _ in range(3):
            print(".", end='', flush=True)
            time.sleep(0.5)

