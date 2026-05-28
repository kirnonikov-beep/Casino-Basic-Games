import tkinter as tk
from tkinter import ttk, messagebox
import random
from collections import Counter
import os
from pathlib import Path

# Try to import pygame for sound effects
try:
    import pygame
    pygame.mixer.init()
    SOUND_ENABLED = True
except:
    SOUND_ENABLED = False

class CasinoGame:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🎰 The Gambling House - Enhanced Edition 🎰")
        self.root.geometry("800x600")
        self.root.configure(bg="#1a1a1a")
        
        # Game variables
        self.balance = 100
        self.borrowed_amount = 0
        self.max_loan = 500
        self.game_over = False
        
        # Sounds
        self.sounds = {}
        self.load_sounds()
        
        # Main frame
        self.main_frame = tk.Frame(self.root, bg="#1a1a1a")
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        self.create_main_menu()
        
    def load_sounds(self):
        """Load or create sound effects"""
        if SOUND_ENABLED:
            try:
                # We'll use simple beep sounds for now
                self.sounds['win'] = self.create_beep(1000, 200)
                self.sounds['lose'] = self.create_beep(400, 200)
                self.sounds['click'] = self.create_beep(800, 100)
            except:
                pass
    
    def create_beep(self, frequency, duration):
        """Create a simple beep sound"""
        try:
            import numpy as np
            sample_rate = 22050
            frames = int(duration * sample_rate / 1000)
            arr = np.sin(2.0 * np.pi * frequency * np.linspace(0, duration/1000, frames))
            arr = (arr * 32767).astype(np.int16)
            return pygame.sndarray.make_sound(arr)
        except:
            return None
    
    def play_sound(self, sound_key):
        """Play a sound effect"""
        if SOUND_ENABLED and sound_key in self.sounds and self.sounds[sound_key]:
            try:
                self.sounds[sound_key].play()
            except:
                pass
    
    def clear_frame(self):
        """Clear all widgets from main frame"""
        for widget in self.main_frame.winfo_children():
            widget.destroy()
    
    def create_header(self, title):
        """Create a header with balance info"""
        header = tk.Frame(self.main_frame, bg="#2a2a2a", relief=tk.RAISED, bd=2)
        header.pack(fill=tk.X, pady=(0, 20))
        
        title_label = tk.Label(header, text=title, font=("Arial", 24, "bold"), 
                              fg="#FFD700", bg="#2a2a2a")
        title_label.pack(pady=10)
        
        info_frame = tk.Frame(header, bg="#2a2a2a")
        info_frame.pack(fill=tk.X, padx=20, pady=(0, 10))
        
        bal_text = f"Balance: ${self.balance}"
        loan_text = f"Borrowed: ${self.borrowed_amount}" if self.borrowed_amount > 0 else ""
        total_text = f"Total Assets: ${self.balance + self.borrowed_amount}"
        
        tk.Label(info_frame, text=bal_text, font=("Arial", 12), 
                fg="#00FF00", bg="#2a2a2a").pack(side=tk.LEFT, padx=10)
        
        if self.borrowed_amount > 0:
            tk.Label(info_frame, text=loan_text, font=("Arial", 12), 
                    fg="#FF6B6B", bg="#2a2a2a").pack(side=tk.LEFT, padx=10)
        
        tk.Label(info_frame, text=total_text, font=("Arial", 12), 
                fg="#4DD0E1", bg="#2a2a2a").pack(side=tk.RIGHT, padx=10)
    
    def create_main_menu(self):
        """Create the main menu"""
        self.clear_frame()
        self.create_header("🎰 GAMBLING HOUSE 🎰")
        
        welcome = tk.Label(self.main_frame, text="Welcome to the Casino!", 
                          font=("Arial", 18, "bold"), fg="#FFD700", bg="#1a1a1a")
        welcome.pack(pady=20)
        
        button_frame = tk.Frame(self.main_frame, bg="#1a1a1a")
        button_frame.pack(pady=20)
        
        games = [
            ("🎰 Slot Machine", self.play_slot_machine),
            ("🎲 Number Gamble", self.play_number_gamble),
            ("♠️ Blackjack", self.play_blackjack),
            ("🃏 Poker Dice", self.play_poker_dice),
            ("🎡 Roulette", self.play_roulette),
            ("🐴 Horse Racing", self.play_horse_racing),
        ]
        
        for game_name, game_func in games:
            btn = tk.Button(button_frame, text=game_name, font=("Arial", 12, "bold"),
                           bg="#4CAF50", fg="white", width=20, height=2,
                           command=game_func, relief=tk.RAISED, bd=2)
            btn.pack(pady=5, fill=tk.X)
        
        separator = tk.Frame(self.main_frame, bg="#444", height=2)
        separator.pack(fill=tk.X, pady=20)
        
        info_frame = tk.Frame(self.main_frame, bg="#1a1a1a")
        info_frame.pack()
        
        tk.Button(info_frame, text="💰 Take Loan", font=("Arial", 11, "bold"),
                 bg="#FF9800", fg="white", width=15, command=self.take_loan).pack(side=tk.LEFT, padx=5)
        
        tk.Button(info_frame, text="📊 Stats", font=("Arial", 11, "bold"),
                 bg="#2196F3", fg="white", width=15, command=self.show_stats).pack(side=tk.LEFT, padx=5)
        
        tk.Button(info_frame, text="❌ Quit", font=("Arial", 11, "bold"),
                 bg="#F44336", fg="white", width=15, command=self.root.quit).pack(side=tk.LEFT, padx=5)
    
    def take_loan(self):
        """Handle loan system"""
        if self.borrowed_amount >= self.max_loan:
            messagebox.showerror("Loan Denied", f"You already have the maximum loan of ${self.max_loan}")
            return
        
        dialog = tk.Toplevel(self.root)
        dialog.title("💰 Take a Loan")
        dialog.geometry("300x200")
        dialog.configure(bg="#1a1a1a")
        
        tk.Label(dialog, text="How much do you want to borrow?", 
                font=("Arial", 12), fg="#FFD700", bg="#1a1a1a").pack(pady=10)
        
        available = self.max_loan - self.borrowed_amount
        tk.Label(dialog, text=f"Available to borrow: ${available}", 
                font=("Arial", 10), fg="#4DD0E1", bg="#1a1a1a").pack()
        
        entry = tk.Entry(dialog, font=("Arial", 12), justify=tk.CENTER)
        entry.pack(pady=10, fill=tk.X, padx=20)
        entry.focus()
        
        def borrow():
            try:
                amount = int(entry.get())
                if amount <= 0:
                    messagebox.showerror("Invalid", "Enter a positive amount")
                elif amount > available:
                    messagebox.showerror("Invalid", "Amount exceeds available loan")
                else:
                    self.balance += amount
                    self.borrowed_amount += amount
                    messagebox.showinfo("Success", f"You borrowed ${amount}. Good luck!")
                    dialog.destroy()
                    self.create_main_menu()
            except ValueError:
                messagebox.showerror("Invalid", "Please enter a valid number")
        
        tk.Button(dialog, text="Borrow", font=("Arial", 11, "bold"),
                 bg="#4CAF50", fg="white", command=borrow).pack(pady=5)
    
    def show_stats(self):
        """Show game statistics"""
        stats = f"""
        Current Balance: ${self.balance}
        Borrowed Amount: ${self.borrowed_amount}
        Total Assets: ${self.balance + self.borrowed_amount}
        Max Loan Limit: ${self.max_loan}
        Available to Borrow: ${self.max_loan - self.borrowed_amount}
        """
        messagebox.showinfo("Game Statistics", stats)
    
    def show_game_over(self, reason="You've run out of money!"):
        """Show game over screen"""
        self.clear_frame()
        
        frame = tk.Frame(self.main_frame, bg="#1a1a1a")
        frame.pack(fill=tk.BOTH, expand=True)
        
        title = tk.Label(frame, text="GAME OVER", font=("Arial", 48, "bold"),
                        fg="#FF0000", bg="#1a1a1a")
        title.pack(pady=30)
        
        reason_label = tk.Label(frame, text=reason, font=("Arial", 16),
                               fg="#FFD700", bg="#1a1a1a")
        reason_label.pack(pady=10)
        
        stats = tk.Label(frame, 
                        text=f"Final Balance: ${self.balance}\nBorrowed: ${self.borrowed_amount}",
                        font=("Arial", 14), fg="#4DD0E1", bg="#1a1a1a")
        stats.pack(pady=20)
        
        button_frame = tk.Frame(frame, bg="#1a1a1a")
        button_frame.pack(pady=20)
        
        def restart():
            self.balance = 100
            self.borrowed_amount = 0
            self.create_main_menu()
        
        tk.Button(button_frame, text="🔄 Retry", font=("Arial", 12, "bold"),
                 bg="#4CAF50", fg="white", width=15, height=2,
                 command=restart).pack(pady=5, fill=tk.X)
        
        tk.Button(button_frame, text="🚪 Exit Game", font=("Arial", 12, "bold"),
                 bg="#F44336", fg="white", width=15, height=2,
                 command=self.root.quit).pack(pady=5, fill=tk.X)
    
    def play_number_gamble(self):
        """Number guessing game"""
        self.clear_frame()
        self.create_header("🎯 Number Gamble")
        
        instruction = tk.Label(self.main_frame, text="Guess a number between 1-10!",
                              font=("Arial", 14, "bold"), fg="#FFD700", bg="#1a1a1a")
        instruction.pack(pady=10)
        
        bet_frame = tk.Frame(self.main_frame, bg="#1a1a1a")
        bet_frame.pack(pady=10)
        
        tk.Label(bet_frame, text="Bet Amount:", font=("Arial", 12),
                fg="#4DD0E1", bg="#1a1a1a").pack(side=tk.LEFT, padx=5)
        
        bet_entry = tk.Entry(bet_frame, font=("Arial", 12), width=10, justify=tk.CENTER)
        bet_entry.pack(side=tk.LEFT, padx=5)
        
        num_frame = tk.Frame(self.main_frame, bg="#1a1a1a")
        num_frame.pack(pady=10)
        
        tk.Label(num_frame, text="Your Number:", font=("Arial", 12),
                fg="#4DD0E1", bg="#1a1a1a").pack(side=tk.LEFT, padx=5)
        
        num_entry = tk.Entry(num_frame, font=("Arial", 12), width=10, justify=tk.CENTER)
        num_entry.pack(side=tk.LEFT, padx=5)
        
        result_label = tk.Label(self.main_frame, text="", font=("Arial", 14, "bold"),
                               fg="#FFD700", bg="#1a1a1a")
        result_label.pack(pady=20)
        
        def play():
            try:
                bet = int(bet_entry.get())
                num = int(num_entry.get())
                
                if bet <= 0 or bet > self.balance:
                    messagebox.showerror("Invalid Bet", f"Bet between 1 and ${self.balance}")
                    return
                
                if num < 1 or num > 10:
                    messagebox.showerror("Invalid Number", "Enter a number between 1-10")
                    return
                
                computer_number = random.randint(1, 10)
                
                if num == computer_number:
                    self.play_sound('win')
                    self.balance += bet
                    result = f"🎉 YOU WIN! Computer: {computer_number}, You: {num}\nWon: ${bet}\nNew Balance: ${self.balance}"
                else:
                    self.play_sound('lose')
                    self.balance -= bet
                    result = f"❌ YOU LOSE! Computer: {computer_number}, You: {num}\nLost: ${bet}\nNew Balance: ${self.balance}"
                
                result_label.config(text=result)
                
                if self.balance <= 0:
                    self.root.after(2000, lambda: self.show_game_over("You've lost all your money!"))
            
            except ValueError:
                messagebox.showerror("Invalid Input", "Please enter valid numbers")
        
        play_btn = tk.Button(self.main_frame, text="🎲 PLAY", font=("Arial", 12, "bold"),
                            bg="#4CAF50", fg="white", command=play)
        play_btn.pack(pady=10)
        
        tk.Button(self.main_frame, text="← Back to Menu", font=("Arial", 10),
                 bg="#666", fg="white", command=self.create_main_menu).pack(pady=5)
    
    def play_slot_machine(self):
        """Slot machine game"""
        self.clear_frame()
        self.create_header("🎰 Slot Machine")
        
        instruction = tk.Label(self.main_frame, text="Spin the reels!",
                              font=("Arial", 14, "bold"), fg="#FFD700", bg="#1a1a1a")
        instruction.pack(pady=10)
        
        bet_frame = tk.Frame(self.main_frame, bg="#1a1a1a")
        bet_frame.pack(pady=10)
        
        tk.Label(bet_frame, text="Bet Amount:", font=("Arial", 12),
                fg="#4DD0E1", bg="#1a1a1a").pack(side=tk.LEFT, padx=5)
        
        bet_entry = tk.Entry(bet_frame, font=("Arial", 12), width=10, justify=tk.CENTER)
        bet_entry.pack(side=tk.LEFT, padx=5)
        
        reels_label = tk.Label(self.main_frame, text="[  ?  ] [  ?  ] [  ?  ]",
                              font=("Arial", 20, "bold"), fg="#FFD700", bg="#1a1a1a",
                              relief=tk.SUNKEN, bd=3, padx=20, pady=20)
        reels_label.pack(pady=20)
        
        result_label = tk.Label(self.main_frame, text="", font=("Arial", 12, "bold"),
                               fg="#FFD700", bg="#1a1a1a")
        result_label.pack(pady=10)
        
        def spin():
            try:
                bet = int(bet_entry.get())
                
                if bet <= 0 or bet > self.balance:
                    messagebox.showerror("Invalid Bet", f"Bet between 1 and ${self.balance}")
                    return
                
                symbols = ["Cherry", "Lemon", "Orange", "Bell", "Seven"]
                spin_result = [random.choice(symbols) for _ in range(3)]
                
                reels_label.config(text=f"[{spin_result[0]:^8}] [{spin_result[1]:^8}] [{spin_result[2]:^8}]")
                
                winnings = self.evaluate_slots(spin_result, bet)
                
                if winnings > 0:
                    self.play_sound('win')
                    self.balance += winnings
                    result_label.config(text=f"🎉 WIN! ${winnings}", fg="#00FF00")
                else:
                    self.play_sound('lose')
                    self.balance -= bet
                    result_label.config(text=f"❌ LOSE! -${bet}", fg="#FF6B6B")
                
                if self.balance <= 0:
                    self.root.after(2000, lambda: self.show_game_over("You've lost all your money!"))
            
            except ValueError:
                messagebox.showerror("Invalid Input", "Please enter a valid bet")
        
        spin_btn = tk.Button(self.main_frame, text="🎰 SPIN!", font=("Arial", 12, "bold"),
                            bg="#4CAF50", fg="white", command=spin)
        spin_btn.pack(pady=10)
        
        tk.Button(self.main_frame, text="← Back to Menu", font=("Arial", 10),
                 bg="#666", fg="white", command=self.create_main_menu).pack(pady=5)
    
    def evaluate_slots(self, spin, bet):
        """Evaluate slot machine results"""
        if spin[0] == spin[1] == spin[2]:
            # Jackpot
            return bet * 5
        elif spin[0] == spin[1] or spin[1] == spin[2]:
            # Two of a kind
            return bet * 2
        return 0
    
    def play_blackjack(self):
        """Simplified Blackjack game"""
        self.clear_frame()
        self.create_header("♠️ Blackjack")
        
        bet_frame = tk.Frame(self.main_frame, bg="#1a1a1a")
        bet_frame.pack(pady=10)
        
        tk.Label(bet_frame, text="Bet Amount:", font=("Arial", 12),
                fg="#4DD0E1", bg="#1a1a1a").pack(side=tk.LEFT, padx=5)
        
        bet_entry = tk.Entry(bet_frame, font=("Arial", 12), width=10, justify=tk.CENTER)
        bet_entry.pack(side=tk.LEFT, padx=5)
        
        game_state = {"player_hand": [], "dealer_hand": [], "shoe": [], "bet": 0, "game_active": False}
        
        display_frame = tk.Frame(self.main_frame, bg="#2a2a2a", relief=tk.SUNKEN, bd=2)
        display_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        dealer_label = tk.Label(display_frame, text="Dealer: ", font=("Arial", 12),
                               fg="#4DD0E1", bg="#2a2a2a", justify=tk.LEFT)
        dealer_label.pack(anchor=tk.W, padx=20, pady=5)
        
        player_label = tk.Label(display_frame, text="You: ", font=("Arial", 12),
                               fg="#00FF00", bg="#2a2a2a", justify=tk.LEFT)
        player_label.pack(anchor=tk.W, padx=20, pady=5)
        
        result_label = tk.Label(display_frame, text="", font=("Arial", 12, "bold"),
                               fg="#FFD700", bg="#2a2a2a")
        result_label.pack(pady=10)
        
        button_frame = tk.Frame(self.main_frame, bg="#1a1a1a")
        button_frame.pack(pady=10)
        
        def deal():
            try:
                bet = int(bet_entry.get())
                if bet <= 0 or bet > self.balance:
                    messagebox.showerror("Invalid Bet", f"Bet between 1 and ${self.balance}")
                    return
                
                game_state["bet"] = bet
                game_state["shoe"] = [2,3,4,5,6,7,8,9,10,10,10,10,11] * 4
                random.shuffle(game_state["shoe"])
                game_state["player_hand"] = [game_state["shoe"].pop(), game_state["shoe"].pop()]
                game_state["dealer_hand"] = [game_state["shoe"].pop(), game_state["shoe"].pop()]
                game_state["game_active"] = True
                
                update_display()
                
                if sum(game_state["player_hand"]) == 21 and sum(game_state["dealer_hand"]) == 21:
                    result_label.config(text="Both Blackjack! It's a TIE!")
                    self.balance += bet
                    game_state["game_active"] = False
                elif sum(game_state["player_hand"]) == 21:
                    result_label.config(text="🎉 BLACKJACK! You Win!")
                    self.play_sound('win')
                    self.balance += int(bet * 1.5)
                    game_state["game_active"] = False
                elif sum(game_state["dealer_hand"]) == 21:
                    result_label.config(text="❌ Dealer has Blackjack! You lose!")
                    self.play_sound('lose')
                    self.balance -= bet
                    game_state["game_active"] = False
            except ValueError:
                messagebox.showerror("Invalid Input", "Please enter a valid bet")
        
        def hit():
            if not game_state["game_active"]:
                return
            game_state["player_hand"].append(game_state["shoe"].pop())
            update_display()
            
            if sum(game_state["player_hand"]) > 21:
                result_label.config(text="❌ BUST! You lose!")
                self.play_sound('lose')
                self.balance -= game_state["bet"]
                game_state["game_active"] = False
        
        def stand():
            if not game_state["game_active"]:
                return
            game_state["game_active"] = False
            
            while sum(game_state["dealer_hand"]) < 17:
                game_state["dealer_hand"].append(game_state["shoe"].pop())
            
            update_display()
            
            player_sum = sum(game_state["player_hand"])
            dealer_sum = sum(game_state["dealer_hand"])
            
            if dealer_sum > 21:
                result_label.config(text="🎉 Dealer BUST! You WIN!")
                self.play_sound('win')
                self.balance += game_state["bet"]
            elif player_sum > dealer_sum:
                result_label.config(text="🎉 You WIN!")
                self.play_sound('win')
                self.balance += game_state["bet"]
            elif player_sum < dealer_sum:
                result_label.config(text="❌ Dealer WINS! You lose!")
                self.play_sound('lose')
                self.balance -= game_state["bet"]
            else:
                result_label.config(text="🤝 TIE!")
        
        def update_display():
            dealer_text = f"Dealer: {game_state['dealer_hand']} = {sum(game_state['dealer_hand'])}"
            player_text = f"You: {game_state['player_hand']} = {sum(game_state['player_hand'])}"
            dealer_label.config(text=dealer_text)
            player_label.config(text=player_text)
        
        tk.Button(button_frame, text="💳 DEAL", font=("Arial", 11, "bold"),
                 bg="#4CAF50", fg="white", command=deal).pack(side=tk.LEFT, padx=5)
        
        tk.Button(button_frame, text="Hit", font=("Arial", 11, "bold"),
                 bg="#2196F3", fg="white", command=hit).pack(side=tk.LEFT, padx=5)
        
        tk.Button(button_frame, text="Stand", font=("Arial", 11, "bold"),
                 bg="#FF9800", fg="white", command=stand).pack(side=tk.LEFT, padx=5)
        
        tk.Button(self.main_frame, text="← Back to Menu", font=("Arial", 10),
                 bg="#666", fg="white", command=self.create_main_menu).pack(pady=5)
    
    def play_poker_dice(self):
        """Poker Dice game"""
        self.clear_frame()
        self.create_header("🃏 Poker Dice")
        
        bet_frame = tk.Frame(self.main_frame, bg="#1a1a1a")
        bet_frame.pack(pady=10)
        
        tk.Label(bet_frame, text="Bet Amount:", font=("Arial", 12),
                fg="#4DD0E1", bg="#1a1a1a").pack(side=tk.LEFT, padx=5)
        
        bet_entry = tk.Entry(bet_frame, font=("Arial", 12), width=10, justify=tk.CENTER)
        bet_entry.pack(side=tk.LEFT, padx=5)
        
        dice_label = tk.Label(self.main_frame, text="Dice: ", font=("Arial", 14, "bold"),
                             fg="#FFD700", bg="#1a1a1a")
        dice_label.pack(pady=20)
        
        result_label = tk.Label(self.main_frame, text="", font=("Arial", 12, "bold"),
                               fg="#FFD700", bg="#1a1a1a")
        result_label.pack(pady=10)
        
        def roll():
            try:
                bet = int(bet_entry.get())
                if bet <= 0 or bet > self.balance:
                    messagebox.showerror("Invalid Bet", f"Bet between 1 and ${self.balance}")
                    return
                
                dice = [random.randint(1, 6) for _ in range(5)]
                dice_label.config(text=f"Dice: {dice}")
                
                category = self.evaluate_poker_hand(dice)
                mult = self.payout_multiplier(category)
                
                if mult == 0:
                    self.play_sound('lose')
                    self.balance -= bet
                    result_text = f"❌ {category} - You lose ${bet}"
                else:
                    self.play_sound('win')
                    winnings = int(bet * mult)
                    self.balance += winnings
                    result_text = f"🎉 {category}! You win ${winnings} ({mult}x)"
                
                result_label.config(text=result_text)
                
                if self.balance <= 0:
                    self.root.after(2000, lambda: self.show_game_over("You've lost all your money!"))
            
            except ValueError:
                messagebox.showerror("Invalid Input", "Please enter a valid bet")
        
        tk.Button(self.main_frame, text="🎲 ROLL", font=("Arial", 12, "bold"),
                 bg="#4CAF50", fg="white", command=roll).pack(pady=10)
        
        tk.Button(self.main_frame, text="← Back to Menu", font=("Arial", 10),
                 bg="#666", fg="white", command=self.create_main_menu).pack(pady=5)
    
    def evaluate_poker_hand(self, dice):
        """Evaluate poker dice hand"""
        counts = Counter(dice)
        freq = sorted(counts.values(), reverse=True)
        
        if freq == [5]:
            return "Five of a Kind"
        elif freq == [4, 1]:
            return "Four of a Kind"
        elif freq == [3, 2]:
            return "Full House"
        elif freq == [3, 1, 1]:
            return "Three of a Kind"
        elif freq == [2, 2, 1]:
            return "Two Pairs"
        elif freq == [2, 1, 1, 1]:
            return "One Pair"
        else:
            return "Nothing"
    
    def payout_multiplier(self, category):
        """Get payout multiplier for poker hand"""
        table = {
            "Five of a Kind": 10,
            "Four of a Kind": 7,
            "Full House": 5,
            "Three of a Kind": 2,
            "Two Pairs": 1.1,
            "One Pair": 0,
            "Nothing": 0
        }
        return table.get(category, 0)
    
    def play_roulette(self):
        """Roulette game"""
        self.clear_frame()
        self.create_header("🎡 Roulette")
        
        bet_frame = tk.Frame(self.main_frame, bg="#1a1a1a")
        bet_frame.pack(pady=10)
        
        tk.Label(bet_frame, text="Bet Amount:", font=("Arial", 12),
                fg="#4DD0E1", bg="#1a1a1a").pack(side=tk.LEFT, padx=5)
        
        bet_entry = tk.Entry(bet_frame, font=("Arial", 12), width=10, justify=tk.CENTER)
        bet_entry.pack(side=tk.LEFT, padx=5)
        
        choice_frame = tk.Frame(self.main_frame, bg="#1a1a1a")
        choice_frame.pack(pady=10)
        
        tk.Label(choice_frame, text="Bet on (number/red/black/even/odd):", 
                font=("Arial", 11), fg="#4DD0E1", bg="#1a1a1a").pack()
        
        choice_entry = tk.Entry(choice_frame, font=("Arial", 12), width=15, justify=tk.CENTER)
        choice_entry.pack(pady=5)
        
        result_label = tk.Label(self.main_frame, text="", font=("Arial", 12, "bold"),
                               fg="#FFD700", bg="#1a1a1a")
        result_label.pack(pady=20)
        
        def spin():
            try:
                bet = int(bet_entry.get())
                choice = choice_entry.get().lower()
                
                if bet <= 0 or bet > self.balance:
                    messagebox.showerror("Invalid Bet", f"Bet between 1 and ${self.balance}")
                    return
                
                winning_number = random.randint(0, 36)
                red_numbers = {1,3,5,7,9,12,14,16,18,19,21,23,25,27,30,32,34,36}
                
                if winning_number == 0:
                    color = "green"
                elif winning_number in red_numbers:
                    color = "red"
                else:
                    color = "black"
                
                odd_even = "even" if winning_number % 2 == 0 and winning_number != 0 else "odd"
                
                result_num_text = f"Winning Number: {winning_number} ({color}, {odd_even})\n"
                
                won = False
                if choice.isdigit() and int(choice) == winning_number:
                    won = True
                    winnings = bet * 35
                elif choice == color:
                    won = True
                    winnings = bet
                elif choice == odd_even:
                    won = True
                    winnings = bet
                
                if won:
                    self.play_sound('win')
                    self.balance += winnings
                    result_label.config(text=result_num_text + f"🎉 YOU WIN! ${winnings}", fg="#00FF00")
                else:
                    self.play_sound('lose')
                    self.balance -= bet
                    result_label.config(text=result_num_text + f"❌ YOU LOSE! -${bet}", fg="#FF6B6B")
                
                if self.balance <= 0:
                    self.root.after(2000, lambda: self.show_game_over("You've lost all your money!"))
            
            except ValueError:
                messagebox.showerror("Invalid Input", "Please enter valid input")
        
        tk.Button(self.main_frame, text="🎡 SPIN", font=("Arial", 12, "bold"),
                 bg="#4CAF50", fg="white", command=spin).pack(pady=10)
        
        tk.Button(self.main_frame, text="← Back to Menu", font=("Arial", 10),
                 bg="#666", fg="white", command=self.create_main_menu).pack(pady=5)
    
    def play_horse_racing(self):
        """Horse racing game"""
        self.clear_frame()
        self.create_header("🐴 Horse Racing")
        
        horses = ["🐴 Yellow", "🏃 Red", "💚 Green", "💙 Blue", "💜 Purple"]
        
        bet_frame = tk.Frame(self.main_frame, bg="#1a1a1a")
        bet_frame.pack(pady=10)
        
        tk.Label(bet_frame, text="Bet Amount:", font=("Arial", 12),
                fg="#4DD0E1", bg="#1a1a1a").pack(side=tk.LEFT, padx=5)
        
        bet_entry = tk.Entry(bet_frame, font=("Arial", 12), width=10, justify=tk.CENTER)
        bet_entry.pack(side=tk.LEFT, padx=5)
        
        horse_frame = tk.Frame(self.main_frame, bg="#1a1a1a")
        horse_frame.pack(pady=10)
        
        tk.Label(horse_frame, text="Choose a horse:", font=("Arial", 11),
                fg="#4DD0E1", bg="#1a1a1a").pack()
        
        choice_entry = tk.Entry(horse_frame, font=("Arial", 12), width=15, justify=tk.CENTER)
        choice_entry.pack(pady=5)
        
        for horse in horses:
            tk.Label(horse_frame, text=horse, font=("Arial", 10),
                    fg="#FFD700", bg="#1a1a1a").pack()
        
        result_label = tk.Label(self.main_frame, text="", font=("Arial", 12, "bold"),
                               fg="#FFD700", bg="#1a1a1a")
        result_label.pack(pady=20)
        
        def race():
            try:
                bet = int(bet_entry.get())
                choice = choice_entry.get().capitalize()
                
                if bet <= 0 or bet > self.balance:
                    messagebox.showerror("Invalid Bet", f"Bet between 1 and ${self.balance}")
                    return
                
                winning_horse = random.choice(horses).split()[-1]
                choice_clean = choice.split()[-1] if len(choice.split()) > 1 else choice
                
                result_num_text = f"Winning Horse: {winning_horse}\n"
                
                if choice_clean == winning_horse:
                    self.play_sound('win')
                    winnings = bet * 4
                    self.balance += winnings
                    result_label.config(text=result_num_text + f"🎉 YOU WIN! ${winnings}", fg="#00FF00")
                else:
                    self.play_sound('lose')
                    self.balance -= bet
                    result_label.config(text=result_num_text + f"❌ YOU LOSE! -${bet}", fg="#FF6B6B")
                
                if self.balance <= 0:
                    self.root.after(2000, lambda: self.show_game_over("You've lost all your money!"))
            
            except ValueError:
                messagebox.showerror("Invalid Input", "Please enter valid input")
        
        tk.Button(self.main_frame, text="🏁 RACE", font=("Arial", 12, "bold"),
                 bg="#4CAF50", fg="white", command=race).pack(pady=10)
        
        tk.Button(self.main_frame, text="← Back to Menu", font=("Arial", 10),
                 bg="#666", fg="white", command=self.create_main_menu).pack(pady=5)
    
    def run(self):
        """Start the game"""
        self.root.mainloop()

if __name__ == "__main__":
    game = CasinoGame()
    game.run()
