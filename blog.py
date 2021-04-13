import sqlite3
import sys
import argparse


data = {"meals": ("breakfast", "brunch", "lunch", "supper"),
        "ingredients": ("milk", "cacao", "strawberry", "blueberry", "blackberry", "sugar"),
        "measures": ("ml", "g", "l", "cup", "tbsp", "tsp", "dsp", "")}

parser = argparse.ArgumentParser()
parser.add_argument('db')
parser.add_argument('--ingredients')
parser.add_argument('--meals')


def create_tables(cur):
    cur.execute('CREATE TABLE IF NOT EXISTS measures (measure_id INTEGER PRIMARY KEY, measure_name TEXT UNIQUE)')
    cur.execute('CREATE TABLE IF NOT EXISTS ingredients (ingredient_id INTEGER PRIMARY KEY, ingredient_name TEXT NOT NULL UNIQUE)')
    cur.execute('CREATE TABLE IF NOT EXISTS meals (meal_id INTEGER PRIMARY KEY, meal_name TEXT NOT NULL UNIQUE)')
    cur.execute('CREATE TABLE IF NOT EXISTS recipes (recipe_id INTEGER PRIMARY KEY, recipe_name TEXT NOT NULL, recipe_description TEXT)')


def create_serve_table(cur):
    cur.execute('PRAGMA foreign_keys = ON;')
    cur.execute('CREATE TABLE IF NOT EXISTS serve (serve_id INTEGER PRIMARY KEY, meal_id INTEGER NOT NULL, recipe_id INTEGER NOT NULL, FOREIGN KEY(meal_id) REFERENCES meals(meal_id), FOREIGN KEY(recipe_id) REFERENCES recipes(recipe_id))')


def create_quantity_table(cur):
    cur.execute('CREATE TABLE IF NOT EXISTS quantity (quantity_id INTEGER PRIMARY KEY, quantity INTEGER NOT NULL, recipe_id INTEGER NOT NULL, measure_id INTEGER NOT NULL, ingredient_id INTEGER NOT NULL, FOREIGN KEY(recipe_id) REFERENCES recipes(recipe_id), FOREIGN KEY(measure_id) REFERENCES measures(measure_id), FOREIGN KEY(ingredient_id) REFERENCES ingredients(ingredient_id))')


def fill_ingredients_table(cur):
    i = 1
    for ingredient in data['ingredients']:
        cur.execute('INSERT INTO ingredients (ingredient_id, ingredient_name) values (?, ?)', (i, ingredient))
        i += 1


def fill_meals_table(cur):
    i = 1
    for meal in data['meals']:
        cur.execute('INSERT INTO meals (meal_id, meal_name) values (?, ?)', (i, meal))
        i += 1


def fill_measures_table(cur):
    i = 1
    for measure in data['measures']:
        cur.execute('INSERT INTO measures (measure_id, measure_name) values (?, ?)', (i, measure))
        i += 1

def fill_recipes_table(cur):
    while True:
        print('Pass the empty recipe name to exit.')
        r_n = input('Recipe name:')
        if r_n == '':
            break
        r_d = input('Recipe description:')
        row_id = cur.execute('INSERT INTO recipes (recipe_name, recipe_description) values (?, ?)', (r_n, r_d)).lastrowid
        select_all_from_meals(cur, row_id)


def fill_qty_table(cur, recipe_id):
    while True:
        u_input = input('Input quantity of ingredient <press enter to stop>:')
        if u_input == '':
            break
        else:
            ingredient_list = u_input.split(' ')
            qty = int(ingredient_list[0])
            sql = 'SELECT ingredient_id FROM ingredients WHERE ingredient_name LIKE "{}%"'.format(ingredient_list[-1])
            ingredient = cur.execute(sql).fetchall()
            if len(ingredient) != 1:
                print('The ingredient is not conclusive!')
                continue
            else:
                ingr = ingredient[0][0]
            if len(ingredient_list) == 2:
                msr = measure_noname
            else:
                sql = 'SELECT measure_id FROM measures WHERE measure_name LIKE "{}%"'.format(ingredient_list[1])
                measure = cur.execute(sql).fetchall()
                if len(measure) !=  1:
                    print('The measure is not conclusive!')
                    continue
                else:
                    msr = measure[0][0]
            cur.execute('INSERT INTO quantity (quantity, recipe_id, measure_id, ingredient_id) VALUES (?, ?, ?, ?)', (int(qty), recipe_id, msr, ingr))

def select_all_from_meals(cur, recipe_id):
    all_meals = cur.execute('SELECT * FROM meals').fetchall()
    for meal in all_meals:
        print(str(meal[0]) + ')', meal[1] + ' ', end='')
    print('\n')
    meals = input('Enter proposed meals separated by a space:').split(' ')
    for meal_ in meals:
        cur.execute('INSERT INTO serve (meal_id, recipe_id) VALUES (?, ?)', (meal_, recipe_id))
    fill_qty_table(cur, recipe_id)

meals, ingredients = None, None
args = parser.parse_args()

conn = sqlite3.connect('./' + args.db)
if args.meals:
    meals = args.meals.split(',')

if args.ingredients:
    ingredients = args.ingredients.split(',')

cur = conn.cursor()
if meals == None and ingredients == None:
    create_tables(cur)
    conn.commit()
    create_serve_table(cur)
    create_quantity_table(cur)
    conn.commit()
    fill_ingredients_table(cur)
    fill_meals_table(cur)
    fill_measures_table(cur)
    conn.commit()
    measure_noname = cur.execute('SELECT measure_id FROM measures where measure_name = ""').fetchall()[0][0]
    fill_recipes_table(cur)
    conn.commit()
else:
    meal_id_list, ingredients_list, recipe_id_list = [], [], []
    try:
        for meal in meals:
            meal_id_list.append(int(cur.execute('SELECT meal_id FROM meals WHERE meal_name like "{}"'.format(meal)).fetchone()[0]))

        for ingr in ingredients:
            ingredients_list.append(int(cur.execute('SELECT ingredient_id FROM ingredients WHERE ingredient_name like "{}"'.format(ingr)).fetchone()[0]))
    except TypeError:
        print('There are no such recipes in the database.')
        conn.close()
        exit()

    recipes_by_meal = cur.execute('SELECT distinct recipe_id FROM serve WHERE meal_id in ({})'.format(",".join([str(id) for id in meal_id_list]))).fetchall()
    sql = ''
    for id in ingredients_list:
        if sql == '':
            sql = 'SELECT distinct recipe_id FROM quantity WHERE ingredient_id = ' + str(id)
        else:
            sql += ' and exists (SELECT distinct recipe_id FROM quantity WHERE ingredient_id = ' + str(id) + ')'

    recipes_by_ingreds = cur.execute(sql).fetchall()
    # szukamy set intersection tych mnóstw
    recipes = list(set(recipes_by_meal) & set(recipes_by_ingreds))
    if recipes == []:
        print('There are no such recipes in the database.')
    else:
        for recipe in recipes:
            recipe_id_list.append(recipe[0])
        recipes_list = cur.execute('SELECT recipe_name FROM recipes WHERE recipe_id in ({}) ORDER BY recipe_id'.format(",".join([str(id) for id in recipe_id_list]))).fetchall()
        recipe_names = ''
        for recipe in recipes_list:
            recipe_names += recipe[0] + ', '
        print('Recipes selected for you:', recipe_names[:-2])
conn.close()


