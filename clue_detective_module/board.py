
class Player():
    """This is a container class used to store all the information about the players of the game.
       
       Attributes:
       - name = name of the player
       - num_cards = number of cards in the player’s hand
       - hand = list of cards in the player’s hand
    """
    
    def __init__(self, name, num_cards=None, hand=[]):
        self.name = name
        self.num_cards = num_cards
        self.hand = hand    
    def __eq__(self, other):
        return self.name == other.name 
    def __repr__(self):
        return self.name
    

class Solution():
    """This is a container class used to store all the solutions found by the detective.

       Attributes:
       - suspect = guess for suspect solution
       - weapon = guess for weapon solution
       - room = guess for room solution
    """
    
    def __init__(self, suspect=None, weapon=None, room=None):
        self.name = 'Solution'
        self.suspect = suspect
        self.weapon = weapon
        self.room = room
        
    def is_solved(self):
        if self.suspect and self.weapon and self.room:
            return True
        else:
            return False
    
    def not_solved(self):
        if not self.suspect and not self.weapon and not self.room:
            return True
        else:
            return False
    
    def partially_solved(self):
        if self.suspect or self.weapon or self.room:
            return True
        else:
            return False

        
class Card():
    """This is class represents the cards in the game of Clue.

       Attributes:
       - name = name of the card

       Subclasses:
       - Suspect: has the attribute type ‘Suspect’
       - Weapon: has the attribute type ‘Weapon’
       - Room: has the attribute type ‘Room’
    """
    
    def __init__(self, name):
        self.name = name
    def __eq__(self, other):
        self.name == other.name    
    def __repr__(self):
        return self.name

class Suspect(Card):
    
    def __init__(self, name):
        super().__init__(name)
        self.type = 'Suspect'

class Weapon(Card):
    
    def __init__(self, name):
        super().__init__(name)
        self.type = 'Weapon'
        
class Room(Card):
    
    def __init__(self, name):
        super().__init__(name)
        self.type = 'Room'


class Turn():
    """This is a container class used to store all the information for one turn.

       Attributes:
       suggester = player whose turn it is
       suggestion = tuple containing the suspect, room, and weapon that was suggested
       disprover = player who disproved the suggestion
       revealed = card that was revealed that turn
    """
    
    def __init__(self, suggester):
        self.suggester = suggester
        suggestion = ()
        self.suggestion = suggestion
        disprover = None
        self.disprover = disprover
        revealed = None
        self.revealed = revealed


class Board():
    """This is a container class used to store all the information about the current game of Clue being played by the user.

       Attributes:
       - *start_cards = list that stores all the starting cards in the Clue game (class attribute)
       - *input_decoder = dictionary for decoding input codes for the cards (class attribute)
       - *player_decoder = dictionary for decoding input codes for the players (class attribute)
       - me: which player the user is
       - players = list of the players in the order of their turn
       - solution = particular instance of the Solution class used in the game
       - cards = cards used in the game
       - history = list of all the turns made in the game

       Functions:
       - translate(): Takes an input code as argument and returns the card it decodes to
       - identify(): Takes an input code as argument and returns the player it decodes to
       - num_card_calc(): Calculates the number of cards each player should have for 2, 3, and 6 player game.  
                          For 4 or 5 player game, takes in which players have less cards 
                          and assigns the number of cards accordingly.  
                          Stores the number of cards for each player in the num_cards attribute.
       - next_player(): Takes in the player whose turn it is as argument 
                        and returns the player whose turn is next.
       - log_turn(): Takes in information about the turn 
                     and returns an instance of the turn with the information recorded in it.
    """
    
    start_cards = [Weapon('Candlestick'), Weapon('Dagger'), Weapon('Lead Pipe'),
             Weapon('Revolver'), Weapon('Rope'), Weapon('Wrench'),
             Room('Ballroom'), Room('Billiard Room'), Room('Conservatory'),
             Room('Dining Room'), Room('Hall'), Room('Kitchen'),
             Room('Library'), Room('Lounge'), Room('Study')]
    
    input_decoder = {'MU': Suspect('Mustard'), 'OR': Suspect('Orchid'), 'SC': Suspect('Scarlett'), 
             'GR': Suspect('Green'), 'PE': Suspect('Peacock'), 'PL': Suspect('Plum'), 
             'WH': Suspect('White'), 'BR': Suspect('Brunette'), 'AZ': Suspect('Azure'),
             'RU': Suspect('Rusty'), 'SH': Suspect('Sherlock'), 'WA': Suspect('Watson'),
             'MO': Suspect('Moriarty'), 'AD': Suspect('Adler'), 'ME': Suspect('Meadow-Brook'), 
             'RS': Suspect('Rose'), 'PH': Suspect('Peach'), 'GY': Suspect('Gray'),
             'CA': Weapon('Candlestick'), 'DA': Weapon('Dagger'), 'LE': Weapon('Lead Pipe'),
             'RE': Weapon('Revolver'), 'RO': Weapon('Rope'), 'WR': Weapon('Wrench'),
             'BA': Room('Ballroom'), 'BI': Room('Billiard Room'), 'CO': Room('Conservatory'),
             'DI': Room('Dining Room'), 'HA': Room('Hall'), 'KI': Room('Kitchen'),
             'LI': Room('Library'), 'LO': Room('Lounge'), 'ST': Room('Study')}
    
    player_decoder = {'MU': Player('Mustard'), 'OR': Player('Orchid'), 'SC': Player('Scarlett'), 
             'GR': Player('Green'), 'PE': Player('Peacock'), 'PL': Player('Plum'),
             'WH': Player('White'), 'BR': Player('Brunette'), 'AZ': Player('Azure'),
             'RU': Player('Rusty'), 'SH': Player('Sherlock'), 'WA': Player('Watson'),
             'MO': Player('Moriarty'), 'AD': Player('Adler'), 'ME': Player('Meadow-Brook'),
             'RS': Player('Rose'), 'PH': Player('Peach'), 'GY': Player('Gray')}

    
    def __init__(self, me, players, suspects):
        
        self.me = me
        self.players = players
        self.num_players = len(players)
        self.solution = Solution()
        self.cards = Board.start_cards
        for suspect in suspects:
            self.cards.append(suspect)
        history = []
        self.history = history
    
    def translate(user_input):
        i = user_input.upper()
        return Board.input_decoder[i]
    
    def identify(user_input):
        i = user_input.upper()
        return Board.player_decoder[i]
    
    def num_card_calc(self, different = []):
        even = [2, 3, 6]
        if self.num_players in even:
            for player in self.players:
                player.num_cards = int(18 / self.num_players)
        elif self.num_players == 4:
            for player in self.players:
                if player in different:
                    player.num_cards = int(4)
                else: 
                    player.num_cards = int(5)
        elif self.num_players == 5:
            for player in self.players:
                if player in different:
                    player.num_cards = int(3)
                else:
                    player.num_cards = int(4)
              
    def next_player(self, player):
        i = self.players.index(player)
        n = self.num_players
        return self.players[(i+1)%n]
    
    def log_turn(self, suggester, suggestion=(), disprover=None, revealed=None):
        turn = Turn(suggester)
        if suggestion:
            turn.suggestion = suggestion
        if disprover:
            turn.disprover = disprover
        if revealed:
            turn.revealed = revealed
        self.history.append(turn)
        return turn
