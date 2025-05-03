import pandas as pd
import numpy as np

class Die():
    """
    This class will create a Die that can be used within the Monte Carlo Simulation.
    
    A die in this insatance is an item with N sides, with each side having a unique "Face" value. These Face 
    values will each be assigned a "Weight", or probability of being "rolled".

    Default Values:
    1) The Weight of each face is 1
    2) The number of times rolled is 1
    3) The behavior of the dice is roll

    Characteristics:
    1) A die has N number of sides, each with W weight
    2) The weights are any positive number
    """

    def __init__(self,faces):
        '''
        This method will initialize the die that will be used throughout the class.

        Args:
        1) faces: The values of the faces to be included on the dice

        Requirements:
        1) faces must be a Numpy Array
        2) Numpy array data type must be either strings or numbers
        3) Each face on the die must be a unique value and cannot be repeated
        
        Defaults:
        1) All faces will have a weight of 1

        Results:
        1) Creates a Pandas DataFrame of the faces and their corresponding weights.
        '''
        self.faces=faces
        if isinstance(self.faces, np.ndarray)==False:
            raise TypeError ("Faces Must be in a Numpy Array")
        if len(self.faces)!=len(set(self.faces)):
            raise ValueError ("Die values must be Unique")

        self._die=pd.DataFrame({'face':faces,'weights':1}).set_index('face')


    def change_weight(self,face,weight):
        '''
        This method will change the weight value for a specified face.

        Args:
        1) faces: The value of the face to be changed
        2) weight: The numeric value of the weight assiged to the face

        Requirements:
        1) faces must exist within the initialized die
        2) weight value must be numeric (either integer or float)

        Results:
        1) Modifies weight value within the existing _die dataframe for the specified face
        '''
        
        try:
            weight=float(weight)
        except (ValueError,TypeError):
            raise TypeError ('Weight Must be a Numeric Value')
        if face in self.faces:
            self._die.loc[face]=weight
        else:
            raise IndexError (f"{face} is not a valid value")

    def roll(self,rolls=1):
        '''
        This method will roll the initialized dice a specified number of times and returns the results.

        Args:
        1) rolls: the number of times the result should be rolled

        Requirements:
        1) rolls must be a positive integer

        Results:
        1) returns a list of the outcomes from the sample of rolls
        '''
        self.rolls=rolls
        weight_probs=[i/sum(self._die.weights) for i in self._die.weights]
        temp=self._die.sample(self.rolls,replace=True, weights=weight_probs)
        return temp.index.tolist()

    def show_die(self):
        '''
        This method returns the current face and weight value for the initalized die.

        Results:
        1) A Pandas dataframe showing each face and its corresonding weight for the initialized die.
        '''
        return self._die




class Game():
    '''
    This class uses the initialized die to simulate a "game" of rolls for those die.

    A game can be played any number of times for one or more similar die. Each set of die within the game will have
    the same faces and number of rolls, however, each may have their own weights for each face.

    Default Values:
    1) The behavior of the game is to roll a set of dice a given number of times

    Characteristics:
    1) Each die has the same number of sides
    2) Each die has the same face values
    3) Each die may have different weight values for each face
    '''
    def __init__(self,dice):
        '''
        This method will initialize the game that will be used throughout the class.

        Args:
        1) dice: An already instantiated list of dice created through the Die class

        Requirements:
        1) faces on each die must match
        2) the dice passed to the method must be instantiated through the Die class

        Results:
        1) Initializes variable _results that is built with a None value to be overwritten later in the class
        '''
        self.dice=dice
        self._results=None

    def play(self,n_rolls):
        '''
        This method will simulate playing a game for the given set of die.

        Args:
        1) n_rolls: the number of times each dice should be rolled within the game

        Requirements:
        1) the number of rolls must be a postive integer

        Results:
        1) The results of the rolls are saved to a private dataframe, _results.
        '''
        results = {}
        for i in range(len(self.dice)):
            roll = self.dice[i].roll(n_rolls)
            results[i] = roll

        self._results = pd.DataFrame(results)
        self._results.index.name = 'roll_num'
            
    def results(self,type='wide'):
        '''
        This method will return a copy of the game results to the user in a specified format.

        Args:
        1) type: The dataframe format that should be returned to the user

        Defaults:
        1) Type will default to 'wide'

        Requirements:
        1) The type passed to the method must be either 'narrow' or 'wide'

        Results:
        1) The _results dataframe will be retunred to the user in either the 'narrow' or 'wide' format
        '''
        if type.lower() =='narrow':
            return self._results.melt(
                ignore_index=False,
                value_name='Outcome',
                var_name='Die Number',
            ).rename_axis('Roll Number').reset_index().set_index(['Roll Number', 'Die Number'])
        
        elif type.lower() =='wide':
            return self._results
        
        else:
            raise ValueError ('Format Must be "Narrow" or "Wide"')
    


