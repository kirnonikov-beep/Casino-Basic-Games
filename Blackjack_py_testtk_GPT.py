import random
import tkinter as tk
from tkinter import ttk, simpledialog, messagebox

try:
    import winsound
except ImportError:
    winsound = None


def play_click_sound():
    """Play a small click sound on Windows."""
    if winsound:
        winsound.Beep(700, 60)


class CasinoState:
    def __init__(self, initial_balance=100):
        self.balance = initial_balance
        self.debt = 0
        self.interest_rate = 0.12

    def change_balance(self, delta: int):
        self.balance += delta

    def take_loan(self, amount: int):
        self.debt += amount
        self.change_balance(amount)

    def repay_loan(self, amount: int) -> int:
        payment = min(amount, self.balance, self.debt)
        self.change_balance(-payment)
        self.debt -= payment
        return payment

    def add_interest(self):
        if self.debt > 0:
            self.debt += int(self.debt * self.interest_rate)


def create_shoe():
    """Create a shoe with 4 decks shuffled together."""
    deck = [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11]
    shoe = deck * 4
    random.shuffle(shoe)
    return shoe


def hand_value(cards):
    """Calculate the best blackjack value for a hand, accounting for Aces."""
    total = sum(cards)
    aces = cards.count(11)
    while total > 21 and aces:
        total -= 10
        aces -= 1
    return total


def card_label(cards):
    """Return a simple string representation of a hand."""
    return ", ".join(str(c) for c in cards)


class CasinoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Casino House")
        self.root.geometry("920x620")
        self.root.minsize(720, 520)
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=1)

        self.state = CasinoState(initial_balance=100)
        self.game_over = False

        self._build_header()
        self._build_notebook()
        self._build_game_frames()
        self._show_lobby()
        self._update_header()

    def _build_header(self):
        header = ttk.Frame(self.root, padding=8)
        header.grid(row=0, column=0, sticky="ew")
        header.columnconfigure(3, weight=1)

        ttk.Label(header, text="Balance:").grid(row=0, column=0, sticky="w")
        self.balance_var = tk.StringVar(value=str(self.state.balance))
        ttk.Label(header, textvariable=self.balance_var).grid(row=0, column=1, sticky="w")

        ttk.Label(header, text="Debt:").grid(row=0, column=2, sticky="e")
        self.debt_var = tk.StringVar(value=str(self.state.debt))
        ttk.Label(header, textvariable=self.debt_var).grid(row=0, column=3, sticky="w")

        self.loan_btn = ttk.Button(header, text="Take Loan", command=self._take_loan)
        self.loan_btn.grid(row=0, column=4, padx=6)
        self.repay_btn = ttk.Button(header, text="Repay", command=self._repay_loan)
        self.repay_btn.grid(row=0, column=5, padx=6)

    def _build_notebook(self):
        self.nb = ttk.Notebook(self.root)
        self.nb.grid(row=1, column=0, sticky="nsew")

        self.lobby_frame = ttk.Frame(self.nb)
        self.blackjack_frame = ttk.Frame(self.nb)
        self.slots_frame = ttk.Frame(self.nb)
        self.number_frame = ttk.Frame(self.nb)
        self.poker_frame = ttk.Frame(self.nb)
        self.roulette_frame = ttk.Frame(self.nb)
        self.horse_frame = ttk.Frame(self.nb)

        self.nb.add(self.lobby_frame, text="Lobby")
        self.nb.add(self.blackjack_frame, text="Blackjack")
        self.nb.add(self.slots_frame, text="Slots")
        self.nb.add(self.number_frame, text="Number Gamble")
        self.nb.add(self.poker_frame, text="Poker Dice")
        self.nb.add(self.roulette_frame, text="Roulette")
        self.nb.add(self.horse_frame, text="Horse Racing")

    def _build_game_frames(self):
        self._build_lobby()
        self.blackjack = BlackjackFrame(self.blackjack_frame, self)
        self.slots = SlotsFrame(self.slots_frame, self)
        self.number = NumberGambleFrame(self.number_frame, self)
        self.poker = PokerDiceFrame(self.poker_frame, self)
        self.roulette = RouletteFrame(self.roulette_frame, self)
        self.horse = HorseRacingFrame(self.horse_frame, self)

    def _build_lobby(self):
        style = ttk.Style(self.root)
        style.configure("Lobby.TFrame", background="#0B3D91")
        style.configure("Lobby.TLabel", background="#0B3D91", foreground="#FFD700", font=(None, 18, "bold"))
        style.configure("Lobby.TButton", font=(None, 12, "bold"))

        self.lobby_frame.configure(style="Lobby.TFrame")

        ttk.Label(self.lobby_frame, text="Welcome to The Gambling House", style="Lobby.TLabel").pack(pady=(18, 10))
        ttk.Label(
            self.lobby_frame,
            text="Choose a game and try to keep your bankroll alive!",
            style="Lobby.TLabel",
        ).pack(pady=(0, 22))

        btn_frame = ttk.Frame(self.lobby_frame, style="Lobby.TFrame")
        btn_frame.pack(pady=12)

        buttons = [
            ("Blackjack", lambda: self._select_tab(1)),
            ("Slots", lambda: self._select_tab(2)),
            ("Number Gamble", lambda: self._select_tab(3)),
            ("Poker Dice", lambda: self._select_tab(4)),
            ("Roulette", lambda: self._select_tab(5)),
            ("Horse Racing", lambda: self._select_tab(6)),
        ]

        for text, cmd in buttons:
            btn = ttk.Button(btn_frame, text=text, command=lambda c=cmd: (play_click_sound(), c()), style="Lobby.TButton")
            btn.pack(side="left", padx=8, pady=4)

        ttk.Label(
            self.lobby_frame,
            text="Tip: You can take a loan (with interest) if you run low.",
            style="Lobby.TLabel",
        ).pack(pady=(22, 0))

    def _select_tab(self, index):
        self.nb.select(index)

    def _show_lobby(self):
        self.nb.select(0)

    def _update_header(self):
        self.balance_var.set(str(self.state.balance))
        self.debt_var.set(str(self.state.debt))
        if self.state.balance <= 0 and self.state.debt <= 0:
            self._trigger_game_over()

    def _take_loan(self):
        if self.game_over:
            return
        amount = simpledialog.askinteger("Take Loan", "Loan amount:", minvalue=1, parent=self.root)
        if not amount:
            return
        if amount > 1000:
            messagebox.showinfo("Loan", "We only lend up to 1000 coins at the moment.")
            return
        self.state.take_loan(amount)
        self._update_header()
        messagebox.showinfo("Loan", f"Loan granted: {amount} coins. You now owe {self.state.debt} coins.")

    def _repay_loan(self):
        if self.state.debt <= 0:
            messagebox.showinfo("Repay", "You have no debt.")
            return
        amount = simpledialog.askinteger(
            "Repay Loan", f"Enter amount to repay (debt: {self.state.debt}):", minvalue=1, parent=self.root
        )
        if not amount:
            return
        paid = self.state.repay_loan(amount)
        self._update_header()
        messagebox.showinfo("Repay", f"Paid {paid} coins. Remaining debt: {self.state.debt}.")

    def _trigger_game_over(self):
        self.game_over = True
        messagebox.showinfo(
            "Game Over",
            "💸 GAME OVER! You've gone bankrupt!\n\n"
            "   ____   _   _  _   _  ____  \n"
            "  / ___| | | | || \\ | |/ ___| \n"
            "  \\___ \\ | | | ||  \\| |\\___ \\ \n"
            "   ___) || |_| || |\\  | ___) |\n"
            "  |____/  \\___/ |_| \\_|____/ \n\n"
            "Take a deep breath, then go to the Lobby and restart.",
        )

    def restart(self):
        self.state = CasinoState(initial_balance=100)
        self.game_over = False
        self._update_header()
        self._show_lobby()


