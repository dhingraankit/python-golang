import pandas as pd
import numpy as np
import datetime

firstPlayer = []
secondPlayer = []

i = 0 
j = 0
Total = 0
startTime = datetime.datetime.now()

#Creating DataFrame of the game for displaying current status of your game
df = pd.DataFrame(data = {"1st Player": firstPlayer,
				"2nd Player": secondPlayer,
				"Total So Far": (sum(firstPlayer[:i + 1]) + sum(secondPlayer[:j + 1]))})

while Total < 100:
	#Taking input for 1st Players Chance
	firstTurn = int(input("Player 1: \n"))
	
	#Run further only when 1st player enter b/w 1 to 10
	if firstTurn in range(1,11):
		firstPlayer.append(firstTurn)
		i = i + 1
		df = df.append({"1st Player": firstTurn,
					"2nd Player": 0}, ignore_index=True)

		#Calculating cummulative sum from both players chances so far
		for row in df:
			df["Total So Far"] =  np.cumsum(df["1st Player"] + df["2nd Player"])
			Total = (sum(firstPlayer[:i + 1]) + sum(secondPlayer[:j + 1]))
		#Print Current Status of the DataFrame
		print("Current Game Status: \n", df.to_string(index=False))	

		#If cummulative sum reaches 100, declare player 1 as a winner, else continue to take entries
		if (sum(firstPlayer[:i + 1]) + sum(secondPlayer[:j])) >= 100:
			print("Player 1 Wins!!")
			endTime = datetime.datetime.now()
			td = endTime - startTime	
			print("Your game session time is %s Seconds." %td)   	
			break
	#If value not in [1,10] then ask player 1 to retry		
	else:
		print("You have entered an invalid number. Kindly abide by the rules and enter a number between 1 to 10.")
		continue
	

	#2nd Players Chance
	secondTurn = int(input("Player 2: \n"))

	#Run further only when 2nd player enter b/w 1 to 10
	if secondTurn in range(1,11):

		#Append second players change to the Series in a DataFrame
		secondPlayer.append(secondTurn)
		j = j + 1

		#Append values to existing dataframe:
		df['2nd Player'] = df['2nd Player'].replace(0, secondTurn)
		
		#Calculating cummulative sum from both players chances so far
		for row in df:
			df["Total So Far"] =  np.cumsum(df["1st Player"] + df["2nd Player"])
			Total = (sum(firstPlayer[:i + 1]) + sum(secondPlayer[:j + 1]))
		#Print Current Status of the DataFrame
		print("Current Game Status: \n", df.to_string(index=False))
		
		#If cummulative sum reaches 100, declare player 2 as a winner, else continue to take entries
		if (sum(firstPlayer[:i + 1]) + sum(secondPlayer[:j + 1])) >= 100:
			print("Player 2 Wins!!")
			endTime = datetime.datetime.now()
			td = endTime - startTime	
			print("Your game session time is %s Seconds." %td)   	
			break 
	
	#If value not in [1,10] then ask player 2 to retry
	else:
		print("You have entered an invalid number. Kindly abide by the rules and enter a number within 1 to 10.")
		continue