class Analyzer():
    '''
    This class extracts statistical metrics from a completed game.

    Characteristics:
    1) The object takes the result of a single game and returns the specified statistical properties.
    '''
    def __init__(self,game):
        '''
        This method will initialize the method with a completed game as the parameter.

        Args:
        1) game: An already instantiated result from a played game

        Requirements:
        1) Value passed as game must be a Game object

        Results:
        1) Initializes variable _game with the details of the game played
        2) Initializes _results with the results of the rolls of the specified game
        3) Initializes _num_dice with the number of dice used in the game
        4) Initializes _faces with a Series of the face values used on the die in the game
        '''
        if not isinstance(game, Game):
            raise ValueError("Input must be a Game object.")
        else:
            self._game = game
            self._results = self._game._results
            self._num_dice = len(self._results.columns)
            self._faces = pd.Series(self._game.dice[0]._die.index).unique()

    def jackpot(self):
        '''
        This method will calculate the number of jackpots rolled in the initialized game.

        A jackpot is determined as a roll where all faces are the same.

        Results:
        1) Returns an integer of the number of jackpots rolled to the user
        '''
        jackpots=0

        for index, roll in self._results.iterrows():
            if len(set(roll)) == 1:
                jackpots+=1
        
        return jackpots

    def face_counts(self):
        '''
        This method will calculate the number of times each face appears for each roll of all dice in the game.

        Results:
        1) Returns a dataframe of the roll number and corresponding count of the times each face appeared for 
        each roll in the game.
        '''
        face_counts=[]
        for index, row in self._results.iterrows():
            counts = row.value_counts().reindex(self._faces, fill_value=0)
            face_counts.append(counts)

        counts = pd.DataFrame(face_counts, index=self._results.index)
        counts.index.name = 'roll_num'
        counts.columns.name = 'face'
        return counts

    def combo_count(self):
        '''
        This method will calculate the number of distinct combinations of faces rolled and the number of times
        that combination occured.

        Results:
        1) Returns a dataframe of the distinct combination of face values and a count of the number of times
        that combination appeared in the game.
        '''
        combinations = self._results.apply(lambda row: sorted(row), axis=1)
        combinations=combinations.to_numpy().tolist()
        combinations=pd.DataFrame(combinations)
        combo_counts = combinations.value_counts().reset_index(name='count')
        cols=[col for col in combo_counts.columns if col !='count']
        combo_counts = combo_counts.set_index(cols)
        return combo_counts


    def perm_count(self):
        '''
        This method will calculate the number of distinct permutations of faces rolled and the number of times
        that combination occured.

        Results:
        1) Returns a dataframe of the distinct permutations of face values and a count of the number of times
        that sequence appeared in the game.
        '''
        perms_list=self._results.to_numpy().tolist()
        perm_df=pd.DataFrame(perms_list)
        perm_df=perm_df.value_counts().reset_index(name='count')
        cols=[col for col in perm_df.columns if col !='count']
        output=perm_df.set_index(cols)

        return output


#if __name__ == "__main__":