class BlackjackFrame:
    def __init__(self, parent, app: CasinoApp):
        self.app = app
        self.parent = parent
        self.parent.columnconfigure(0, weight=1)
        self.parent.rowconfigure(0, weight=0)
        self.parent.rowconfigure(1, weight=1)

        self.message_var = tk.StringVar(value="Place your bet and deal.")

        self._build_ui()
        self.reset_round()

    def _build_ui(self):
        top = ttk.Frame(self.parent, padding=8)
        top.grid(row=0, column=0, sticky="ew")
        top.columnconfigure(4, weight=1)

        ttk.Label(top, text="Bet:").grid(row=0, column=0, sticky="w")
        self.bet_var = tk.StringVar(value="0")
        ttk.Entry(top, textvariable=self.bet_var, width=8).grid(row=0, column=1, sticky="w", padx=4)

        ttk.Button(top, text="Deal", command=lambda: (play_click_sound(), self._deal())).grid(row=0, column=2, padx=6)
        ttk.Button(top, text="Lobby", command=lambda: (play_click_sound(), self.app._show_lobby())).grid(
            row=0, column=3, padx=6
        )

        ttk.Label(top, textvariable=self.message_var).grid(row=1, column=0, columnspan=5, sticky="w", pady=(8, 0))

        board = ttk.Frame(self.parent, padding=8)
        board.grid(row=1, column=0, sticky="nsew")
        board.columnconfigure(0, weight=1)
        board.columnconfigure(1, weight=1)

        self.dealer_frame = ttk.LabelFrame(board, text="Dealer")
        self.dealer_frame.grid(row=0, column=0, sticky="nsew", padx=8, pady=4)
        self.player_frame = ttk.LabelFrame(board, text="Player")
        self.player_frame.grid(row=0, column=1, sticky="nsew", padx=8, pady=4)

        self.dealer_cards_var = tk.StringVar(value="")
        self.dealer_total_var = tk.StringVar(value="")
        ttk.Label(self.dealer_frame, textvariable=self.dealer_cards_var).pack(anchor="w")
        ttk.Label(self.dealer_frame, textvariable=self.dealer_total_var).pack(anchor="w")

        self.player_cards_var = tk.StringVar(value="")
        self.player_total_var = tk.StringVar(value="")
        ttk.Label(self.player_frame, textvariable=self.player_cards_var).pack(anchor="w")
        ttk.Label(self.player_frame, textvariable=self.player_total_var).pack(anchor="w")

        actions = ttk.Frame(self.parent, padding=8)
        actions.grid(row=2, column=0, sticky="ew")
        actions.columnconfigure(5, weight=1)

        self.hit_btn = ttk.Button(actions, text="Hit", command=lambda: (play_click_sound(), self._hit()))
        self.stand_btn = ttk.Button(actions, text="Stand", command=lambda: (play_click_sound(), self._stand()))
        self.double_btn = ttk.Button(actions, text="Double", command=lambda: (play_click_sound(), self._double()))
        self.split_btn = ttk.Button(actions, text="Split", command=lambda: (play_click_sound(), self._split()))
        self.restart_btn = ttk.Button(actions, text="Restart", command=lambda: (play_click_sound(), self.app.restart()))

        self.hit_btn.grid(row=0, column=0, padx=4)
        self.stand_btn.grid(row=0, column=1, padx=4)
        self.double_btn.grid(row=0, column=2, padx=4)
        self.split_btn.grid(row=0, column=3, padx=4)
        self.restart_btn.grid(row=0, column=4, padx=4)

        self._set_button_state(enabled=False)

    def _set_button_state(self, enabled: bool):
        state = "normal" if enabled else "disabled"
        self.hit_btn.config(state=state)
        self.stand_btn.config(state=state)
        self.double_btn.config(state=state)
        self.split_btn.config(state=state)

    def reset_round(self):
        self.shoe = create_shoe()
        self.player_hand = []
        self.dealer_hand = []
        self.split_hand = None
        self.current_hand = "player"
        self.bet = 0
        self.split_bet = 0
        self.message_var.set("Place your bet and deal.")
        self._update_board()

    def _update_board(self):
        self.dealer_cards_var.set(f"Cards: {card_label(self.dealer_hand)}")
        self.dealer_total_var.set(f"Total: {hand_value(self.dealer_hand)}")
        self.player_cards_var.set(f"Cards: {card_label(self.player_hand)}")
        self.player_total_var.set(f"Total: {hand_value(self.player_hand)}")
        self.app._update_header()

    def _draw_card(self):
        if len(self.shoe) < 10:
            self.shoe = create_shoe()
        return self.shoe.pop()

    def _deal(self):
        if self.app.game_over:
            return
        try:
            bet = int(self.bet_var.get())
        except ValueError:
            self.message_var.set("Enter a valid bet.")
            return
        if bet <= 0:
            self.message_var.set("Bet must be > 0.")
            return
        if bet > self.app.state.balance:
            self.message_var.set("Not enough balance. Consider taking a loan.")
            return

        self.bet = bet
        self.app.state.change_balance(-bet)
        self.player_hand = [self._draw_card(), self._draw_card()]
        self.dealer_hand = [self._draw_card(), self._draw_card()]
        self.split_hand = None
        self.split_bet = 0
        self.current_hand = "player"

        pt = hand_value(self.player_hand)
        dt = hand_value(self.dealer_hand)
        if pt == 21 or dt == 21:
            if pt == 21 and dt != 21:
                self.app.state.change_balance(int(self.bet * 2.5))
                self.message_var.set("Blackjack! You win 3:2.")
            elif dt == 21 and pt != 21:
                self.message_var.set("Dealer has Blackjack. You lose.")
            else:
                self.app.state.change_balance(self.bet)
                self.message_var.set("Push (tie).")
            self._set_button_state(False)
            self._check_game_over()
            self._update_board()
            return

        self.message_var.set("Hit / Stand / Double / Split")
        self._set_button_state(True)
        self._update_board()

    def _active_hand(self):
        if self.current_hand == "split" and self.split_hand is not None:
            return self.split_hand
        return self.player_hand

    def _hit(self):
        hand = self._active_hand()
        hand.append(self._draw_card())
        if hand_value(hand) > 21:
            self.message_var.set("Busted!")
            self._settle_round()
        else:
            self.message_var.set("Hit or Stand?")
        self._update_board()

    def _stand(self):
        self._settle_round()

    def _double(self):
        if self.bet > self.app.state.balance:
            self.message_var.set("Not enough balance to double.")
            return
        self.app.state.change_balance(-self.bet)
        self.bet *= 2
        self.player_hand.append(self._draw_card())
        self._settle_round()

    def _split(self):
        if len(self.player_hand) != 2 or self.player_hand[0] != self.player_hand[1]:
            self.message_var.set("Can only split matching cards.")
            return
        if self.bet > self.app.state.balance:
            self.message_var.set("Not enough for split.")
            return
        self.app.state.change_balance(-self.bet)
        self.split_bet = self.bet
        self.split_hand = [self.player_hand.pop(), self._draw_card()]
        self.player_hand.append(self._draw_card())
        self.message_var.set("Split! Play first hand.")
        self._update_board()

    def _settle_round(self):
        dealer_total = hand_value(self.dealer_hand)
        while dealer_total < 17:
            self.dealer_hand.append(self._draw_card())
            dealer_total = hand_value(self.dealer_hand)

        def score(hand, bet, label):
            total = hand_value(hand)
            if total > 21:
                return 0, f"{label}: Busted."
            if dealer_total > 21:
                return bet * 2, f"{label}: Dealer busted!"
            if total > dealer_total:
                return bet * 2, f"{label}: You win!"
            if total == dealer_total:
                return bet, f"{label}: Push."
            return 0, f"{label}: Dealer wins."

        results = [score(self.player_hand, self.bet, "Hand 1")]
        if self.split_hand is not None:
            results.append(score(self.split_hand, self.split_bet, "Hand 2"))

        total_gain = sum(r[0] for r in results)
        self.app.state.change_balance(total_gain)
        self.message_var.set(" | ".join(r[1] for r in results))
        self._set_button_state(False)
        self._check_game_over()
        self._update_board()

    def _check_game_over(self):
        if self.app.state.balance <= 0 and self.app.state.debt <= 0:
            self.app._trigger_game_over()


