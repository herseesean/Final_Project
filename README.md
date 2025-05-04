# Final_Project
DS5100 Final Project

Monte Carlo Simulator
Created by: Sean Hersee

This package provides a set of classes that allow the user to create instances of dice that can be rolled and analyzed in a way that mimic a Monte Carlo simulation.

Classes:  
1)	Die: This class will create a Die that can be used within the Monte Carlo Simulation.  
	a)	Initialization  
	•	A die in this instance is an item with N sides, with each side having a unique "Face" value. These Face values will each be assigned a "Weight", or probability of being "rolled".  
	•	Default Values:  
		i)	The Weight of each face is 1  
		ii)	The number of times rolled is 1  
		iii)	The behavior of the dice is roll  
	•	Characteristics:  
		i)	A die has N number of sides, each with W weight  
		ii)	The weights are any positive number  
	b)	Methods  
		i)	change Weight: Takes the face of an initialized die and the weight value that the face should be assigned.  
		ii)	roll: This method will roll the initialized dice a specified number of times and returns the results.  
		iii)	show_die: This method returns the current face and weight value for the initialized die.  
2)	Game: This class uses the initialized die to simulate a "game" of rolls for those die.  
	a)	Initialization  
		i)	A game can be played any number of times for one or more similar die. Each set of die within the game will have the same faces and number of rolls, however, each may have their own 					weights for each face.  
		ii)	Default Values:  
			(1)	The behavior of the game is to roll a set of dice a given number of times  
		iii)	Characteristics:  
				(1)	Each die has the same number of sides  
				(2)	Each die has the same face values  
				(3)	Each die may have different weight values for each face  
	b)	Methods  
		i)	Play: This method takes the number of rolls as a parameter for an initialized set of die and stores the results of the rolls in a private data frame.  
		ii)	Results: This method will return a copy of the game results to the user in a specified format (wide or narrow data frame).  
3)	Analyzer: This class extracts statistical metrics from a completed game.
	a)	Initialization  
		i)	The object takes the result of a single game and returns the specified statistical properties.  
		ii)	A completed game object as taken as a parameter to complete the analysis from.  
	b)	Methods  
		i)	Combo_count: This method will calculate the number of distinct combinations of faces rolled and the number of times that combination occurred and return a data frame of those 								combinations and the counts.  
		ii)	Face_counts: This method will calculate the number of times each face appears for each roll of all dice in the game and will return a data frame of those face values for each roll.  
		iii)	Jackpot: This method will calculate the number rolls where all faces are the same value. An integer is returned to the user.  
		iv)	Perm_count: This method will calculate the number of distinct permutations of faces rolled and the number of times that combination occurred and return a data frame of those 						permutations and the count to the user.  

How To Use:
1)	Import Libraries  

			from project_classes import Die,Game,Analyzer  
			import numpy as np  
			import pandas as pd  
			import matplotlib.pyplot as plt  

2)	Create Dice

			fair_coin=Die(np.array(["H","T"]))  
			unfair_coin=Die(np.array(["H","T"]))  
			unfair_coin.change_weight("H",5)  

3)	Create a Game

			game1=Game([fair_coin,unfair_coin])  

4)	Play a Game

			game1.play(1000)  

5)	Analyze the Results

			analyze=Analyzer(game1)  
			print(analyze.jackpot())  
			print(analyze.face_counts())  
			print(analyze.combo_count())  
			print(analyze.perm_count())  


