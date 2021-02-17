import pandas as pd
import datetime as dt
import inquirer

class ANSI_escape_codes():
    MAGENTA = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def query(df):
    new_row = pd.Series(index=df.columns, dtype='object')
    last_choice = None
    while(True):
        choice = inquirer.list_input("",
                choices=list(df.columns)[1:-1] + ['back'],
                default = last_choice)
        if choice == 'back':
            break    
        else:
            try:
                amount = round(float(inquirer.text(message = 'Amount')), 2)
                new_row.at[choice] = amount
            except:
                print("Please, input a number.")
            last_choice = choice
    if new_row.notna().any():
        new_row.at['sum'] = new_row.sum()
        new_row.at['date'] = dt.date.today().strftime("%d/%m/%y")
        return new_row
    return

def modify(df, path):
    while(True):
        columns = df.columns
        choice = inquirer.list_input("Remove",
                choices=['add'] + list(columns)[1:-1] + ['back'])
        if choice == 'add':
            new_column = inquirer.text(message = 'Title')
            df.insert(loc = 1, column=new_column, value = 0)
            df.to_csv(path, index=False)
        elif choice == 'back':
            break
        else:
            df = df.drop(choice, axis=1)
            df.to_csv(path, index=False)
    return df

def init_prompt(arr):
    while(True):
        choice = inquirer.list_input("(Select a category to remove it)",
                choices=['add'] + arr + ['accept'])
        if choice == 'add':
            new_column = inquirer.text(message = 'Title')
            arr.append(new_column)
        elif choice == 'accept':
            return arr
        else:
            arr.pop(arr.index(choice))

def new_row_query(df, csv_path = None):
    df = df.append(query(df), ignore_index = True)
    if csv_path:
        df.to_csv(csv_path, index=False)
    return df

def new_eco_df(columns_arr=None, csv_path=None):
    df_cats = ['date'] + columns_arr + ['sum']
    df = pd.DataFrame(columns=df_cats)
    if csv_path:
        df.to_csv(csv_path, index=False)
    return df