class SlotsFrame:
    def __init__(self, parent, app: CasinoApp):
        self.app = app
        self.parent = parent
        self._build_ui()

    def _build_ui(self):
        frame = ttk.Frame(self.parent, padding=12)
        frame.pack(fill="both", expand=True)

        ttk.Label(frame, text="Slot Machine", font=(None, 16, "bold")).pack(pady=8)
        self.result_var = tk.StringVar(value="Place a bet and spin.")
        ttk.Label(frame, textvariable=self.result_var, wraplength=500).pack(pady=6)

        control = ttk.Frame(frame)
        control.pack(pady=6)
        ttk.Label(control, text="Bet:").grid(row=0, column=0)
        self.bet_var = tk.StringVar(value="0")
        ttk.Entry(control, textvariable=self.bet_var, width=6).grid(row=0, column=1, padx=4)
        ttk.Button(control, text="Spin", command=lambda: (play_click_sound(), self.spin())).grid(row=0, column=2, padx=8)

    def spin(self):
        if self.app.game_over:
            return
        try:
            bet = int(self.bet_var.get())
        except ValueError:
            self.result_var.set("Enter a valid bet.")
            return
        if bet <= 0 or bet > self.app.state.balance:
            self.result_var.set("Invalid bet.")
            return

        self.app.state.change_balance(-bet)
        symbols = ["Cherry", "Lemon", "Orange", "Bell", "Seven"]
        lines = [[random.choice(symbols) for _ in range(3)] for _ in range(3)]
        display = "\n".join("  ".join(r) for r in lines)
        self.result_var.set(display)

        winnings = 0
        if len({*lines[1]}) == 1:
            winnings = bet * 5
        elif len({*lines[0]}) == 1 or len({*lines[2]}) == 1:
            winnings = bet * 3
        elif len({*lines[1]}) == 2:
            winnings = bet * 2

        if winnings > 0:
            self.app.state.change_balance(winnings)
            self.result_var.set(self.result_var.get() + f"\nYou win {winnings} coins!")
        else:
            self.result_var.set(self.result_var.get() + f"\nYou lose {bet} coins.")

        self.app._update_header()
        self.app._check_game_over()


