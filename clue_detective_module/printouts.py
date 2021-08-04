"""This module contains helper functions for printing out decoder keys, legends, and banners."""

from board import *

def welcome():
    print("*"+"-"*58+"*")
    print("|"+" "*24+"WELCOME TO"+" "*24+"|")
    print("|"+" "*22+"CLUE DETECTIVE!"+" "*21+"|")
    print("*"+"-"*58+"*")

def instructions():
    print("*"+" "*58+"*")
    print("*"+" "*23+"HOW TO USE:"+" "*24+"*")
    print("*"+" "*4+"Use the given input codes to enter your responses"+" "*5+"*")
    print("*"+" "*2+"HINT: Most codes are the first two letters of the word"+" "*2+"*")
    print("*"+" "*9+"To quit the program at any time, enter Q"+" "*9+"*")
    print("*"+" "*58+"*")
    suspect_decoder()
    weapon_decoder()
    room_decoder()
    print()

def suspect_decoder():
    key = [key for key in Board.input_decoder if Board.input_decoder[key].type == 'Suspect']
    value = [value.name for value in Board.input_decoder.values() if value.type == 'Suspect']
    print("-"*22+" SUSPECT CODES "+"-"*23)
    print(" "*8+f"{key[0]} = {value[0]:8s}  {key[1]} = {value[1]:8s}  {key[2]} = {value[2]:7s}")
    print(" "*8+f"{key[3]} = {value[3]:8s}  {key[4]} = {value[4]:8s}  {key[5]} = {value[5]:7s}")
    print(" "*8+f"{key[6]} = {value[6]:8s}  {key[7]} = {value[7]:8s}  {key[8]} = {value[8]:7s}")
    print(" "*8+f"{key[9]} = {value[9]:8s}  {key[10]} = {value[10]:8s}  {key[11]} = {value[11]:7s}")
    print(" "*8+f"{key[12]} = {value[12]:8s}  {key[13]} = {value[13]:8s}  {key[14]} = {value[14]:7s}")
    print(" "*8+f"{key[15]} = {value[15]:8s}  {key[16]} = {value[16]:8s}  {key[17]} = {value[17]:7s}")
    print("-"*60)
    
def weapon_decoder():
    key = [key for key in Board.input_decoder if Board.input_decoder[key].type == 'Weapon']
    value = [value.name for value in Board.input_decoder.values() if value.type == 'Weapon']
    print("-"*23+" WEAPON CODES "+"-"*23)
    print(" "*5+f"{key[0]} = {value[0]:12s}  {key[1]} = {value[1]:8s}  {key[2]} = {value[2]:8s}"+" "*5)
    print(" "*5+f"{key[3]} = {value[3]:12s}  {key[4]} = {value[4]:8s}  {key[5]} = {value[5]:8s}"+" "*5)
    print("-"*60)

def room_decoder():
    key = [key for key in Board.input_decoder if Board.input_decoder[key].type == 'Room']
    value = [value.name for value in Board.input_decoder.values() if value.type == 'Room']
    print("-"*24+" ROOM CODES "+"-"*24)
    print(f" {key[0]} = {value[0]:12s}  {key[1]} = {value[1]:14s}  {key[2]} = {value[2]:8s}")
    print(f" {key[3]} = {value[3]:12s}  {key[4]} = {value[4]:14s}  {key[5]} = {value[5]:8s}")
    print(f" {key[6]} = {value[6]:12s}  {key[7]} = {value[7]:14s}  {key[8]} = {value[8]:8s}")
    print("-"*60)

def notes_legend():
    print("-"*23+" NOTES LEGEND "+"-"*23)
    print(" "*2+"\u2731 = In your hand", end = "   ")
    print("\u2713 = Has card", end = "   ")
    print("X = Does not have card"+" "*2)
    print(" "*10+"? = Might have card", end = "   ")
    print("! = Likely has card"+" "*9)
    print("-"*60)

def solution_banner(suspect, weapon, room):
    print("*"+"-"*58+"*")
    print("|"+" "*20+"SOLUTION FOUND!!!!"+" "*20+"|")
    print("|"+" "*20+f"It was {suspect:8s}"+" "*23+"|")
    print("|"+" "*20+f"with the {weapon:12s}"+" "*17+"|")
    print("|"+" "*20+f"in the {room:14s}"+" "*17+"|")
    print("*"+"-"*58+"*")
