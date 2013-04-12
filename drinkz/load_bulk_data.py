"""
Module to load in bulk data from text files.
"""

# ^^ the above is a module-level docstring.  Try:
#
#   import drinkz.load_bulk_data
#   help(drinkz.load_bulk_data)
#

import csv                              # Python csv package

from . import db, recipes

def checkEmptyOrCommented(fp):
    reader = csv.reader(fp)

    for line in reader:
        if len(line) == 0:
            print "Skip empty line"
            continue
        if line[0].startswith('#'):
            print "Skip commented string"
            continue
        if not line[0].strip():
            print "Skip empty string"
            continue

        yield line  

def load_recipes(fp):
    """
    Loads recipes from a CSV file

    Returns number of bottle types loaded
    """

    new_reader = checkEmptyOrCommented(fp)
    x = []
    n = 0

    for line in new_reader:

        try:
            values = line

            recipeNames = values[0]

            Ingredients = []
            firstValue = True
            i = 0
            while i < len(values):
                if(firstValue == False):
                    Ingredients.append((values[i], values[i+1]))
                    i+=2
                else:
                    firstValue = False
                    i+=1
                n += 1

            db.add_recipe(recipes.Recipe(values[0], Ingredients))
        except ValueError:
            print "ERROR: Malformed input line "
            print values
            pass
        except:
            print "ERROR: Error Unknown "
            print Ingredients
            print len(values)
            pass

    return n


def load_bottle_types(fp):
    """
    Loads in data of the form manufacturer/liquor name/type from a CSV file.

    Takes a file pointer.

    Adds data to database.

    Returns number of bottle types loaded
    """
    new_reader = checkEmptyOrCommented(fp)

    x = []
    n = 0

    for line in new_reader:
        try:
            (mfg, name, typ) = line
            n += 1
            db.add_bottle_type(mfg, name, typ)
        except ValueError:
            print "ERROR: Malformed input line"
            pass
        except:
            print "ERROR: Error Unknown"
            pass

    return n

def load_inventory(fp):
    """
    Loads in data of the form manufacturer/liquor name/amount from a CSV file.

    Takes a file pointer.

    Adds data to database.

    Returns number of records loaded.

    Note that a LiquorMissing exception is raised if bottle_types_db does
    not contain the manufacturer and liquor name already.
    """
    new_reader = checkEmptyOrCommented(fp)

    x = []
    n = 0
    for line in new_reader:
        try:
            (mfg, name, amount) = line
            n += 1
            db.add_to_inventory(mfg, name, amount)
        except ValueError:
            print "ERROR: Malformed input line"
            pass
        except:
            print "ERROR: Error Unknown"
            pass

    return n
