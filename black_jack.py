# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 949x392 - source: jfitz.com
DISP_CARD_SIZE = (54, 73)
CARD_SIZE = (73, 98)
CARD_CENTER = (36.5, 49)
card_images = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/cards.jfitz.png")

CARD_BACK_SIZE = (71, 96)
CARD_BACK_CENTER = (35.5, 48)
card_back = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/card_back.png")    

# load backgroud image
background_img = simplegui.load_image("http://www.australia-casino.org/sites/default/files/800x600_blackjack_table_game.jpg")

# load backgroud score
sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/Epoq-Lepidoptera.ogg")
sound.set_volume(0.5)
sound.play()

# initialize some useful global variables
in_play = False

message1 = " "
message2 = "    NEW DEAL??"
outcome = ""

score = 0
vol = 1

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos, flag_test_dealer):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], DISP_CARD_SIZE)
   
    def draw_back(self, canvas, pos, flag_test_dealer):
        canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, [pos[0] + CARD_BACK_CENTER[0], pos[1] + CARD_BACK_CENTER[1]], DISP_CARD_SIZE)
            
# define hand class
class Hand:
    def __init__(self):
        # create Hand object
        self.hand = []	
        self.value = 0
        
    def __str__(self):
        # return a string representation of a hand
        ans = ""
        for i in self.hand:
            ans += i.get_suit()
            ans += i.get_rank()
            ans += " "   
        return ans

    def add_card(self, card):
        self.hand.append(card)	# add a card object to a hand

    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        # compute the value of the hand, see Blackjack video
        self.value = 0
        flag_aces = False
        for i in self.hand:
            self.value += VALUES[i.get_rank()]
            if i.get_rank() == "A":
                flag_aces = True
        if flag_aces:
            if self.value + 10 <= 21:
                self.value += 10
            flag_aces = False
        return self.value
    
    def draw(self, canvas, pos, flag_dealer):
        # draw a hand on the canvas, use the draw method for cards
        global in_play
        if not flag_dealer:
            for i in self.hand:
                pos[0] += 30 
                i.draw(canvas, pos, flag_dealer)
        else:
            if in_play:
                pos[0] += 30
                self.hand[0].draw_back(canvas, pos, flag_dealer)
            else:
                if self.hand:
                    pos[0] += 30
                    self.hand[0].draw(canvas, pos, flag_dealer)
            for i in range(1, len(self.hand)):
                pos[0] += 30
                self.hand[i].draw(canvas, pos, flag_dealer)
            
# define deck class 
class Deck:
    def __init__(self):
        # create a Deck object
        self.deck = []
        for i in SUITS:
            for j in RANKS:
                self.deck.append(Card(i, j))    

    def shuffle(self):
        # add cards back to deck and shuffle
        return random.shuffle(self.deck)

    def deal_card(self):
        return random.choice(self.deck)	# deal a card object from the deck
    
    def __str__(self):
        # return a string representing the deck
        ans = ""
        for i in self.deck:
            ans += i.get_suit()
            ans += i.get_rank()
            ans += " "   
        return ans

dealer = Hand()
player = Hand()    

#define event handlers for buttons
def deal():
    global outcome, in_play, deck, dealer, player, canvas, message1, message2, score, c1
    if in_play:    
        score -= 1
        message1 = "Resigned Round. You Lost!"
    else:
        message1 = " "    
    message2 = "HIT/STAND??"
    in_play = True
    
    # generate two cards each for dealer and player
    c1 = Card(random.choice(SUITS), random.choice(RANKS))
    c2 = Card(random.choice(SUITS), random.choice(RANKS))
    p1 = Card(random.choice(SUITS), random.choice(RANKS))
    p2 = Card(random.choice(SUITS), random.choice(RANKS))
        
    deck = Deck()
    deck.shuffle()
        
    dealer = Hand()
    player = Hand()
        
    dealer.add_card(c1)
    dealer.add_card(c2)
        
    player.add_card(p1)
    player.add_card(p2)
    
def hit():
    global message1, message2, score, in_play
    if in_play:
        message1= " "
        # if the hand is in play, hit the player
        p3 = Card(random.choice(SUITS), random.choice(RANKS))
        player.add_card(p3)
        
        # if busted, assign a message to outcome, update in_play and score
        if player.get_value() > 21:
            message1 = "Busted. You Lost!"
            message2 = "New Deal??"
            score -= 1
            in_play = False    
       
def stand():
    global score, in_play, message1, message2
    # assign a message to outcome, update in_play and score
    if in_play:
        message1 = " "
        # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
        while dealer.get_value() < 17:
            c3 = Card(random.choice(SUITS), random.choice(RANKS))
            dealer.add_card(c3)
        if dealer.get_value() > 21:
            score += 1
            message1 = "Dealer Busted. You win!"
            message2 = "New Deal??"
            in_play = False
        elif dealer.get_value() == player.get_value():
            score -= 1
            message1 = "Tie. Dealer Wins!"
            message2 = "New Deal??"
            in_play = False
        elif dealer.get_value() > player.get_value():
            score -= 1
            message1 = "Dealer Wins!"
            message2 = "New Deal??"
            in_play = False
        elif dealer.get_value() < player.get_value():
            score += 1
            message1 = "You Win!"
            message2 = "New Deal??"
            in_play = False
            
# draw handler    
def draw(canvas):
    global message, in_play
    # test to make sure that card.draw works, replace with your code below
    canvas.draw_image(background_img, (300, 225), (600, 450), (300,225), (600,450))    
    dealer.draw(canvas, [200,136], True)
    player.draw(canvas, [200,233], False)
    
    canvas.draw_polygon([[220, 135], [382, 135], [382, 98], [220, 98]], 2, "White", "Green")
    canvas.draw_text("BLACK JACK!", (225, 123), 24, "White")
    canvas.draw_text("Score: " + str(score), (520, 120), 20, "Blue")
    if not in_play:
        canvas.draw_text("Dealer Value: " + str(dealer.get_value()), (15, 100), 18, "Blue")
    elif in_play and c1.get_rank() == "A":
        canvas.draw_text("Dealer Value: " + str(dealer.get_value() - VALUES[c1.get_rank()] - 10), (15, 100), 18, "Blue")
    else:
        canvas.draw_text("Dealer Value: " + str(dealer.get_value() - VALUES[c1.get_rank()]), (15, 100), 18, "Blue")
    canvas.draw_text("Hand Value: " + str(player.get_value()), (250, 335), 18, "Blue")
    canvas.draw_text(message1, (232, 92), 18, "Yellow")
    canvas.draw_text(message2, (235, 240), 18, "Yellow")

# mute the background score
def mute():
    global vol
    vol = 0
    sound.set_volume(vol)

# increase volume
def vol_up():
    global vol
    if vol < 0.9:
        vol += 0.1
    sound.set_volume(vol)

# reduce volume 
def vol_down():
    global vol
    if vol > 0.1:
        vol -= 0.1
    sound.set_volume(vol)

# exit game
def exit():
    frame.stop()
    sound.rewind()
    
# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 450)
frame.set_canvas_background("Green")

# create buttons and canvas callback
label = frame.add_label("Game Controls")
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)

# game controls
label = frame.add_label(" ")
label = frame.add_label("Volume Controls")
frame.add_button("Mute Sound", mute, 200)
frame.add_button("Increase Volume", vol_up, 200)
frame.add_button("Decrease Volume", vol_down, 200)

# exit game
label = frame.add_label(" ")
label = frame.add_label("Quit")
frame.add_button("Exit", exit, 200)
frame.set_draw_handler(draw)

# start the frame & remember to review the gradic rubric
frame.start()