### Live Code Tests 

    # ## Die Class Tests

    # # Test Die Class - Scenario 1
    # test_die=Die(np.array(['H','T']))
    # test_die.change_weight('H',1)
    # print(test_die.roll(10))
    # print(test_die.show_die())

    # # Test Die Class - Scenario 2
    # test_die=Die(np.array([1,2,3,4,5,6]))
    # test_die.change_weight(1,2)
    # print(test_die.roll(10))
    # print(test_die.show_die())

    # # Test Die Class - Scenraio 3
    # test_die=Die(np.array(['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S',
    #                    'T','U','V','W','X','Y','Z']))
    # letter_prob=pd.read_table('english_letters.txt',names=['Count'],index_col=0,header=None,delimiter=' ')
    # letter_prob['prob']=letter_prob.Count/sum(letter_prob.Count)
    # for i in letter_prob.index:
    #     test_die.change_weight(i,letter_prob.loc[i,'prob'])
    # print(test_die.roll(10))
    # print(test_die.show_die())
    

    # ## Game Class Tests

    # # Test Game Class - Scenario 1
    # fair_coin=Die(np.array(["H","T"]))
    # unfair_coin=Die(np.array(["H","T"]))
    # unfair_coin.change_weight("H",5)
    # game1=Game([fair_coin,unfair_coin])
    # game1.play(1000)
    # print(game1.results('narrow'))
    # print(game1.results('wide'))

    # # Test Game Class - Scenario 2
    # die1=Die(np.array([1,2,3,4,5,6]))
    # die2=Die(np.array([1,2,3,4,5,6]))
    # die3=Die(np.array([1,2,3,4,5,6]))
    # unfair_die1=Die(np.array([1,2,3,4,5,6]))
    # unfair_die2=Die(np.array([1,2,3,4,5,6]))
    # unfair_die1.change_weight(6,5)
    # unfair_die2.change_weight(1,5)
    # game1=Game([die1,die2,die3])
    # game2=Game([die1,die2,die3,unfair_die1,unfair_die2])
    # game1.play(10000)
    # game2.play(10000)
    # print(game1.results('narrow'))
    # print(game1.results('wide'))
    # print(game2.results('narrow'))
    # print(game2.results('wide'))

    # # Test Game Class - Scenario 3
    # alph_die=Die(np.array(['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S',
    #                    'T','U','V','W','X','Y','Z']))
    # letter_prob=pd.read_table('english_letters.txt',names=['Count'],index_col=0,header=None,delimiter=' ')
    # letter_prob['prob']=letter_prob.Count/sum(letter_prob.Count)
    # for i in letter_prob.index:
    #     alph_die.change_weight(i,letter_prob.loc[i,'prob'])
    # game1=Game([alph_die,alph_die,alph_die,alph_die])
    # game1.play(10000)
    # print(game1.results('narrow'))
    # print(game1.results('wide'))


    ## Test Analyzer Class

    # Test Analyzer Class - Scenario 1
    # fair_coin=Die(np.array(["H","T"]))
    # unfair_coin=Die(np.array(["H","T"]))
    # unfair_coin.change_weight("H",5)
    # game1=Game([fair_coin,unfair_coin])
    # game1.play(1000)

    # analyze=Analyzer(game1)
    # print(analyze.jackpot())
    # print(analyze.face_counts())
    # print(analyze.combo_count())
    # print(analyze.perm_count())


    # Test Analyzer Class - Scenario 2
    # die1=Die(np.array([1,2,3,4,5,6]))
    # die2=Die(np.array([1,2,3,4,5,6]))
    # die3=Die(np.array([1,2,3,4,5,6]))
    # unfair_die1=Die(np.array([1,2,3,4,5,6]))
    # unfair_die2=Die(np.array([1,2,3,4,5,6]))
    # unfair_die1.change_weight(6,5)
    # unfair_die2.change_weight(1,5)
    # game1=Game([die1,die2,die3])
    # game2=Game([die1,die2,die3,unfair_die1,unfair_die2])
    # game1.play(10000)
    # game2.play(10000)

    # analyze=Analyzer(game1)
    # print(analyze.jackpot())
    # print(analyze.face_counts())
    # print(analyze.combo_count())
    # print(analyze.perm_count())

    # analyze=Analyzer(game2)
    # print(analyze.jackpot())
    # print(analyze.face_counts())
    # print(analyze.combo_count())
    # print(analyze.perm_count())



    # # Test Analyzer Class - Scenario 3
    # alph_die=Die(np.array(['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S',
    #                    'T','U','V','W','X','Y','Z']))
    # letter_prob=pd.read_table('english_letters.txt',names=['Count'],index_col=0,header=None,delimiter=' ')
    # letter_prob['prob']=letter_prob.Count/sum(letter_prob.Count)
    # for i in letter_prob.index:
    #     alph_die.change_weight(i,letter_prob.loc[i,'prob'])
    # game1=Game([alph_die,alph_die,alph_die,alph_die])
    # game1.play(1000)


    # analyze=Analyzer(game1)
    # print(analyze.jackpot())
    # print(analyze.face_counts())
    # print(analyze.combo_count())
    # print(analyze.perm_count())

    # perm_table=analyze.perm_count().index.to_list()
    # perm_results=[]
    
    # for n in perm_table:
    #     out=''
    #     for i in n:
    #         out+=i
    #     perm_results.append(out)

    # english_words=pd.read_table('scrabble_words.txt',names=['Word'],header=None)
    # words=[]
    # words=set(words)
    # for i in english_words['Word']:
    #     words.add(i)

    # results=list(set(perm_results) & set(words))
    # print(results)
    # print(len(results))