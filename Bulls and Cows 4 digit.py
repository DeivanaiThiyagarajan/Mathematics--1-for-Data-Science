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

import math
from itertools import permutations, combinations
import random
import time
import matplotlib.pyplot as plt

class Game:
    #------------Create a class for the game---------------#
    def __init__(self) -> None:
        #-------------Necessary variables to keep in track of the number of bulls and cows, current guess, entropy, probability------------#
        self.all_possibilities = []
        self.all_entropy = []
        self.all_probability = []
        self.possibility_length = []
        l = [i for i in range(0,10)]
        #--------------Generate all possible outcomes--------------#
        for comb in combinations(l,4):
            for perm in permutations(comb):
                self.all_possibilities.append(perm)
        self.probability = 1/len(self.all_possibilities)
        self.entrophy = self.probability * math.log2(1/self.probability) * len(self.all_possibilities)
        self.all_entropy.append(self.entrophy)
        self.all_probability.append(self.probability)
        self.possibility_length.append(len(self.all_possibilities))

    #---------Get the count of bulls and cows, remove the possibilities accordingly and calculate entropy-----------#
    def reduce_choices(self,guess,bullcount,cowcount):
        to_be_removed = [guess]

        if(bullcount == 0 and cowcount == 0):
            for i in self.all_possibilities:
                if(guess[0] in i or guess[1] in i or guess[2] in i or guess[3] in i):
                    to_be_removed.append(i)
            
        elif(bullcount == 0 and cowcount ==1):
            for i in self.all_possibilities:
                '''if(guess[0] not in i and guess[1] not in i and guess[2] not in i and guess[3] not in i):
                    to_be_removed.append(i)
                elif(guess[0] == i[0] or guess[1]==i[1] or guess[2]==i[2] or guess[3]==i[3]):
                    to_be_removed.append(i)'''
                if(len(set([str(i[0])+'0',str(i[1])+'1',str(i[2])+'2',str(i[3])+'3']) & set([str(guess[0])+'0',str(guess[1])+'1',str(guess[2])+'2',str(guess[3])+'3']))==0
                   and len(set(i) & set(guess))==1):
                    continue
                else:
                    to_be_removed.append(i)

            
        elif(bullcount == 0 and cowcount == 2):
            for i in self.all_possibilities:
                '''if((guess[0] not in i and guess[1] not in i and guess[2] not in i) and (guess[0] not in i and guess[2] not in i) and (guess[0] not in i and guess[3] not in i)
                   and (guess[1] not in i and guess[2] not in i) and (guess[1] not in i and guess[3] not in i) and (guess[2] not in i and guess[3] not in i)):
                    to_be_removed.append(i)
                elif((guess[0] == i[0] and guess[1] == i[1]) or (guess[0] == i[0] and guess[2] == i[2]) or (guess[0] == i[0] and guess[2] == i[2])
                     or (guess[1] == i[1] and guess[2] == i[2]) or (guess[1] == i[1] and guess[3] == i[3]) or (guess[2] == i[2] and guess[3] == i[3])):
                    to_be_removed.append(i)'''
                if(len(set([str(i[0])+'0',str(i[1])+'1',str(i[2])+'2',str(i[3])+'3']) & set([str(guess[0])+'0',str(guess[1])+'1',str(guess[2])+'2',str(guess[3])+'3']))==0
                   and len(set(i) & set(guess))==2):
                    continue
                else:
                    to_be_removed.append(i)
            
        elif(bullcount == 0 and cowcount == 3):
            for i in self.probability:
                '''if((guess[0] not in i and guess[1] not in i and guess[2] not in i) and 
                   (guess[0] not in i and guess[1] not in i and guess[3] not in i) and 
                   (guess[0] not in i and guess[2] not in i and guess[3] not in i) and 
                   (guess[1] not in i and guess[2] not in i and guess[3] not in i)):
                    to_be_removed.append(i)
                elif((guess[0] == i[0] and guess[1] == i[1] and guess[2] == i[2]) or 
                     (guess[0] == i[0] and guess[1] == i[1] and guess[3] == i[3]) or 
                     (guess[0] == i[0] and guess[2] == i[2] and guess[3] == i[3]) or
                     (guess[1] == i[1] and guess[2] == i[2] and guess[3] == i[3])):
                    to_be_removed.append(i)'''
                if(len(set([str(i[0])+'0',str(i[1])+'1',str(i[2])+'2',str(i[3])+'3']) & set([str(guess[0])+'0',str(guess[1])+'1',str(guess[2])+'2',str(guess[3])+'3']))==0
                   and len(set(i) & set(guess))==3):
                    continue
                else:
                    to_be_removed.append(i)
            
        elif(bullcount == 0 and cowcount == 4):
            for i in self.all_possibilities:
                '''if(guess[0] not in i and guess[1] not in i and guess[2] not in i and guess[3] not in i):
                    to_be_removed.append(i)'''
                if(len(set([str(i[0])+'0',str(i[1])+'1',str(i[2])+'2',str(i[3])+'3']) & set([str(guess[0])+'0',str(guess[1])+'1',str(guess[2])+'2',str(guess[3])+'3']))==0
                   and len(set(i) & set(guess))==4):
                    continue
                else:
                    to_be_removed.append(i)
            
        elif(bullcount == 1 and cowcount == 0):
            for i in self.all_possibilities:
                if(i[0] == guess[0] or i[1]==guess[1] or i[2] == guess[2] or i[3]==guess[3]):
                    continue
                else:
                    to_be_removed.append(i)
            
        elif(bullcount == 2 and cowcount == 0):
            for i in self.all_possibilities:
                if((i[0] == guess[0] and i[1]==guess[1]) or (i[0]==guess[0] and i[2]==guess[2]) or (i[0]==guess[0] and i[3]==guess[3])
                   or (i[1]==guess[1] and i[2]==guess[2]) or (i[1]==guess[1] and i[3]==guess[3])
                   or (i[2]==guess[2] and i[3]==guess[3])):
                    continue
                else:
                    to_be_removed.append(i)
            
        elif(bullcount == 3 and cowcount == 0):
            for i in self.all_possibilities:
                if((i[0]==guess[0] and i[1]==guess[1] and i[2]==guess[2]) or (i[0]==guess[0] and i[1]==guess[1] and i[3]==guess[3])
                   or (i[1]==guess[1] and i[2]==guess[2] and i[3] == guess[3]) or (i[0]==guess[0] and i[2]==guess[2] and i[3] == guess[3])):
                    continue
                else:
                    to_be_removed.append(i)
            
        elif(bullcount == 1 and cowcount == 1):
            for i in self.all_possibilities:
                if((i[0] == guess[0] and i[1]!=guess[1] and i[2]!=guess[2] and i[3]!=guess[3] and len(set(guess[1:]) & set(i[1:]))==1) or
                   (i[1] == guess[1] and i[0]!=guess[0] and i[2]!=guess[2] and i[3]!=guess[3] and len(set([guess[0],guess[2],guess[3]]) & set([i[0],i[2],i[3]])) == 1) or
                   (i[2] == guess[2] and i[0]!=guess[0] and i[1]!=guess[1] and i[3]!=guess[3] and len(set([guess[0],guess[1],guess[3]]) & set([i[0],i[1],i[3]])) == 1) or
                   (i[3] == guess[3] and i[0]!=guess[0] and i[1]!=guess[1] and i[2]!=guess[2] and len(set(guess[0:3]) & set(i[0:3])) == 1)):
                    continue
                else:
                    to_be_removed.append(i)

        elif(bullcount==1 and cowcount==2):
            for i in self.all_possibilities:
                if((i[0] == guess[0] and i[1]!=guess[1] and i[2]!=guess[2] and i[3]!=guess[3] and len(set(guess[1:]) & set(i[1:]))==2) or
                   (i[1] == guess[1] and i[0]!=guess[0] and i[2]!=guess[2] and i[3]!=guess[3] and len(set([guess[0],guess[2],guess[3]]) & set([i[0],i[2],i[3]])) == 2) or
                   (i[2] == guess[2] and i[0]!=guess[0] and i[1]!=guess[1] and i[3]!=guess[3] and len(set([guess[0],guess[1],guess[3]]) & set([i[0],i[1],i[3]])) == 2) or
                   (i[3] == guess[3] and i[0]!=guess[0] and i[1]!=guess[1] and i[2]!=guess[2] and len(set(guess[0:3]) & set(i[0:3])) == 2)):
                    continue
                else:
                    to_be_removed.append(i)

        elif(bullcount==1 and cowcount==3):
            for i in self.all_possibilities:
                if((i[0] == guess[0] and i[1]!=guess[1] and i[2]!=guess[2] and i[3]!=guess[3] and len(set(guess[1:]) & set(i[1:]))==3) or
                   (i[1] == guess[1] and i[0]!=guess[0] and i[2]!=guess[2] and i[3]!=guess[3] and len(set([guess[0],guess[2],guess[3]]) & set([i[0],i[2],i[3]])) == 3) or
                   (i[2] == guess[2] and i[0]!=guess[0] and i[1]!=guess[1] and i[3]!=guess[3] and len(set([guess[0],guess[1],guess[3]]) & set([i[0],i[1],i[3]])) == 3) or
                   (i[3] == guess[3] and i[0]!=guess[0] and i[1]!=guess[1] and i[2]!=guess[2] and len(set(guess[0:3]) & set(i[0:3])) == 6)):
                    continue
                else:
                    to_be_removed.append(i)

        elif(bullcount==2 and cowcount == 1):
            for i in self.all_possibilities:
                if((i[0]==guess[0] and i[1]==guess[1] and i[2]!=guess[2] and i[3]!=guess[3] and len(set(i[2:]) & set(guess[2:]))==1) or
                   (i[0]==guess[0] and i[2]==guess[2] and i[1]!=guess[1] and i[3]!=guess[3] and len(set([i[1],i[3]])&set([guess[1],guess[3]]))==1) or
                   (i[0]==guess[0] and i[3]==guess[3] and i[1]!=guess[1] and i[2]!=guess[2] and len(set([i[1],i[2]])&set([guess[1],guess[2]]))==1) or
                   (i[1]==guess[1] and i[2]==guess[2] and i[0]!=guess[0] and i[3]!=guess[3] and len(set([i[0],i[3]])&set([guess[0],guess[3]]))==1) or
                   (i[1]==guess[1] and i[3]==guess[3] and i[0]!=guess[0] and i[2]!=guess[2] and len(set([i[0],i[2]])&set([guess[0],guess[2]]))==1) or
                   (i[2]==guess[2] and i[3]==guess[3] and i[0]!=guess[0] and i[1]!=guess[1] and len(set([i[0],i[1]])&set([guess[0],guess[1]]))==1)):
                    continue
                else:
                    to_be_removed.append(i)

        elif(bullcount==2 and cowcount == 2):
            for i in self.all_possibilities:
                if((i[0]==guess[0] and i[1]==guess[1] and i[2]!=guess[2] and i[3]!=guess[3] and len(set(i[2:]) & set(guess[2:]))==2) or
                   (i[0]==guess[0] and i[2]==guess[2] and i[1]!=guess[1] and i[3]!=guess[3] and len(set([i[1],i[3]])&set([guess[1],guess[3]]))==2) or
                   (i[0]==guess[0] and i[3]==guess[3] and i[1]!=guess[1] and i[2]!=guess[2] and len(set([i[1],i[2]])&set([guess[1],guess[2]]))==2) or
                   (i[1]==guess[1] and i[2]==guess[2] and i[0]!=guess[0] and i[3]!=guess[3] and len(set([i[0],i[3]])&set([guess[0],guess[3]]))==2) or
                   (i[1]==guess[1] and i[3]==guess[3] and i[0]!=guess[0] and i[2]!=guess[2] and len(set([i[0],i[2]])&set([guess[0],guess[2]]))==2) or
                   (i[2]==guess[2] and i[3]==guess[3] and i[0]!=guess[0] and i[1]!=guess[1] and len(set([i[0],i[1]])&set([guess[0],guess[1]]))==2)):
                    continue
                else:
                    to_be_removed.append(i)
        #------------If the guess is correct just display the message in the main function---------------#
        else:
            for i in self.all_possibilities:
                if(i!=guess):
                    to_be_removed.append(i)

        self.all_possibilities = [i for i in self.all_possibilities if i not in to_be_removed]

        self.probability = 1/len(self.all_possibilities)
        self.entrophy = self.probability * math.log2(1/self.probability) * len(self.all_possibilities)
        self.all_entropy.append(self.entrophy)
        self.all_probability.append(self.probability)
        self.possibility_length.append(len(self.all_possibilities))

    def show_graph(self):
        fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(10, 5))

        # Plot the Entropy line graph
        ax1.plot(self.all_entropy, color='blue', label='Entropy')
        ax1.set_title('Entropy Graph')
        ax1.set_xlabel('# of Guesses')
        ax1.set_ylabel('Bits')
        ax1.legend()

        # Plot the Probability line graph
        ax2.plot(self.all_probability, color='red', label='Probability')
        ax2.set_title('Probability Graph')
        ax2.set_xlabel('# of Guesses')
        ax2.set_ylabel('Probability')
        ax2.legend()

        # Plot the Possibility length line graph
        ax3.plot(self.possibility_length ,color = 'green',label = 'Possibility Length')
        ax3.set_title('Possibility Length Graph')
        ax3.set_xlabel('# of Guesses')
        ax3.set_ylabel('Possibilities')
        ax3.legend()

        plt.tight_layout()
        plt.show()


