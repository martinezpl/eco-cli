import inquirer
import numpy as np
import pandas as pd
import datetime  as dt
import sys, os

# WILD IDEAS:
# external dataframe monitor
# plots

# TO DO:
# structure
# setup!!
# GH deploy :) 

class bc:
    MAGENTA = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class Eco:
    def __init__(self):
        tables_path = os.path.abspath(sys.argv[0] + "/../tables")
        assert os.path.exists(tables_path), "Have you lost your tables folder? Create a new one." 
        self.tables_path = tables_path
        self.income_path = tables_path + "/income.csv"
        self.spendings_path = tables_path + "/spendings.csv"
        self.savings_path = tables_path + "/savings.csv"
        self.daily_path = tables_path + "/daily.csv"
        try:
            self.income_df = pd.read_csv(self.income_path)
            self.spendings_df = pd.read_csv(self.spendings_path)
            self.savings_df = pd.read_csv(self.savings_path)
            self.update_daily()
        except:
            print(f"{bc.BOLD}{bc.GREEN}~~~~~~~~ Hi! Let's customize the program to your lifestyle. ~~~~~~~{bc.ENDC}")
            self.initialize()
    
    def update_daily(self):
        self.daily_df = pd.concat([self.income_df, self.spendings_df, self.savings_df], 
                ignore_index=True, levels=['income', 'spendings', 'savings'], 
                copy=False).groupby('date', as_index=False).sum().reset_index(drop=True).drop('sum', axis=1)
        self.daily_df['in'] = self.income_df[['date', 'sum']].groupby('date').transform('sum')
        self.daily_df['out'] = self.spendings_df[['date', 'sum']].groupby('date').transform('sum')
        self.daily_df['saved'] = self.savings_df[['date', 'sum']].groupby('date').transform('sum')
        self.daily_df.to_csv(self.daily_path, index=False)

    def intro(self):
        last_choice = None
        while True:
            choice = inquirer.list_input("fun fact: mitch caught a body bout a week ago",
                                        choices=['flow', 'summary', 'config', 'exit'],
                                        default=last_choice)
            if choice == 'flow':
                self.flow()
                last_choice = 'flow'
            elif choice == 'summary':
                try:
                    self.summary()
                except:
                    print("No entries.")
                last_choice = choice
            elif choice == 'config':
                self.config()
                last_choice = choice
            elif choice == 'exit':
                return 0

    def flow(self):
        last_choice = None
        while(True):
            choice = inquirer.list_input("New",
                                        choices=['spendings', 'savings', 'income', 'back'],
                                        default = last_choice)
            if choice == 'spendings':
                self.spendings_df = self.spendings_df.append(self.query(self.spendings_df.columns), ignore_index=True)
                self.spendings_df.to_csv(self.spendings_path, index=False)
                last_choice = choice
            elif choice == 'income':
                self.income_df = self.income_df.append(self.query(self.income_df.columns), ignore_index=True)
                self.income_df.to_csv(self.income_path, index=False)
                last_choice = choice
            elif choice == 'savings': 
                self.savings_df = self.savings_df.append(self.query(self.savings_df.columns), ignore_index=True)
                self.savings_df.to_csv(self.savings_path, index=False)
                last_choice = choice
            elif choice == 'back':
                return

    def initialize(self):
        income = inquirer.text(message="First, enter your sources of income divided by comma eg. job, freelance, crime")
        spendings = inquirer.text(message="Now, enter your spending categories divided by comma eg. food, bills, hobby")
        savings = inquirer.text(message="Lastly, enter your saving categories divided by comma eg. rent, future, guitar")
        income_cats = ['date'] + income.replace(' ', '').split(',') + ['sum']
        spendings_cats = ['date'] + spendings.replace(' ', '').split(',') + ['sum']
        sav_cats = ['date'] + savings.replace(' ', '').split(',') + ['sum']
        pd.DataFrame(columns=income_cats).to_csv(self.income_path, index=False)
        pd.DataFrame(columns=spendings_cats).to_csv(self.spendings_path, index=False)
        pd.DataFrame(columns=sav_cats).to_csv(self.savings_path, index=False)
        self.__init__()
        print(f"{bc.UNDERLINE}{bc.GREEN}You're set my friend!{bc.ENDC}\n")
        input()

    def modify(self, df, path):
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

    def config(self):
        last_choice = None
        while(True):
            choice = inquirer.list_input("", choices=['initialize', 'modify sources of income', 'modify spending categories', 'modify saving categories', 'back'],
                                        default = last_choice)
            if choice == 'initialize':
                self.initialize()
                break
            elif choice == 'modify sources of income':
                self.income_df = self.modify(self.income_df, self.income_path)
                last_choice = choice
            elif choice == 'modify spending categories':
                self.spendings_df = self.modify(self.spendings_df, self.spendings_path)
                last_choice = choice
            elif choice == 'modify saving categories':
                self.savings_df = self.modify(self.savings_df, self.savings_path)
                last_choice = choice
            elif choice == 'back':
                return 0

    def query(self, columns):
        new_row = pd.Series(index=columns, dtype='object')
        last_choice = None
        while(True):
            choice = inquirer.list_input("",
                    choices=list(columns)[1:-1] + ['back'],
                    default = last_choice)
            if choice == 'back':
                break    
            else:
                try:
                    amount = round(float(inquirer.text(message = 'Amount')), 2)
                    new_row.at[choice] = amount
                except:
                    print("Don't be naughty!")
                last_choice = choice
        if new_row.notna().any():
            new_row.at['sum'] = new_row.sum()
            new_row.at['date'] = dt.date.today().strftime("%d/%m/%y")
            return new_row
        return

    def summary(self):
        self.update_daily()
        assert self.daily_df.shape[0] > 0
        last_week_dates = [(dt.date.today() - dt.timedelta(days=x)).strftime("%d/%m/%y") for x in list(range(0, 7))]
        last_week = self.daily_df[self.daily_df.date.apply(lambda x: any(date for date in last_week_dates if date in x))]
        this_month = self.daily_df.loc[self.daily_df.date.str.contains(dt.date.today().strftime("%m/%y"))]
        print("============================================================================================")
        print(last_week)
        print("============================================================================================")
        print(f"{bc.BOLD}{bc.MAGENTA}WALLET:{bc.ENDC} {round((self.daily_df['in'].sum() - self.daily_df['out'].sum() - self.daily_df['saved'].sum()), 2)} PLN\n")
        print(f"{bc.BOLD}\nLast 7 days:{bc.ENDC}")
        print("------------------------------------------------------------------------------")
        print(f"{bc.BOLD}{bc.CYAN}EARNED:{bc.ENDC} {last_week['in'].sum()} PLN\t|\t",
                f"{bc.BOLD}{bc.RED}SPENT:{bc.ENDC} {last_week['out'].sum()} PLN\t|\t",
                f"{bc.BOLD}{bc.GREEN}SAVED:{bc.ENDC} {last_week['saved'].sum()} PLN")
        
        print(f"{bc.BOLD}\nThis month:{bc.ENDC}")
        print("------------------------------------------------------------------------------")
        print(f"{bc.BOLD}{bc.CYAN}EARNED:{bc.ENDC} {this_month['in'].sum()} PLN\t|\t",
                f"{bc.BOLD}{bc.RED}SPENT:{bc.ENDC} {this_month['out'].sum()} PLN\t|\t",
                f"{bc.BOLD}{bc.GREEN}SAVED:{bc.ENDC} {this_month['saved'].sum()} PLN")
       
        print(f"{bc.BOLD}\nOverall:{bc.ENDC}")
        print("------------------------------------------------------------------------------")
        print(f"{bc.BOLD}{bc.CYAN}EARNED:{bc.ENDC} {self.daily_df['in'].sum()} PLN\t|\t",
                f"{bc.BOLD}{bc.RED}SPENT:{bc.ENDC} {self.daily_df['out'].sum()} PLN\t|\t",
                f"{bc.BOLD}{bc.GREEN}SAVED:{bc.ENDC} {self.daily_df['saved'].sum()} PLN\n")
        input()

if __name__ == "__main__":
    Eco().intro()
