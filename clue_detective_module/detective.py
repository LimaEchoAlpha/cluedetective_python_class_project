
from board import *

class Note():
    """This is class represents the types of notes stored in a notebook.

       Attributes:
       - type = what type of information the note contains

       Subclasses:
       - Yes: marks the cards that are known to be in another player’s hand
       - No: marks the cards that are known to be absent from another player’s hand
       - Maybe: marks the unknown cards that a player secretly revealed in a turn 
       - Mine: marks the cards that are in the user’s hand
    """
    
    def __init__(self):
        pass
    def __eq__(self, other):
        return self.type == other.type
    
class Yes(Note):
    def __init__(self):
        self.type = 'yes'
    def __repr__(self):
        return '\u2713'

class No(Note):
    def __init__(self):
        self.type = 'no'
    def __repr__(self):
        return 'X'

class Maybe(Note):
    def __init__(self):
        self.type = 'maybe'
        self.notes = []
    def __repr__(self):
        if len(self.notes) == 0:
            return ' '
        elif len(self.notes) == 1:
            return '?'
        elif len(self.notes) > 1:
            return '!'

class Mine(Note):
    def __init__(self):
        self.type = 'mine'
    def __repr__(self):
        return '\u2731'


class Notebook():
    """This is a container class used to store all the notes taken by the detective during 
       the current game of Clue being played by the user.

       Attributes:
       - board:  current instance of Board
       - contents:  dictionary that stores all the notes indexed by card and player

       Functions:
       - mark_mine():   Marks the appropriate notes for all the cards in the user’s hand.
       - mark_no():  Marks a card as absent in a player’s hand.
       - mark_yes():  Marks the card as present in a player’s hand and absent in everyone else’s.
       - mark_maybe():  Marks the unknown cards that a player secretly revealed that turn.
       - rows():  Takes in a card type as argument and returns all the rows in the notebook 
                  containing cards of that type.
       - printout():  Prints out the current contents of the notebook.
    """
    
    def __init__(self, board):
        self.board = board
        self.contents = {(card.type, card.name, player.name): Maybe() 
                         for card in board.cards 
                         for player in board.players}
        self.mark_mine()

    def mark_mine(self):
        # mark all the cards in the user's hand
        keys = [(card.type, card.name, self.board.me.name) for card in self.board.me.hand]
        for key in keys:
            self.contents[key] = Mine()
        
        # cross out all cards in the user's column that is absent from their hand
        x_keys = [key for key in self.contents.keys() 
                  if key[2] == self.board.me.name and self.contents[key] != Mine()]
        for key in x_keys:
            self.mark_no(key)
        
        # cross out the cards in the user's hand for all the other players
        my_hand = [card.name for card in self.board.me.hand]
        x_keys2 = [key for key in self.contents 
                   if key[2] != self.board.me.name and key[1] in my_hand]
        for key in x_keys2:
            self.mark_no(key)
            
    def mark_no(self, key):
        
        # only proceed if card is orginally marked as maybe
        not_maybe = ['yes', 'no', 'mine']
        if self.contents[key].type in not_maybe:
            return
        else: 
            self.contents[key] = No()
       
    def mark_yes(self, key):
        
        # only proceed if card is orginally marked as maybe
        not_maybe = ['yes', 'no', 'mine']
        if self.contents[key].type in not_maybe:
            print("Warning: something is wrong with the entry; not recorded.")
            return
        
        # if card was marked as a maybe for a turn
        # remove those maybe marks for other cards that remain
        # this is needed for a deduction step later
        if len(self.contents[key].notes) > 0:
            player_maybe = [new_key for new_key in self.contents 
                            if new_key[2] == key[2] 
                            and self.contents[new_key].type == 'maybe']
            for new_key in player_maybe:
                if len(self.contents[new_key].notes) > 0:
                    for i in self.contents[new_key].notes:
                        if i in self.contents[key].notes:
                            self.contents[new_key].notes.remove(i)
        
        # mark the card with check
        self.contents[key] = Yes()
        
        # cross out the card for all the other players
        x_keys = [x_key for x_key in self.contents
                 if x_key[2] != key[2] and x_key[1] == key[1]]
        for x in x_keys:
            self.mark_no(x)
    
    def mark_maybe(self, turn):
        i = self.board.history.index(turn)
        for card in turn.suggestion:
            key = (card.type, card.name, turn.disprover.name)
            if self.contents[key].type == 'maybe':
                self.contents[key].notes.append(i)
           
    def rows(self, card_type):
        rows = {}
        for key in self.contents:
            if key[0] == card_type:
                if key[1] not in rows:
                    rows[key[1]] = []
                rows[key[1]].append(self.contents[key])
        return rows  
    
    def printout(self):
        
        border = '-'*(16 + 4*self.board.num_players)
        print(f"{' ':17s}", end = ' ')
        for player in self.board.players:
            if player.name == 'Rose':
                print('RS', end=" ")
            elif player.name == 'Peach':
                print('PH', end=" ")
            elif player.name == 'Gray':
                print('GY', end=" ")
            else:
                print(f"{player.name[:2].upper():^3s}", end=" ")
        print('\n' + border)
        
        card_types = ['Suspect', 'Weapon', 'Room']
        for t in card_types:
            cards = self.rows(t)
            print(t.upper() + ":" )
            for card in cards.keys():
                print(f"{card:13s}", '-|-', end = ' ')
                for player in self.board.players:
                    symbol = str(self.contents[(t, card, player.name)])
                    print(f"{symbol:^3s}", end = ' ')
                print()
            print('\n', border)
        print()


