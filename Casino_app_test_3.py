import random
import tkinter as tk
from tkinter import messagebox

# ---------- HELPERS ----------

def create_shoe():
    deck = [2,3,4,5,6,7,8,9,10,10,10,10,11]
    shoe = deck * 4
    random.shuffle(shoe)
    return shoe

# ---------- MAIN APP ----------

class CasinoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Casino App")

        self.balance = 100
        self.bet = 10

        self.frame = tk.Frame(root)
        self.frame.pack()

        self.show_menu()

    def clear_screen(self):
        for widget in self.frame.winfo_children():
            widget.destroy()

    # ---------- MENU ----------

    def show_menu(self):
        self.clear_screen()

        tk.Label(self.frame, text=f"Balance: {self.balance}", font=("Arial", 16)).pack(pady=10)
        tk.Label(self.frame, text="Casino Menu", font=("Arial", 20)).pack(pady=10)

        tk.Button(self.frame, text="Blackjack", width=20, command=self.blackjack_screen).pack(pady=5)
        tk.Button(self.frame, text="Slot Machine", width=20, command=self.slot_screen).pack(pady=5)
        tk.Button(self.frame, text="Quit", width=20, command=self.root.quit).pack(pady=5)

    # ---------- BLACKJACK ----------

    def blackjack_screen(self):
        self.clear_screen()

        self.shoe = create_shoe()
        self.player_hand = [self.draw(), self.draw()]
        self.dealer_hand = [self.draw(), self.draw()]

        self.info = tk.Label(self.frame, text="Blackjack", font=("Arial", 16))
        self.info.pack()

        self.player_label = tk.Label(self.frame)
        self.player_label.pack()

        self.dealer_label = tk.Label(self.frame)
        self.dealer_label.pack()

        self.update_bj_labels(False)

        tk.Button(self.frame, text="Hit", command=self.hit).pack(pady=5)
        tk.Button(self.frame, text="Stand", command=self.stand).pack(pady=5)
        tk.Button(self.frame, text="Back to Menu", command=self.show_menu).pack(pady=10)

    def draw(self):
        if len(self.shoe) < 10:
            self.shoe = create_shoe()
        return self.shoe.pop()

    def hit(self):
        self.player_hand.append(self.draw())
        self.adjust_ace(self.player_hand)

        if sum(self.player_hand) > 21:
            self.update_bj_labels(True)
            self.end_bj("Bust! You lose.", False)
        else:
            self.update_bj_labels(False)

    def stand(self):
        while sum(self.dealer_hand) < 17:
            self.dealer_hand.append(self.draw())
            self.adjust_ace(self.dealer_hand)

        self.update_bj_labels(True)

        p = sum(self.player_hand)
        d = sum(self.dealer_hand)

        if d > 21 or p > d:
            self.end_bj("You win!", True)
        elif p == d:
            self.end_bj("Tie!", None)
        else:
            self.end_bj("Dealer wins.", False)

    def adjust_ace(self, hand):
        while sum(hand) > 21 and 11 in hand:
            hand[hand.index(11)] = 1

    def update_bj_labels(self, show_dealer):
        self.player_label.config(text=f"Player: {self.player_hand} ({sum(self.player_hand)})")

        if show_dealer:
            self.dealer_label.config(text=f"Dealer: {self.dealer_hand} ({sum(self.dealer_hand)})")
        else:
            self.dealer_label.config(text=f"Dealer: [{self.dealer_hand[0]}, ?]")

    def end_bj(self, msg, win):
        if win is True:
            self.balance += self.bet
        elif win is False:
            self.balance -= self.bet

        messagebox.showinfo("Result", msg)
        self.show_menu()

    # ---------- SLOT MACHINE ----------

    def slot_screen(self):
        self.clear_screen()

        tk.Label(self.frame, text="Slot Machine", font=("Arial", 16)).pack(pady=10)

        self.slot_result = tk.Label(self.frame, text="--- --- ---", font=("Arial", 20))
        self.slot_result.pack(pady=10)

        tk.Button(self.frame, text="Spin", command=self.spin).pack(pady=5)
        tk.Button(self.frame, text="Back to Menu", command=self.show_menu).pack(pady=10)

    def spin(self):
        symbols = ["🍒", "🍋", "🔔", "⭐", "7"]

        result = [random.choice(symbols) for _ in range(3)]
        self.slot_result.config(text=" ".join(result))

        if result[0] == result[1] == result[2]:
            self.balance += self.bet * 3
            messagebox.showinfo("Win!", "Jackpot!")
        elif len(set(result)) == 2:
            self.balance += self.bet
            messagebox.showinfo("Win!", "Small win!")
        else:
            self.balance -= self.bet
            messagebox.showinfo("Lose", "Try again!")

        self.show_menu()

# ---------- RUN ----------

root = tk.Tk()
root.geometry("300x300")
app = CasinoApp(root)
root.mainloop()