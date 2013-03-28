import db

class Recipe:
	"Recipe class for storing recipe information"
	def __init__(self, name, ingredients):
		self._name = name
		self._ingredients = []

		for (alcohol, amount) in ingredients:
			number, unit = amount.split()
			mlAmount = db.ConvertToMilliters(number, unit);

			self._ingredients.append((alcohol, mlAmount))


	def need_ingredients(self):
		missingList = []
		for (alcohol, amount) in self._ingredients:

			#Get a list of the bottleTypes from the inventory
			bottleTypeList = db.check_inventory_for_type(alcohol)

			#Create an amounts dictionary to determine how much of an amount of 
			#a bottle type is needed. Stores the key as (m,l,t) to ensure there
			#is no mixing of alcohol types
			amounts=dict()
			for(mlg, liquor, alcoholType, inventoryAmount) in bottleTypeList:
				if(alcoholType == alcohol):
					if((mlg, liquor,alcoholType) not in amounts):
						amounts[(mlg,liquor,alcoholType)] = amount - inventoryAmount
					else:
						amounts[(mlg,liquor,alcoholType)] -= inventoryAmount

			#Find out if the bottle type was found, if so, find the type that you have
			#the most of (called lowestAmount, which represents the amount needed.
			#Therefore a negative amount means that you have enough for the recipe.)
			lowestAmount = 99999999999
			amountFound = False
			for(m, l, t) in amounts:
				if(amounts[(m,l,t)] < lowestAmount):
					lowestAmount = amounts[(m,l,t)]
					amountFound = True

			#Appends the lowestAmount needed if an amount at all was found, otherwise
			#append the fact that you need the entire amount for your recipe
		 	if(lowestAmount > 0 and amountFound == True):
				missingList.append((alcohol, lowestAmount))
			elif(amountFound == False):
				missingList.append((alcohol,amount))

		return missingList