class NumberGambleFrame:
    def __init__(self, parent, app: CasinoApp):
        self.app = app
        self.parent = parent
        self._build_ui()

    def _build_ui(self):
        frame = ttk.Frame(self.parent, padding=12)
        frame.pack(fill="both", expand=True)

        ttk.Label(frame, text="Number Gamble", font=(None, 16, "bold")).pack(pady=8)
        self.result_var = tk.StringVar(value="Pick a number 1-10 and bet.")
        ttk.Label(frame, textvariable=self.result_var, wraplength=500).pack(pady=6)

        control = ttk.Frame(frame)
        control.pack(pady=6)

        ttk.Label(control, text="Bet:").grid(row=0, column=0)
        self.bet_var = tk.StringVar(value="0")
        ttk.Entry(control, textvariable=self.bet_var, width=6).grid(row=0, column=1, padx=4)
        ttk.Label(control, text="Number:").grid(row=0, column=2, padx=(14, 0))
        self.number_var = tk.StringVar(value="1")
        ttk.Entry(control, textvariable=self.number_var, width=4).grid(row=0, column=3, padx=4)

        ttk.Button(frame, text="Play", command=lambda: (play_click_sound(), self.play())).pack(pady=10)

    def play(self):
        if self.app.game_over:
            return
        try:
            bet = int(self.bet_var.get())
            choice = int(self.number_var.get())
        except ValueError:
            self.result_var.set("Enter valid numbers.")
            return
        if bet <= 0 or bet > self.app.state.balance or not (1 <= choice <= 10):
            self.result_var.set("Invalid bet/number.")
            return

        self.app.state.change_balance(-bet)
        secret = random.randint(1, 10)
        if choice == secret:
            winnings = bet
            self.app.state.change_balance(winnings)
            self.result_var.set(f"You chose {choice}, computer {secret}. You win {winnings} coins!")
        else:
            self.result_var.set(f"You chose {choice}, computer {secret}. You lose {bet} coins.")

        self.app._update_header()
        self.app._check_game_over()


