from difflib import restore
import fractions
from lib2to3.refactor import get_all_fix_names
import random
from re import sub
import tkinter
from typing import Text

from matplotlib.pyplot import fill, sci, text
from pip import main
import scipy as sp



class Gesture:
    '''
    Gesture class to represent gestures. Implements comparator to determine outcomes between gestures. 
    E.g., Rock > Scissors = True, Rock smashes Scissors. 
    
    Parameters
    ----------
    name : string
        Name of the gesture. E.g. Rock, Scissors..
    wins : [string]
        A list of gestures that this gesture beats. 
    loses : [string]
        A list of gestures that this gestures loses to.
    outcomes : [{string:string}]
        A list of dictionaries that map the result verb to gestures match up. E.g., For gesture 'Spock', the result
        'Paper disproves Spock' maps to 'Paper':'disproves'.
    '''
    def __init__(self, name, wins, loses, outcomes):
        self.gesture = name
        self.wins=wins
        self.loses = loses
        self.outcomes = outcomes

    def __gt__(self, other):
        #If a gesture is in the list of what this gesture loses to, then return true.
        return self.gesture in other.loses
    def __lt__(self, other):
        #If this gesture is in the list of the gesture being compared beats, then return true
        return self.gesture in other.wins
    def __eq__(self, other):
        #Are both gestures the same?
        return self.gesture == other.gesture


def click_handler(event):
    '''
    Handler for click events. When a gesture is clicked, determine the outcome, update the result frame, 
    and then raise the results frame.
    '''
    input_gesture =event.widget["text"]
    pc_input = random.choice(gestures)
    if pc_input == input_gesture:
        player_lable['text']="Player chooses "+ input_gesture
        pc_lable['text']="Computer chooses "+pc_input
        result_lable['text']=input_gesture+" vs "+pc_input +" is a draw"
        win_lose_lable['text']=""
        result.tkraise()
    else:
        player_lable['text']="Player chooses "+ input_gesture
        pc_lable['text']="Computer chooses "+pc_input
        if gesture_objects[input_gesture] > gesture_objects[pc_input]:
            result_lable['text'] = input_gesture + ' '+gesture_objects[input_gesture].outcomes[pc_input] +' ' + pc_input
            win_lose_lable['text']="Player wins!"
        else:
            result_lable['text'] = pc_input + ' '+gesture_objects[input_gesture].outcomes[pc_input] +' ' + input_gesture
            win_lose_lable['text']="Computer wins!"
        result.tkraise()

#GUI setup
top_window = tkinter.Tk()
top_window.title("Rock, Paper, Scissors, Lizard, Spock")
top_window.geometry("500x300")
top_window.rowconfigure(0, weight=1)
top_window.columnconfigure(0, weight=1)

#Frame for 'main screen' of the game.
game_frame = tkinter.Frame(master=top_window)
game_frame.grid(row=0, column=0, sticky='news')

#Frame for results screen.
result  = tkinter.Frame(master=top_window)
result.grid(row=0, columnspan=5, sticky='news')

#Setup grid on result screen
for j in range(0,5):
    result.rowconfigure(j,weight=1)
    result.columnconfigure(0,weight=1)

#Setup UI components on results screen
#-------------------------------------
#player_lable -> what gesture the player choose
player_lable= tkinter.Label(master=result, text="")
player_lable.grid(row=0, column=0)

#pc_lable -> what gesture the computer choose
pc_lable= tkinter.Label(master=result, text="")
pc_lable.grid(row=1, column=0)

#result_lable -> Holds the result sentence
result_lable= tkinter.Label(master=result, text="")
result_lable.grid(row=2, column=0)

#win_lose_lable -> shows who (player or computer) won the match
win_lose_lable = tkinter.Label(master=result, text="")
win_lose_lable.grid(row=3, column=0)

#Place restart button with lambda function to raise the game frame (restart the game)
restart_button = tkinter.Button(master=result,text="Play Again?", command=lambda:game_frame.tkraise())
restart_button.grid(row=4, column=0)


#Setup grid on game frame
for i in range(0,5):
    for j in range(0,2):
        game_frame.rowconfigure(j,weight=1)
        game_frame.columnconfigure(i,weight=1)


#Place lable for game instruction
game_text_label = tkinter.Label(text="Choose a Gesture", master=game_frame)
game_text_label.grid(row=0, columnspan=5)

#Gestures data
gestures = ["Rock", "Paper", "Scissors", "Lizard", "Spock"]
data = {"Rock":{"Scissors":["win","smashes"], "Paper":["loses", "covers"], "Lizard":["win", "smashes"], "Spock":["loses","vaporizes"]},
"Paper":{"Rock":["win","covers"], "Scissors":["loses", "cuts"], "Lizard":["loses","eats"], "Spock":["win","disproves"]},
"Scissors":{"Rock":["loses","smashes"], "Paper":["win","cuts"], "Lizard":["win", "decapitates"], "Spock":["loses","smashes"]}, 
"Lizard":{"Rock":["loses","crushes"], "Paper":["loses","eats"], "Scissors":["loses","decapitates"], "Spock":["win","poisons"]},
"Spock":{"Rock":["win","vaporizes"], "Paper":["loses","disproves"], "Scissors":["win", "smashes"], "Lizard":["loses", "poisons"]}}


#containers holding the gestures objects and buttons corresponding to gestures
gesture_buttons=[]
gesture_objects = {}

#Put buttons on game screen and bind the click handler to left mouse click events
for i in range(0, len(gestures)):
    gesture_buttons.append(tkinter.Button(text=gestures[i], master=game_frame))
    gesture_buttons[i].bind("<1>", click_handler)
    gesture_buttons[i].grid(row=1, column=i)

#parse gesture data to gesture objects 
for gesture in range(0, len(gestures)):
  gesture_data = data[gestures[gesture]]
  win = []
  loses = []
  outcomes = {}
  for opposing_gesture in gesture_data.keys():
        #if the gesture beats the opposing gesture, then it goes in the win list
        if gesture_data[opposing_gesture][0] == 'win':
            win.append(opposing_gesture)
        #gesture loses to the loses list
        else:
            loses.append(opposing_gesture)
        #map outcome, e.g., {'Rock':'covers'} for Paper
        outcomes[opposing_gesture]=gesture_data[opposing_gesture][1]
  gesture_objects[gestures[gesture]]=Gesture(name=gestures[gesture], wins=win, loses=loses, outcomes=outcomes)


    
#Start GUI
game_frame.tkraise()
top_window.mainloop()