class Detective():
    """This is class takes notes on information learned in each turn 
       and deduced new information from previous notes. 

       Attributes:
       - board: current instance of Board
       - notebook = current instance of Notebook

       Functions:
       - take notes(): Takes in a turn as argument. If there is no disprover, crosses out 
                       the cards suggested for all the players except the suggester.  
                       If there is a disprover and a card is revealed, checks off the card.  
                       If there is a disprover, but the card is revealed secretly, marks all the maybes.
       - deduce_count(): Check to see if all the player’s cards are known.  
                         If they are, cross off all the other cards for that player.
       - deduce_maybe(): Check a player’s column for any cards from previous turns that are 
                         now known to be in that player’s hand by process of elimination.
       - deduce_solution(): Takes a card type as an argument, checks for a solution for that type, 
                            and returns the solution, if found.  
       - find_solution(): Uses the deduce_solution function to find any solutions and stores it in 
                          the current instance of Solution.
    """

    def __init__(self, board, notebook):
        self.board = board
        self.notebook = notebook

        
    def take_notes(self, turn):
        suggestion = turn.suggestion
        revealed = turn.revealed
        disprover = turn.disprover
        suggester = turn.suggester

        if not disprover:
            x_keys = [(card.type, card.name, player.name) 
                      for card in suggestion 
                      for player in self.board.players if player != suggester]
            for key in x_keys:
                self.notebook.mark_no(key)

        elif disprover != self.board.me:

            # check off the revealed card if any
            # or else mark secretly revealed unknown cards as maybe
            if revealed:
                key = (revealed.type, revealed.name, disprover.name)
                self.notebook.mark_yes(key)
                x_keys = [key for key in self.notebook.contents 
                          if key[1] == revealed.name 
                          and key[2] != disprover.name 
                          and key[2] != self.board.me.name]
                for key in x_keys:
                    self.notebook.mark_no(key)
            else: 
                self.notebook.mark_maybe(turn)

            # if players could not disprove before the disprover
            # mark the cards suggested as absent in all those players' hands
            x_players = []
            next_player = self.board.next_player(suggester)
            while next_player.name != disprover.name:
                x_players.append(next_player)
                current_player = next_player
                next_player = self.board.next_player(current_player)

            x_keys = [(card.type, card.name, player.name)
                      for card in suggestion 
                      for player in x_players if player != self.board.me]
            for key in x_keys:
                self.notebook.mark_no(key)

        self.deduce_count()
        self.deduce_maybe()
        self.deduce_count()
        self.deduce_maybe()
        self.deduce_count()
        
        self.find_solution()
                       
    
    def deduce_count(self):
        dictionary = self.notebook.contents
        for player in self.board.players:
            cards = [key for key in dictionary 
                     if key[2] == player.name 
                     and key[2] != self.board.me.name
                     and dictionary[key] != Yes()]
            yes_cards = 21 - len(cards)
            if player.num_cards == yes_cards:
                for key in cards:
                    self.notebook.mark_no(key)

                    
    def deduce_maybe(self):
        dictionary = self.notebook.contents
        for player in self.board.players:
            maybe_cards = [key for key in dictionary 
                           if key[2] == player.name and dictionary[key].type == 'maybe']
            if len(maybe_cards) > 0:
                maybe_short = maybe_cards.copy()
                values = []
                # look if the player has any maybes marked from previous turns
                for key in maybe_cards:
                    if len(dictionary[key].notes) == 0:
                        maybe_short.remove(key)
                    if len(dictionary[key].notes) > 0:
                        values.extend(dictionary[key].notes)
                # look to see if any maybes from previous turns have been isolated
                # if so, we know by process of elimination
                # that the player definitely has that card
                # only works if the safeguard in mark_yes() in notebook works
                if len(values) > 0:
                    value_count = [x for x in set(values) if values.count(x) == 1]
                    if len(value_count) > 0:
                        for key in maybe_short:
                            for i in dictionary[key].notes:
                                if i in value_count:
                                    self.notebook.mark_yes(key)
    
                                  
    def deduce_solution(self, card_type):
        check = [key for key in self.notebook.rows(card_type)] 
        for key, row in self.notebook.rows(card_type).items():
            count = 0
            # checks for the solution by row
            for entry in row:
                if entry == No():
                    count += 1
                # checks for the solution by column
                elif entry == Yes() or entry == Mine():
                    check.remove(key)
            if count == self.board.num_players:
                return key
        if len(check) == 1:
            return check[0]
                                
    
    def find_solution(self):
        solution = self.board.solution
        if solution.suspect == None:
            solution.suspect = self.deduce_solution('Suspect')
        if solution.weapon == None:
            solution.weapon = self.deduce_solution('Weapon')
        if solution.room == None:
            solution.room = self.deduce_solution('Room')
