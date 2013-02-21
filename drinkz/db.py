"""
Database functionality for drinkz information.

_recipe_db is stored as a dictionary because of two reasons:
    1) Recipes will be unique based on their names, and therefore using
        a dictionary with a name key is ideal, a list would be a bad idea.
    2) Since there is a specific get_recipe function that passes a name string
        as a parameter, a dictionary is ideal to retrieve the recipe from the 
        database, as it is just the key of _recipe_db.
"""

import drinkz.recipes

# private singleton variables at module level
_bottle_types_db = set()
_inventory_db = dict()
_recipe_db = dict()

def _reset_db():
    "A method only to be used during testing -- toss the existing db info."
    global _bottle_types_db, _inventory_db, _recipe_db
    _bottle_types_db = set()
    _inventory_db = dict()
    _recipe_db = dict()

# exceptions in Python inherit from Exception and generally don't need to
# override any methods.
class LiquorMissing(Exception):
    pass

class DuplicateRecipeName(Exception):
    pass

def add_recipe(r):
    "Add the recipe to the recipe database"
    if(r._name not in _recipe_db):
        _recipe_db[r._name] = r
    else:
        err = "Duplicated recipe name: '%s'" % (r._name)
        raise DuplicateRecipeName(err)

def get_recipe(name):
    "Get a recipe, via a name string parameter"
    if(name in _recipe_db):
        return _recipe_db[name]

def get_all_recipes():
    "Return all of the recipes in the database"
    for k, r in _recipe_db.iteritems():
        yield r

def add_bottle_type(mfg, liquor, typ):
    "Add the given bottle type into the drinkz database."
    _bottle_types_db.add((mfg, liquor, typ))

def _check_bottle_type_exists(mfg, liquor):
    for (m, l, _) in _bottle_types_db:
        if mfg == m and liquor == l:
            return True

    return False

def check_inventory_for_type(alcoholType):
    alcoholTypes = []
    for (m, l, t) in _bottle_types_db:
            if t == alcoholType:
                amount = get_liquor_amount(m,l)
                alcoholTypes.append((m,l,t,amount))

    return alcoholTypes



def add_to_inventory(mfg, liquor, amount):
    "Add the given liquor/amount to inventory."
    if not _check_bottle_type_exists(mfg, liquor):
        err = "Missing liquor: manufacturer '%s', name '%s'" % (mfg, liquor)
        raise LiquorMissing(err)

    mlAmount = 0
    number, unit = amount.split();

    # Check what unit it is and convert to mL
    if unit == "ml" or unit == "mL" or unit == "ML":
        mlAmount += float(number)
    elif unit == "oz" or unit == "OZ" or unit == "Oz":
        mlAmount += float(float(number)*29.5735)
    elif unit == "gallon" or unit == "gallons":
        mlAmount += float(float(number)*3785.41)
    elif unit == "liter" or unit == "Liter":
        mlAmount += float(float(number)*1000.0)
    else:
        assert False, 'Error: Incorrect Unit'

    if (mfg,liquor) in _inventory_db:
        #inventoryAmount,inventoryUnit = _inventory_db[(mfg, liquor)].split()
        totalAmount = float(_inventory_db[(mfg, liquor)]) +  mlAmount
        _inventory_db[(mfg, liquor)] = str(totalAmount)
    else:
        _inventory_db[(mfg,liquor)] = str(mlAmount)

def check_inventory(mfg, liquor):
    for (m, l) in _inventory_db:
        if mfg == m and liquor == l:
            return True
        
    return False

def get_liquor_amount(mfg, liquor):
    "Retrieve the total amount of any given liquor currently in inventory."
    return float(_inventory_db[mfg,liquor])

def get_all_bottle_types():
    return _bottle_types_db

def get_all_liquor_amounts():
    return _inventory_db

def get_liquor_inventory():
    "Retrieve all liquor types in inventory, in tuple form: (mfg, liquor)."
    for (m, l) in _inventory_db:
        yield m, l
