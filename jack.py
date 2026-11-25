import tkinter as tk
from random import choice, randint

class BlackjackGUI:
    
    #A Blackjack game implemented using Tkinter, featuring proper Ace handling,
    #visual card representation (Unicode symbols), and the unique Joker rule:
    #a Joker raises the player's non-bust limit from 21 to 22 while having a value of -1.
    
    
    def __init__(self, master):
        self.master = master
        master.title("Blackjack")
        
        # Aesthetic setup
        self.BACKGROUND_COLOR = "#0C302B" # Dark Teal/Green for card table feel
        self.TEXT_COLOR = "#EFEFEF"       # Off-white
        self.BTN_COLOR = "#FFD700"        # Gold/Yellow
        self.BTN_ACTIVE_COLOR = "#FFA500" # Orange
        self.RULE_BG_COLOR = "#214F4A"    # Slightly different dark color for rules pane
        
        master.configure(bg=self.BACKGROUND_COLOR)
        
        # Configure master grid to support two main sections (Game and Rules)
        master.grid_columnconfigure(0, weight=3) # Game area is wider
        master.grid_columnconfigure(1, weight=1) # Rules area is narrower
        master.grid_rowconfigure(0, weight=1)
        
        # Card representation (simulating a deck for random draw)
        self.card_map = {
            '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10,
            'J': 10, 'Q': 10, 'K': 10, 'A': 11, 'JK': -1 # Joker (JK) now has a value of -1
        }
        self.ranks = list(self.card_map.keys())
        self.suits = ['♠', '♥', '♦', '♣'] 
        
        # Game variables
        self.player_total = 0
        self.dealer_total = 0
        self.player_cards = []  # Stores list of (rank_str, suit_char) tuples
        self.dealer_cards = []  # Stores list of (rank_str, suit_char) tuples
        self.game_over = False

        # --- Game UI Frame (Left Side) ---
        self.game_frame = tk.Frame(master, bg=self.BACKGROUND_COLOR)
        self.game_frame.grid(row=0, column=0, padx=(20, 10), pady=20, sticky="nsew")

        # Dealer Section
        self.dealer_label = tk.Label(self.game_frame, text="Dealer Hand:", font=("Arial", 16, "bold"), bg=self.BACKGROUND_COLOR, fg=self.TEXT_COLOR)
        self.dealer_label.grid(row=0, column=0, columnspan=2, pady=(0, 0))
        
        self.dealer_cards_frame = tk.Frame(self.game_frame, bg=self.BACKGROUND_COLOR)
        self.dealer_cards_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=5)
        
        self.dealer_total_label = tk.Label(self.game_frame, text="Total: ?", font=("Arial", 14), bg=self.BACKGROUND_COLOR, fg=self.TEXT_COLOR)
        self.dealer_total_label.grid(row=2, column=0, columnspan=2, pady=(0, 15))

        # Player Section
        self.player_label = tk.Label(self.game_frame, text="Player Hand:", font=("Arial", 16, "bold"), bg=self.BACKGROUND_COLOR, fg=self.TEXT_COLOR)
        self.player_label.grid(row=3, column=0, columnspan=2, pady=(15, 0))
        
        self.player_cards_frame = tk.Frame(self.game_frame, bg=self.BACKGROUND_COLOR)
        self.player_cards_frame.grid(row=4, column=0, columnspan=2, padx=10, pady=5)
        
        self.player_total_label = tk.Label(self.game_frame, text="Total: 0", font=("Arial", 14), bg=self.BACKGROUND_COLOR, fg=self.TEXT_COLOR)
        self.player_total_label.grid(row=5, column=0, columnspan=2, pady=(0, 15))

        # Result Label
        self.result_label = tk.Label(self.game_frame, text="", font=("Arial", 18, "bold"), bg=self.BACKGROUND_COLOR, fg="#FF0000")
        self.result_label.grid(row=6, column=0, columnspan=2, padx=10, pady=15)
        
        # Button Frame (Action buttons)
        self.btn_frame = tk.Frame(self.game_frame, bg=self.BACKGROUND_COLOR)
        self.btn_frame.grid(row=7, column=0, columnspan=2, padx=10, pady=10)
        
        self.hit_button = tk.Button(self.btn_frame, text="Hit", command=self.hit, width=12, bg=self.BTN_COLOR, activebackground=self.BTN_ACTIVE_COLOR, font=("Arial", 12, "bold"))
        self.hit_button.pack(side=tk.LEFT, padx=5)
        
        self.stick_button = tk.Button(self.btn_frame, text="Stand", command=self.stick, width=12, bg=self.BTN_COLOR, activebackground=self.BTN_ACTIVE_COLOR, font=("Arial", 12, "bold"))
        self.stick_button.pack(side=tk.LEFT, padx=5)
        
        self.double_button = tk.Button(self.btn_frame, text="Double Down", command=self.double_down, width=12, bg=self.BTN_COLOR, activebackground=self.BTN_ACTIVE_COLOR, font=("Arial", 12, "bold"))
        self.double_button.pack(side=tk.LEFT, padx=5)

        # New Fold Button
        self.fold_button = tk.Button(self.btn_frame, text="Fold (Quit)", command=self.fold_game, width=12, bg="#FF4500", activebackground="#E9967A", fg="white", font=("Arial", 12, "bold"))
        self.fold_button.pack(side=tk.LEFT, padx=5)
        
        self.new_game_button = tk.Button(self.game_frame, text="New Game", command=self.new_game, width=20, bg="#4CAF50", activebackground="#66BB6A", fg="white", font=("Arial", 12, "bold"))
        self.new_game_button.grid(row=8, column=0, columnspan=2, padx=10, pady=15)

        # --- Rule Board Frame (Right Side) ---
        self.rules_frame = tk.Frame(master, bg=self.RULE_BG_COLOR, padx=15, pady=15, relief=tk.RIDGE, bd=3)
        self.rules_frame.grid(row=0, column=1, padx=(10, 20), pady=20, sticky="nsew")
        
        # Rule Board Content
        rules_title = tk.Label(self.rules_frame, text="GAME RULES", font=("Arial", 16, "bold"), bg=self.RULE_BG_COLOR, fg="#FFD700")
        rules_title.pack(pady=(0, 10))

        # --- General Rules ---
        tk.Label(self.rules_frame, text="1. Basic Objective", font=("Arial", 13, "bold"), anchor="w", justify=tk.LEFT, bg=self.RULE_BG_COLOR, fg=self.TEXT_COLOR).pack(fill='x')
        tk.Label(self.rules_frame, text="Get your total higher than the Dealer's without exceeding 21 (or 22 with Joker).", font=("Arial", 10), anchor="w", justify=tk.LEFT, wraplength=200, bg=self.RULE_BG_COLOR, fg=self.TEXT_COLOR).pack(fill='x', pady=(0, 10))

        tk.Label(self.rules_frame, text="2. Standard Card Values", font=("Arial", 13, "bold"), anchor="w", justify=tk.LEFT, bg=self.RULE_BG_COLOR, fg=self.TEXT_COLOR).pack(fill='x')
        tk.Label(self.rules_frame, text="• 2-10: Face Value.\n• J, Q, K: 10 points.", font=("Arial", 10), anchor="w", justify=tk.LEFT, bg=self.RULE_BG_COLOR, fg=self.TEXT_COLOR).pack(fill='x', pady=(0, 10))
        
        # --- Special Rules ---
        
        # Rule 3: Ace Value
        tk.Label(self.rules_frame, text="3. Ace Value (1 or 11)", font=("Arial", 13, "bold"), anchor="w", justify=tk.LEFT, bg=self.RULE_BG_COLOR, fg=self.TEXT_COLOR).pack(fill='x')
        tk.Label(self.rules_frame, text="• Ace counts as 11, reducing to 1 if the hand total exceeds the max limit (21 or 22).", font=("Arial", 10), anchor="w", justify=tk.LEFT, bg=self.RULE_BG_COLOR, fg=self.TEXT_COLOR).pack(fill='x', pady=(0, 10))

        # Rule 4: Joker 22 (Updated)
        tk.Label(self.rules_frame, text="4. 🃏 Joker Advantage (Value: -1)", font=("Arial", 13, "bold"), anchor="w", justify=tk.LEFT, bg=self.RULE_BG_COLOR, fg=self.TEXT_COLOR).pack(fill='x')
        tk.Label(self.rules_frame, text="• Joker ('JK') counts as -1 point.\n• Player's hand with a Joker is non-bust up to 22.", font=("Arial", 10), anchor="w", justify=tk.LEFT, bg=self.RULE_BG_COLOR, fg=self.TEXT_COLOR).pack(fill='x', pady=(0, 10))

        # Rule 5: Dealer's Play Rule
        tk.Label(self.rules_frame, text="5. Dealer's Play Rule", font=("Arial", 13, "bold"), anchor="w", justify=tk.LEFT, bg=self.RULE_BG_COLOR, fg=self.TEXT_COLOR).pack(fill='x')
        tk.Label(self.rules_frame, text="• Dealer must Hit on 16 or less.\n• Exception: Dealer has a 50% chance to STAND on 16 (hard or soft).", font=("Arial", 10), anchor="w", justify=tk.LEFT, bg=self.RULE_BG_COLOR, fg=self.TEXT_COLOR).pack(fill='x', pady=(0, 10))

        # Rule 6: Player Actions
        tk.Label(self.rules_frame, text="6. Player Actions", font=("Arial", 13, "bold"), anchor="w", justify=tk.LEFT, bg=self.RULE_BG_COLOR, fg=self.TEXT_COLOR).pack(fill='x')
        tk.Label(self.rules_frame, text="• Double Down takes 2 cards then stands.\n• Fold (Quit) immediately closes the game.", font=("Arial", 10), anchor="w", justify=tk.LEFT, bg=self.RULE_BG_COLOR, fg=self.TEXT_COLOR).pack(fill='x')

        # Initial Deal
        self.deal()

    def draw_card(self):
        """Draws a random card as a (rank_str, suit_char) tuple or ('JK', 'JOKER')."""
        rank = choice(self.ranks)
        if rank == 'JK':
            # Joker has no standard suit, using an emoji for identification
            suit = '🃏'
        else:
            suit = choice(self.suits)
        return (rank, suit)
        
    def has_joker(self, cards):
        """Checks if a hand contains a Joker."""
        return any(rank == 'JK' for rank, _ in cards)

    def calculate_total(self, cards):
        """
        Calculates the hand total. Aces start as 11 and are reduced to 1 if the total busts.
        Jokers (JK) are now calculated as -1 and are NOT adjustable.
        """
        total = 0
        num_adjustable_cards = 0 # Counts only Aces
        
        for rank, _ in cards:
            if rank == 'A':
                num_adjustable_cards += 1
                total += 11 # Start by counting Ace as 11
            elif rank == 'JK':
                # Use the fixed -1 value for Joker
                total += self.card_map[rank]
            else:
                total += self.card_map[rank]

        # Adjust Aces from 11 to 1 if busting
        while total > 21 and num_adjustable_cards > 0:
            total -= 10
            num_adjustable_cards -= 1

        return total
    
    def display_cards(self, card_list, frame, hide_first=False):
        """Creates and packs individual card labels into the given frame."""
        # Clear existing cards
        for widget in frame.winfo_children():
            widget.destroy()

        for i, (rank, suit) in enumerate(card_list):
            is_hidden = hide_first and i == 0
            
            card_text = '??' if is_hidden else (f'{rank}\n{suit}' if rank != 'JK' else 'JK\n🃏')
            
            # Card color logic
            if is_hidden:
                card_bg = 'grey' # Hidden card has a grey background
                card_fg = 'black' # Hidden card text is black
            else:
                if rank == 'JK':
                    card_bg = '#8B008B' # Dark Magenta for Joker
                    card_fg = 'white'
                else:
                    # Visible standard card
                    card_bg = 'red' if suit in ['♥', '♦'] else 'black'
                    card_fg = 'white' 
            
            # Create the card label
            label = tk.Label(frame, 
                             text=card_text, 
                             font=("Arial", 24, "bold"), 
                             bg=card_bg, 
                             fg=card_fg,
                             width=4, height=3, 
                             relief=tk.RAISED, borderwidth=3,
                             padx=5, pady=5)
            label.pack(side=tk.LEFT, padx=5, pady=5)
        
    def update_labels(self, hide_dealer_card=True):
        """Updates all card displays and total labels."""
        
        # Player update
        self.player_total = self.calculate_total(self.player_cards)
        self.player_total_label.config(text=f"Total: {self.player_total}")
        self.display_cards(self.player_cards, self.player_cards_frame)

        # Dealer update
        self.display_cards(self.dealer_cards, self.dealer_cards_frame, hide_first=hide_dealer_card and not self.game_over)

        if not hide_dealer_card or self.game_over:
            self.dealer_total = self.calculate_total(self.dealer_cards)
            self.dealer_total_label.config(text=f"Total: {self.dealer_total}")
        else:
            # Show visible card total
            visible_card_rank = self.dealer_cards[1][0]
            visible_value = self.card_map[visible_card_rank] if visible_card_rank not in ['A', 'JK'] else (11 if visible_card_rank == 'A' else -1)
            self.dealer_total_label.config(text=f"Total: {visible_value} + ?")

    def disable_action_buttons(self, disable=True):
        """Enables or disables the Hit, Stand, Double Down, and Fold buttons."""
        state = tk.DISABLED if disable else tk.NORMAL
        self.hit_button.config(state=state)
        self.stick_button.config(state=state)
        self.double_button.config(state=state)
        self.fold_button.config(state=state)

    def deal(self):
        """Initial deal of two cards to player and dealer."""
        self.player_cards = [self.draw_card(), self.draw_card()]
        self.dealer_cards = [self.draw_card(), self.draw_card()]
        
        self.update_labels(hide_dealer_card=True)
        self.disable_action_buttons(disable=False)
        self.result_label.config(fg="white", text="Game On!")

        # Check for immediate win (Blackjack or 22 - 22 is now harder to hit with -1 Joker)
        if self.player_total == 21 or (self.player_total == 22 and self.has_joker(self.player_cards)):
            self.game_over = True
            win_text = "Blackjack!" if self.player_total == 21 else "Joker 22 Win!"
            self.result_label.config(fg="#FFD700", text=win_text)
            self.stick() # Proceed to dealer's reveal

    def check_player_bust(self, action_name="Hit"):
        """Checks for player bust, respecting the Joker's 22 rule."""
        max_allowed = 21
        if self.has_joker(self.player_cards):
            max_allowed = 22 # Joker raises non-bust limit

        if self.player_total > max_allowed:
            self.game_over = True
            self.disable_action_buttons()
            self.result_label.config(fg="#FF0000", text=f"{action_name} Bust! Dealer Wins!")
            self.update_labels(hide_dealer_card=False)
            return True
        return False

    def hit(self):
        """Adds one card to the player's hand."""
        if self.game_over:
            return

        # Disable Double Down after the first hit
        self.double_button.config(state=tk.DISABLED)
        
        self.player_cards.append(self.draw_card())
        self.update_labels(hide_dealer_card=True)
        
        self.check_player_bust("Hit")

    def stick(self):
        """Ends the player's turn and starts the dealer's turn."""
        if self.game_over:
            return
            
        self.game_over = True
        self.disable_action_buttons()
        self.dealer_turn_step(0) # Start dealer's turn animation
        
    def fold_game(self):
        """Allows the player to fold/surrender the current hand and shuts down the UI."""
        if self.game_over:
            return
            
        # Shut down the Tkinter application as requested
        self.master.destroy()

    def double_down(self):
        """Player takes two final cards and then stands (non-standard rule)."""
        if self.game_over:
            return
            
        # Draw two cards as requested by the user
        self.player_cards.append(self.draw_card())
        self.player_cards.append(self.draw_card()) 
        
        self.update_labels(hide_dealer_card=True)
        
        # Check for bust after two cards, using "Double Down" in the message
        if not self.check_player_bust("Double Down"):
            # If not busted, immediately stick
            self.stick()

    def dealer_turn_step(self, delay=500):
        """Non-blocking, animated step of the dealer's turn."""
        
        # Reveal hidden card on first step
        if delay == 0:
            self.update_labels(hide_dealer_card=False)
            self.master.update()
            # If player busted, we are done
            max_allowed = 22 if self.has_joker(self.player_cards) else 21
            if self.player_total > max_allowed:
                self.determine_winner()
                return

        # Dealer's AI logic (Dealer plays strictly to 17, no Joker advantage for the house)
        if self.dealer_total < 17:
            
            # User's non-standard rule: 50/50 chance to stick on 16
            if self.dealer_total == 16:
                if randint(0, 1) == 0: # 50% chance (0 or 1)
                    self.determine_winner()
                    return # Dealer sticks on 16
            
            # Hit logic
            new_card = self.draw_card()
            self.dealer_cards.append(new_card)
            self.dealer_total = self.calculate_total(self.dealer_cards)
            
            self.update_labels(hide_dealer_card=False)
            
            # Schedule the next step after 500ms
            self.master.after(500, self.dealer_turn_step)
        else:
            # Dealer stands (>= 17)
            self.determine_winner()

    def determine_winner(self):
        """Compares final hands to declare a winner, respecting the Joker's 22 rule."""
        
        # Ensure final totals are calculated and displayed
        self.update_labels(hide_dealer_card=False)

        player_has_joker = self.has_joker(self.player_cards)
        dealer_has_joker = self.has_joker(self.dealer_cards)
        player_max_non_bust = 22 if player_has_joker else 21
        
        # 1. Player Bust (Check against 22 or 21)
        if self.player_total > player_max_non_bust:
            result_text = "Bust! Dealer Wins!"
            color = "#FF0000"

        # 2. Dealer Bust (Check against 21, as the dealer doesn't get the Joker advantage in this implementation)
        elif self.dealer_total > 21:
            result_text = "Dealer Busts! You Win!"
            color = "#00FF00"
            
        # 3. Joker 22 Win Condition (Checking for 22 is still possible, but now requires 23 points + -1 Joker)
        elif self.player_total == 22 and player_has_joker:
            # Check for rare Joker 22 push (only if dealer also has Joker 22)
            if self.dealer_total == 22 and dealer_has_joker:
                result_text = "Double Joker Push (22 vs 22)!"
                color = "#FFD700"
            else:
                # Player 22 (Joker) beats everything else
                result_text = "Joker Advantage Win (22)!"
                color = "#00FF00"

        # 4. Standard Comparisons
        elif self.player_total > self.dealer_total:
            result_text = "You Win!"
            color = "#00FF00"
        elif self.dealer_total > self.player_total:
            result_text = "Dealer Wins!"
            color = "#FF0000"
        else: # Tie
            result_text = "It's a Tie (Push)!"
            color = "#FFD700"
            
        self.result_label.config(text=result_text, fg=color)
        self.game_over = True

    def new_game(self):
        """Resets all game variables and starts a new round."""
        self.game_over = False
        self.player_total = 0
        self.dealer_total = 0
        self.player_cards = []
        self.dealer_cards = []
        self.result_label.config(text="")
        self.deal()

if __name__ == '__main__':
    root = tk.Tk()
    game = BlackjackGUI(root)
    root.mainloop()