class PokerDiceFrame:
    def __init__(self, parent, app: CasinoApp):
        self.app = app
        self.parent = parent
        self._build_ui()

    def _build_ui(self):
        frame = ttk.Frame(self.parent, padding=12)
        frame.pack(fill="both", expand=True)

        ttk.Label(frame, text="Poker Dice", font=(None, 16, "bold")).pack(pady=8)
        self.result_var = tk.StringVar(value="Roll five dice and see what you get.")
        ttk.Label(frame, textvariable=self.result_var, wraplength=500).pack(pady=6)

        control = ttk.Frame(frame)
        control.pack(pady=6)
        ttk.Label(control, text="Bet:").grid(row=0, column=0)
        self.bet_var = tk.StringVar(value="0")
        ttk.Entry(control, textvariable=self.bet_var, width=6).grid(row=0, column=1, padx=4)
        ttk.Button(frame, text="Roll", command=lambda: (play_click_sound(), self.roll())).pack(pady=10)

    def roll(self):
        if self.app.game_over:
            return
        try:
            bet = int(self.bet_var.get())
        except ValueError:
            self.result_var.set("Invalid bet.")
            return
        if bet <= 0 or bet > self.app.state.balance:
            self.result_var.set("Invalid bet.")
            return

        self.app.state.change_balance(-bet)
        dice = [random.randint(1, 6) for _ in range(5)]
        counts = {v: dice.count(v) for v in set(dice)}
        freq = sorted(counts.values(), reverse=True)
        unique = sorted(set(dice))

        if freq == [5]:
            category = "Five of a kind"
            payout = 10
        elif freq == [4, 1]:
            category = "Four of a kind"
            payout = 7
        elif freq == [3, 2]:
            category = "Full house"
            payout = 5
        elif unique in ([1, 2, 3, 4, 5], [2, 3, 4, 5, 6]):
            category = "Straight"
            payout = 3
        elif freq == [3, 1, 1]:
            category = "Three of a kind"
            payout = 2
        elif freq == [2, 2, 1]:
            category = "Two pairs"
            payout = 1.1
        elif freq == [2, 1, 1, 1]:
            category = "One pair"
            payout = 0
        else:
            category = "Nothing"
            payout = 0

        winnings = int(bet * payout)
        self.app.state.change_balance(winnings)
        self.result_var.set(
            f"Roll: {dice} -> {category}. Payout: {winnings} coins (x{payout})."
        )
        self.app._update_header()
        self.app._check_game_over()


