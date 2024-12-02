'''
1. In this start of the game there are 5040(10x9x8x7) unique possibilities each with equal probability of occurence.
2. Initial Entropy is also calculated with the probability and number of possibilities.
3. As the guess increases the number of possibilities decreases--> probability increases and entropy descreases.
4. The number of possibilities decreases with each guess and the rate of decrease depends on the following conditions.
    a. If b=0 and c=0, 
        then remove all the possibilities if any one of the number is present in the possibility considered.
    b. If b=0 and c=1, 
        then concatenate the index and number of the guess and current possibility and find the common occurences of these 
        should be 0(Indicating 0 bull) and common numbers between guess and current possibility should be exactly 1(Cow).
    c. If b=0 and c=2,
        then do the same as before condition but the common numbers between guess and current possibility should be exactly 2(Cow).
    d. If b=0 and c=3,
        same as above but common occurences should be 3(Cow).
    e. If b=0 and c=4,
        same as above but common occurences should be 4(Cow).
    f. If b=1 and c=0,
        atleast one of the number in the guess and current possibility should be in same index.
    g. If b=2 and c=0,
        atleast 2 of the number in the guess and current possibility should be in the same index.
    h. If b=3 and c=0,
        atleast 3 of the number in the guess and current possibility should be in the same index.
    i. If b=1 and c=1,
        one of the element in the guess and current possibility should be in same index and out of all other elements in other index
        should have one common occurence in different indices.
    j. If b=1 and c=2,
        one of the element in the guess and current possibility should be in same index and out of all other elements in other indices
        should have 2 common occurences in different indices.
    k. If b=1 and c=3,
        same as above condition but should have 3 common occurrences all in different indices.
    l. If b=2 and c=1,
        Two of the elements in the guess and current possibility should be in same index and out of all other elements in other indices
        should have 1 common occurences in different indices.
    m. If b=2 and c=2,
        same as above, but 2 common occurences should be present in different indices
    n. If b=4 and c=0,
        then the guess is correctly predicted and end the game.
5. After each guess reduce the number of possibilities this inturn increases the probability and decreases entropy
6. After winning, show the graph on how the probability increases, entropy decreases and number of possibility decreases.
'''

#--------Import all the neccessary packages-----------#

