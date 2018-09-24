import pandas as pd
import numpy as np
import random
import datetime


startTime = datetime.datetime.now()

def computersChance(somelist,somechance, j):
	HumanCitySuffix = somechance[j]
	FilteredList = []
	for value in somelist:
		if value.startswith(HumanCitySuffix):
			FilteredList.append(value)
	FilteredLength = len(FilteredList)
	Choice = FilteredList[random.randint(0,FilteredLength - 1)] 
	return Choice


def toLower(oldlist):
	newList = []
	for value in oldlist:
		value = value.lower()
		newList.append(value)
	return newList

CityList = pd.read_csv("city_list.csv")
Cities = toLower(list(CityList.City))


AllChances = []
i = 1


while i in range(1, len(Cities)):	
	HumansChance = input("Human: \n")
	
	if HumansChance in Cities:
		#Appending Humans chance if the value does not exists
		if HumansChance not in AllChances:
			AllChances.append(HumansChance)
		else:
			#If Humans chance already exists in the list of names mentioned earlier, he loses
			print("You repeated the city already mentioned. You lost, sucker!! " +  '%r' % u'\U0001f604')
			endTime = datetime.datetime.now()
			td = endTime - startTime	
			print("Your game session time is %s Seconds." %td)
			break
		print("Human: \n",AllChances) 
		
		#Use ComputersChance function defined above to compute his chance
		computersChoses = computersChance(Cities,HumansChance, -1)
		
		#Appending Computers chance if the value does not exists		
		if computersChoses not in AllChances:
			AllChances.append(computersChoses)
		else:
			#If computers chance already exists in the list of names mentioned earlier, it loses
			print("You've beaten the computer'!! " +  '%r' % u'\U0001f604')
			endTime = datetime.datetime.now()
			td = endTime - startTime	
			print("Your game session time is %s Seconds." %td)
			break
		print("Computer: \n",AllChances)		
		i = i + 1
	else:
		print("Do you want me to give you a dictionary?! Duh!")