def main():
    choice = 'y'
    while(choice[0].lower()=='y'):
        new_game = Game()
        print('guess 4 numbers between 0 and 9 without repetition')
        time.sleep(5)
        print()
        print("Ready? Let's Start")
        print()
        print('This is my initial Entropy: '+ str(new_game.entrophy))
        print('The possibile choice are: '+str(len(new_game.all_possibilities)))
        bullcount = 0
        cowcount = 0
        #first = True
        #second = True
        while(True):
            #-------loop through until the correct numbers are not found--------#
            guess = random.choice(new_game.all_possibilities)
            print('Is it ....' , guess)
            #---------Get feedback from the User--------#
            bullcount = int(input('What is the Bull Count?'))
            cowcount = int(input('What is the cow count?'))
            print()
            if(bullcount != 4):
                new_game.reduce_choices(guess,bullcount,cowcount)
                print('New Entropy is '+ str(new_game.entrophy))
                print('My choices are now limited to ',len(new_game.all_possibilities))
                print()
            else:
                #-----------Break the loop-----------#
                break
        print('Found it')
        print('The Uncertainty Level graph')
        #-----------Once the secret number is found display the graph-------------#
        new_game.show_graph()
        print('Game Over!!!')
        #---------------Ask the user if he wants to play another game-----------------#
        choice = input('Do you want to play another game?(yes/no):')


if __name__ == '__main__':
    main()