class RouletteFrame:
    def __init__(self, parent, app: CasinoApp):
        self.app = app
        self.parent = parent
        self._build_ui()

    def _build_ui(self):
        frame = ttk.Frame(self.parent, padding=12)
        frame.pack(fill="both", expand=True)

        ttk.Label(frame, text="Roulette", font=(None, 16, "bold")).pack(pady=8)
        self.result_var = tk.StringVar(value="Bet on number, color, even/odd.")
        ttk.Label(frame, textvariable=self.result_var, wraplength=500).pack(pady=6)

        control = ttk.Frame(frame)
        control.pack(pady=6)
        ttk.Label(control, text="Bet:").grid(row=0, column=0)
        self.bet_var = tk.StringVar(value="0")
        ttk.Entry(control, textvariable=self.bet_var, width=6).grid(row=0, column=1, padx=4)

        ttk.Label(control, text="Choice:").grid(row=0, column=2, padx=(12, 0))
        self.choice_var = tk.StringVar(value="red")
        choices = ["red", "black", "even", "odd"] + [str(i) for i in range(37)]
        self.choice_menu = ttk.Combobox(control, textvariable=self.choice_var, values=choices, width=10)
        self.choice_menu.grid(row=0, column=3, padx=4)
        self.choice_menu.set("red")

        ttk.Button(frame, text="Spin", command=lambda: (play_click_sound(), self.spin())).pack(pady=10)

    def spin(self):
        if self.app.game_over:
            return
        try:
            bet = int(self.bet_var.get())
        except ValueError:
            self.result_var.set("Invalid bet.")
            return
        if bet <= 0 or bet > self.app.state.balance:
            self.result_var.set("Invalid bet.")
            return

        self.app.state.change_balance(-bet)
        winning = random.randint(0, 36)
        red_numbers = {1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36}
        color = "green" if winning == 0 else "red" if winning in red_numbers else "black"
        parity = "even" if winning != 0 and winning % 2 == 0 else "odd"

        choice = self.choice_var.get().lower()
        payout = 0
        win_msg = ""

        if choice.isdigit():
            if int(choice) == winning:
                payout = bet * 35
                win_msg = "Hit the number!"
        elif choice == color:
            payout = bet
            win_msg = f"Color {color} hit!"
        elif choice in ("even", "odd") and winning != 0 and parity == choice:
            payout = bet
            win_msg = f"{choice.title()} hits!"

        self.app.state.change_balance(payout)
        self.result_var.set(
            f"{winning} ({color}, {parity}). {win_msg} You {'win' if payout>0 else 'lose'} {payout if payout>0 else bet} coins."
        )
        self.app._update_header()
        self.app._check_game_over()


class HorseRacingFrame:
    def __init__(self, parent, app: CasinoApp):
        self.app = app
        self.parent = parent
        self._build_ui()

    def _build_ui(self):
        frame = ttk.Frame(self.parent, padding=12)
        frame.pack(fill="both", expand=True)

        ttk.Label(frame, text="Horse Racing", font=(None, 16, "bold")).pack(pady=8)
        self.result_var = tk.StringVar(value="Pick a horse and bet.")
        ttk.Label(frame, textvariable=self.result_var, wraplength=500).pack(pady=6)

        control = ttk.Frame(frame)
        control.pack(pady=6)
        ttk.Label(control, text="Bet:").grid(row=0, column=0)
        self.bet_var = tk.StringVar(value="0")
        ttk.Entry(control, textvariable=self.bet_var, width=6).grid(row=0, column=1, padx=4)

        horses = ["Yellow", "Red", "Green", "Blue", "Purple"]
        ttk.Label(control, text="Horse:").grid(row=0, column=2, padx=(12, 0))
        self.horse_var = tk.StringVar(value=horses[0])
        self.horse_menu = ttk.Combobox(control, values=horses, textvariable=self.horse_var, width=10)
        self.horse_menu.grid(row=0, column=3, padx=4)

        ttk.Button(frame, text="Race", command=lambda: (play_click_sound(), self.race())).pack(pady=10)

    def race(self):
        if self.app.game_over:
            return
        try:
            bet = int(self.bet_var.get())
        except ValueError:
            self.result_var.set("Invalid bet.")
            return
        if bet <= 0 or bet > self.app.state.balance:
            self.result_var.set("Invalid bet.")
            return

        self.app.state.change_balance(-bet)
        horses = ["Yellow", "Red", "Green", "Blue", "Purple"]
        winner = random.choice(horses)
        if self.horse_var.get() == winner:
            payout = bet * 4
            self.app.state.change_balance(payout)
            self.result_var.set(f"{winner} won! You win {payout} coins.")
        else:
            self.result_var.set(f"{winner} won. You lose {bet} coins.")

        self.app._update_header()
        self.app._check_game_over()


if __name__ == "__main__":
    root = tk.Tk()
    app = CasinoApp(root)
    root.mainloop()