import tkinter as tk
from tkinter import messagebox
import math
from itertools import permutations, combinations
import random
import time
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import math
import sys
#------------Create a class for the game as well as Graphical User Interface---------------#
class BullsAndCowsGUI:
    #--------------Initialize all the necessary variables and window for the GUI game---------------#
    def __init__(self, root):
        #-----------------Initialize the gaming window elements line tab name, root window---------------#
        self.root = root
        self.root.title("Bulls and Cows Game")
        #-------------Necessary variables to keep in track of the number of bulls and cows, current guess, entropy, probability------------#
        self.attempts = 0
        self.all_possibilities = []
        self.all_entropy = []
        self.all_probability = []
        self.possibility_length = []
        l = [i for i in range(0,10)]
        #----------Generate all set of possible combinations------------#
        for comb in combinations(l,4):
            for perm in permutations(comb):
                self.all_possibilities.append(perm)
        #-----------Calculate the Initial probability and entropy-------------#
        self.probability = 1/len(self.all_possibilities)
        self.entrophy = self.probability * math.log2(1/self.probability) * len(self.all_possibilities)
        self.all_entropy.append(self.entrophy)
        self.all_probability.append(self.probability)
        self.possibility_length.append(len(self.all_possibilities))
        #------------Get the initial guess of the computer-------------#
        self.guess = random.choice(self.all_possibilities) 
        
        #------------Initialize the GUI related components----------------#
        self.label_title = tk.Label(root, text="Bulls and Cows Game", font=("Arial", 22, "bold"))
        self.label_title.pack(pady=10)

        self.label_instructions = tk.Label(root, text="Think of a 4-digit secret number (unique digits).\n"
                                                      "The computer will try to guess it.\n"
                                                      "Enter Bulls and Cows feedback below.", font=("Arial", 20))
        self.label_instructions.pack(pady=10)

        self.label_guess = tk.Label(root, text=f"Computer's Guess: {self.guess}", font=("Arial", 20))
        self.label_guess.pack(pady=10)

        self.label_bulls = tk.Label(root, text="Bulls (correct digit and position):", font=("Arial", 20))
        self.label_bulls.pack()

        self.entry_bulls = tk.Entry(root, font=("Arial", 20))
        self.entry_bulls.pack()

        self.label_cows = tk.Label(root, text="Cows (correct digit but wrong position):", font=("Arial", 20))
        self.label_cows.pack()

        self.entry_cows = tk.Entry(root, font=("Arial", 20))
        self.entry_cows.pack()

        self.button_submit = tk.Button(root, text="Submit Feedback", command=self.process_feedback, font=("Arial", 20))
        self.button_submit.pack(pady=10)

        self.label_entropy = tk.Label(root, text=f"Current Entropy: {round(self.entrophy,2)} bits", font=("Arial", 20))
        self.label_entropy.pack(pady=10)

        self.label_probability = tk.Label(root, text=f"Current Probability: {round(self.probability,2)}", font=("Arial", 20))
        self.label_probability.pack(pady=10)

        self.label_possibilities = tk.Label(root, text=f"Remaining Possibilities: {len(self.all_possibilities)}", font=("Arial", 20))
        self.label_possibilities.pack(pady=10)

        #------------Display the entropy graph--------------#
        self.figure, self.ax = plt.subplots(figsize=(5, 4))
        self.ax.set_title("Remaining Possibilities Over Time")
        self.ax.set_xlabel("Attempts")
        self.ax.set_ylabel("Remaining Possibilities")
        self.line, = self.ax.plot([], [], marker='o')
        self.canvas = FigureCanvasTkAgg(self.figure, master=root)
        self.canvas.get_tk_widget().pack()

    #------------Update the graph after each guess by storing the entropy calculated after each guess----------------#
    def update_graph(self):
        """Update the Matplotlib graph with the latest data."""
        self.ax.clear()
        self.ax.set_title("Entropy(Measure of Uncertainty) Over Time")
        self.ax.set_xlabel("Attempts")
        self.ax.set_ylabel("Entropy")
        self.ax.plot(range(1, len(self.all_entropy) + 1), self.all_entropy, marker='o', color='blue')
        self.canvas.draw()

    #---------Get the count of bulls and cows, remove the possibilities accordingly and calculate entropy-----------#
    def process_feedback(self):
        try:
            bullcount = int(self.entry_bulls.get())
            cowcount = int(self.entry_cows.get())
        #--------when other values are given---------#
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter integers for Bulls and Cows.")
            return

        to_be_removed = [self.guess]

        if(bullcount == 0 and cowcount == 0):
            for i in self.all_possibilities:
                if(self.guess[0] in i or self.guess[1] in i or self.guess[2] in i or self.guess[3] in i):
                    to_be_removed.append(i)
            
        elif(bullcount == 0 and cowcount ==1):
            for i in self.all_possibilities:
                if(len(set([str(i[0])+'0',str(i[1])+'1',str(i[2])+'2',str(i[3])+'3']) & set([str(self.guess[0])+'0',str(self.guess[1])+'1',str(self.guess[2])+'2',str(self.guess[3])+'3']))==0
                   and len(set(i) & set(self.guess))==1):
                    continue
                else:
                    to_be_removed.append(i)
            
        elif(bullcount == 0 and cowcount == 2):
            for i in self.all_possibilities:
                if(len(set([str(i[0])+'0',str(i[1])+'1',str(i[2])+'2',str(i[3])+'3']) & set([str(self.guess[0])+'0',str(self.guess[1])+'1',str(self.guess[2])+'2',str(self.guess[3])+'3']))==0
                   and len(set(i) & set(self.guess))==2):
                    continue
                else:
                    to_be_removed.append(i)
            
        elif(bullcount == 0 and cowcount == 3):
            for i in self.all_possibilities:
                if(len(set([str(i[0])+'0',str(i[1])+'1',str(i[2])+'2',str(i[3])+'3']) & set([str(self.guess[0])+'0',str(self.guess[1])+'1',str(self.guess[2])+'2',str(self.guess[3])+'3']))==0
                   and len(set(i) & set(self.guess))==3):
                    continue
                else:
                    to_be_removed.append(i)
            
        elif(bullcount == 0 and cowcount == 4):
            for i in self.all_possibilities:
                if(len(set([str(i[0])+'0',str(i[1])+'1',str(i[2])+'2',str(i[3])+'3']) & set([str(self.guess[0])+'0',str(self.guess[1])+'1',str(self.guess[2])+'2',str(self.guess[3])+'3']))==0
                   and len(set(i) & set(self.guess))==4):
                    continue
                else:
                    to_be_removed.append(i)
            
        elif(bullcount == 1 and cowcount == 0):
            for i in self.all_possibilities:
                if(i[0] == self.guess[0] or i[1]==self.guess[1] or i[2] == self.guess[2] or i[3]==self.guess[3]):
                    continue
                else:
                    to_be_removed.append(i)
            
        elif(bullcount == 2 and cowcount == 0):
            for i in self.all_possibilities:
                if((i[0] == self.guess[0] and i[1]==self.guess[1]) or (i[0]==self.guess[0] and i[2]==self.guess[2]) or (i[0]==self.guess[0] and i[3]==self.guess[3])
                   or (i[1]==self.guess[1] and i[2]==self.guess[2]) or (i[1]==self.guess[1] and i[3]==self.guess[3])
                   or (i[2]==self.guess[2] and i[3]==self.guess[3])):
                    continue
                else:
                    to_be_removed.append(i)
            
        elif(bullcount == 3 and cowcount == 0):
            for i in self.all_possibilities:
                if((i[0]==self.guess[0] and i[1]==self.guess[1] and i[2]==self.guess[2]) or (i[0]==self.guess[0] and i[1]==self.guess[1] and i[3]==self.guess[3])
                   or (i[1]==self.guess[1] and i[2]==self.guess[2] and i[3] == self.guess[3]) or (i[0]==self.guess[0] and i[2]==self.guess[2] and i[3] == self.guess[3])):
                    continue
                else:
                    to_be_removed.append(i)
            
        elif(bullcount == 1 and cowcount == 1):
            for i in self.all_possibilities:
                if((i[0] == self.guess[0] and i[1]!=self.guess[1] and i[2]!=self.guess[2] and i[3]!=self.guess[3] and len(set(self.guess[1:]) & set(i[1:]))==1) or
                   (i[1] == self.guess[1] and i[0]!=self.guess[0] and i[2]!=self.guess[2] and i[3]!=self.guess[3] and len(set([self.guess[0],self.guess[2],self.guess[3]]) & set([i[0],i[2],i[3]])) == 1) or
                   (i[2] == self.guess[2] and i[0]!=self.guess[0] and i[1]!=self.guess[1] and i[3]!=self.guess[3] and len(set([self.guess[0],self.guess[1],self.guess[3]]) & set([i[0],i[1],i[3]])) == 1) or
                   (i[3] == self.guess[3] and i[0]!=self.guess[0] and i[1]!=self.guess[1] and i[2]!=self.guess[2] and len(set(self.guess[0:3]) & set(i[0:3])) == 1)):
                    continue
                else:
                    to_be_removed.append(i)

        elif(bullcount==1 and cowcount==2):
            for i in self.all_possibilities:
                if((i[0] == self.guess[0] and i[1]!=self.guess[1] and i[2]!=self.guess[2] and i[3]!=self.guess[3] and len(set(self.guess[1:]) & set(i[1:]))==2) or
                   (i[1] == self.guess[1] and i[0]!=self.guess[0] and i[2]!=self.guess[2] and i[3]!=self.guess[3] and len(set([self.guess[0],self.guess[2],self.guess[3]]) & set([i[0],i[2],i[3]])) == 2) or
                   (i[2] == self.guess[2] and i[0]!=self.guess[0] and i[1]!=self.guess[1] and i[3]!=self.guess[3] and len(set([self.guess[0],self.guess[1],self.guess[3]]) & set([i[0],i[1],i[3]])) == 2) or
                   (i[3] == self.guess[3] and i[0]!=self.guess[0] and i[1]!=self.guess[1] and i[2]!=self.guess[2] and len(set(self.guess[0:3]) & set(i[0:3])) == 2)):
                    continue
                else:
                    to_be_removed.append(i)

        elif(bullcount==1 and cowcount==3):
            for i in self.all_possibilities:
                if((i[0] == self.guess[0] and i[1]!=self.guess[1] and i[2]!=self.guess[2] and i[3]!=self.guess[3] and len(set(self.guess[1:]) & set(i[1:]))==3) or
                   (i[1] == self.guess[1] and i[0]!=self.guess[0] and i[2]!=self.guess[2] and i[3]!=self.guess[3] and len(set([self.guess[0],self.guess[2],self.guess[3]]) & set([i[0],i[2],i[3]])) == 3) or
                   (i[2] == self.guess[2] and i[0]!=self.guess[0] and i[1]!=self.guess[1] and i[3]!=self.guess[3] and len(set([self.guess[0],self.guess[1],self.guess[3]]) & set([i[0],i[1],i[3]])) == 3) or
                   (i[3] == self.guess[3] and i[0]!=self.guess[0] and i[1]!=self.guess[1] and i[2]!=self.guess[2] and len(set(self.guess[0:3]) & set(i[0:3])) == 6)):
                    continue
                else:
                    to_be_removed.append(i)

        elif(bullcount==2 and cowcount == 1):
            for i in self.all_possibilities:
                if((i[0]==self.guess[0] and i[1]==self.guess[1] and i[2]!=self.guess[2] and i[3]!=self.guess[3] and len(set(i[2:]) & set(self.guess[2:]))==1) or
                   (i[0]==self.guess[0] and i[2]==self.guess[2] and i[1]!=self.guess[1] and i[3]!=self.guess[3] and len(set([i[1],i[3]])&set([self.guess[1],self.guess[3]]))==1) or
                   (i[0]==self.guess[0] and i[3]==self.guess[3] and i[1]!=self.guess[1] and i[2]!=self.guess[2] and len(set([i[1],i[2]])&set([self.guess[1],self.guess[2]]))==1) or
                   (i[1]==self.guess[1] and i[2]==self.guess[2] and i[0]!=self.guess[0] and i[3]!=self.guess[3] and len(set([i[0],i[3]])&set([self.guess[0],self.guess[3]]))==1) or
                   (i[1]==self.guess[1] and i[3]==self.guess[3] and i[0]!=self.guess[0] and i[2]!=self.guess[2] and len(set([i[0],i[2]])&set([self.guess[0],self.guess[2]]))==1) or
                   (i[2]==self.guess[2] and i[3]==self.guess[3] and i[0]!=self.guess[0] and i[1]!=self.guess[1] and len(set([i[0],i[1]])&set([self.guess[0],self.guess[1]]))==1)):
                    continue
                else:
                    to_be_removed.append(i)

        elif(bullcount==2 and cowcount == 2):
            for i in self.all_possibilities:
                if((i[0]==self.guess[0] and i[1]==self.guess[1] and i[2]!=self.guess[2] and i[3]!=self.guess[3] and len(set(i[2:]) & set(self.guess[2:]))==2) or
                   (i[0]==self.guess[0] and i[2]==self.guess[2] and i[1]!=self.guess[1] and i[3]!=self.guess[3] and len(set([i[1],i[3]])&set([self.guess[1],self.guess[3]]))==2) or
                   (i[0]==self.guess[0] and i[3]==self.guess[3] and i[1]!=self.guess[1] and i[2]!=self.guess[2] and len(set([i[1],i[2]])&set([self.guess[1],self.guess[2]]))==2) or
                   (i[1]==self.guess[1] and i[2]==self.guess[2] and i[0]!=self.guess[0] and i[3]!=self.guess[3] and len(set([i[0],i[3]])&set([self.guess[0],self.guess[3]]))==2) or
                   (i[1]==self.guess[1] and i[3]==self.guess[3] and i[0]!=self.guess[0] and i[2]!=self.guess[2] and len(set([i[0],i[2]])&set([self.guess[0],self.guess[2]]))==2) or
                   (i[2]==self.guess[2] and i[3]==self.guess[3] and i[0]!=self.guess[0] and i[1]!=self.guess[1] and len(set([i[0],i[1]])&set([self.guess[0],self.guess[1]]))==2)):
                    continue
                else:
                    to_be_removed.append(i)
        
        #------------If the guess is correct just display the message, point out the # of attempts and close the game----------------#
        else:
            to_be_removed=[]
            for i in self.all_possibilities:
                if(i!=self.guess):
                    to_be_removed.append(i)
            messagebox.showinfo("Congratulations!", f"The computer guessed your number in {self.attempts + 1} attempts!")
            self.root.destroy()
            sys.exit()
            return

        self.all_possibilities = [i for i in self.all_possibilities if i not in to_be_removed]

        self.probability = 1/len(self.all_possibilities)
        self.entrophy = self.probability * math.log2(1/self.probability) * len(self.all_possibilities)
        self.all_entropy.append(self.entrophy)
        self.all_probability.append(self.probability)
        self.possibility_length.append(len(self.all_possibilities))

        #-----------When the bull count is not 4 then display the entropy and probability for the guess--------------#
        if(bullcount!=4 and cowcount!=0):

            self.attempts+=1
        #-------------Generate the next guess--------------#
            self.guess = random.choice(self.all_possibilities)
            self.label_guess.config(text=f"Computer's Guess: {self.guess}")

            self.label_guess.config(text=f"Computer's Guess: {''.join(map(str, self.guess))}")
            self.label_entropy.config(text=f"Current Entropy: {round(self.entrophy,2)} bits")
            self.label_probability.config(text=f"Current Probability: {round(self.probability,2)}")
            self.label_possibilities.config(text=f"Remaining Possibilities: {len(self.all_possibilities)}")

        #------------Update the graph------------#
            self.update_graph()

        #---------------Clear entry fields for next feedback----------------#
            self.entry_bulls.delete(0, tk.END)
            self.entry_cows.delete(0, tk.END)

#-----Start the Game Here-------#
root = tk.Tk()
app = BullsAndCowsGUI(root)
root.mainloop()