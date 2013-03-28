import os
import drinkz.db, drinkz.recipes

if not os.path.exists('./html'):
	os.makedirs('./html')

try:
	drinkz.db.load_db('bin/drinkz_db')
except IOError:
	print "ERROR! The specified db file does not exist, no data was loaded. Moving on..."
	pass

#Create the index file
f = open("./html/index.html", "w")
f.write('<html><head></head><body>')
f.write('<h1>Eric Miller - HTML Output</h1><br/>')
f.write('<a href="./recipes.html">View recipes.html</a><br/><br/>')
f.write('<a href="./inventory.html">View inventory.html</a><br/><br/>')
f.write('<a href="./liquor_types.html">View liquor_types.html</a>')
f.write('</body></html>')
f.close()

#--------------------------------------------------------------------------------------------

#Add liquor types to db
# drinkz.db._reset_db()
# drinkz.db.add_bottle_type('Johnnie Walker', 'Black Label', 'blended scotch')
# drinkz.db.add_bottle_type('V&S Group','Absolute','vodka')
# drinkz.db.add_bottle_type('Diageo', 'Smirnoff', 'vodka')
# drinkz.db.add_bottle_type('Jack Daniels Manufacturing Company', 'Jack Daniels', 'whiskey')


#Create the liquor_types.html file
f = open("./html/liquor_types.html", "w")
f.write('<html><head></head><body><ul>')
f.write('<h1>Liquor Types</h1><br/>')

alcoholTypes = drinkz.db.get_all_bottle_types()
for(m,l,t) in alcoholTypes:
	f.write('<li> <ul><li>Manufacturer: ' + m + '</li><li>Liquor: ' + l + '</li><li>Type: ' + t + '</li></ul>')

f.write('</ul>')
f.write('<a href="./index.html">View index.html</a><br/><br/>')
f.write('<a href="./recipes.html">View recipes.html</a><br/><br/>')
f.write('<a href="./inventory.html">View inventory.html</a><br/><br/>')
f.write('</body></html>')
f.close()

#--------------------------------------------------------------------------------------------

#Add to inventory db
# drinkz.db.add_to_inventory('Johnnie Walker', 'Black Label', '1000 ml')
# drinkz.db.add_to_inventory('Johnnie Walker', 'Black Label', '500 ml')
# drinkz.db.add_to_inventory('V&S Group','Absolute', '60 oz')
# drinkz.db.add_to_inventory('Diageo', 'Smirnoff', '1 gallon')
# drinkz.db.add_to_inventory('Jack Daniels Manufacturing Company', 'Jack Daniels', '2.5 liter')

#Create the inventory.html file
f = open("./html/inventory.html", "w")
f.write('<html><head></head><body><ul>')
f.write('<h1>Liquor Inventory</h1><br/>')

alcoholAmounts = drinkz.db.get_all_liquor_amounts()
for(m,l) in alcoholAmounts:
	f.write('<li> <ul><li>Manufacturer: ' + m + '</li><li>Liquor: ' + l + '</li><li>Amount: ' + alcoholAmounts[(m,l)] + ' ml</li></ul>')

f.write('</ul><br/>')
f.write('<a href="./index.html">View index.html</a><br/><br/>')
f.write('<a href="./recipes.html">View recipes.html</a><br/><br/>')
f.write('<a href="./liquor_types.html">View liquor_types.html</a><br/><br/>')
f.write('</body></html>')
f.close()


#--------------------------------------------------------------------------------------------

#Add recipes to db
# r = drinkz.recipes.Recipe('whiskey on the rocks', [('whiskey',
#                                                    '4 oz')])
# drinkz.db.add_recipe(r)
# r = drinkz.recipes.Recipe('vodka martini', [('vodka', '6 oz'),
#                                             ('vermouth', '1.5 oz')])
# drinkz.db.add_recipe(r)

# r = drinkz.recipes.Recipe('vomit inducing martini', [('orange juice',
#                                                       '6 oz'),
#                                                      ('vermouth',
#                                                       '1.5 oz')])
# drinkz.db.add_recipe(r)

#Create the liquor_types.html file
f = open("./html/recipes.html", "w")
f.write('<html><head></head><body><ul>')
f.write('<h1>Recipes</h1><br/>')

recipeList = list(drinkz.db.get_all_recipes())
for(n) in recipeList:
	f.write('<li> Name: ' + str(n._name) )
	if(len(n.need_ingredients()) == 0):
		f.write(' - Yes' )
	else:
		f.write(' - No')
	f.write('</li>')

f.write('</ul></body>')
f.write('<a href="./index.html">View index.html</a><br/><br/>')
f.write('<a href="./liquor_types.html">View liquor_types.html</a><br/><br/>')
f.write('<a href="./inventory.html">View inventory.html</a><br/><br/>')
f.write('</html>')
f.close()

