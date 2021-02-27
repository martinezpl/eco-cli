import inquirer
import pandas as pd
import datetime  as dt
import sys, os
from eco.eco_utils import get_fun_fact, query, modify, new_row_query, new_eco_df, init_prompt
from eco.eco_utils import ANSI_escape_codes as ec
from pathlib import Path

# WILD IDEAS:
# external dataframe monitor
# plots

class Eco:
    def __init__(self):
        tables_path = str(Path.home()) + "/eco_tables"
        if not os.path.exists(tables_path):
            os.mkdir(tables_path)
        self.tables_path = tables_path
        self.income_path = tables_path + "/income.csv"
        self.spendings_path = tables_path + "/spendings.csv"
        self.savings_path = tables_path + "/savings.csv"
        self.daily_path = tables_path + "/daily.csv"
        self.fun_fact = get_fun_fact()
        try:
            self.income_df = pd.read_csv(self.income_path)
            self.spendings_df = pd.read_csv(self.spendings_path)
            self.savings_df = pd.read_csv(self.savings_path)
            self.update_daily()
        except:
            print(f"{ec.BOLD}{ec.GREEN}~~~~~~~~ Hi! Let's customize the program to your lifestyle. ~~~~~~~{ec.ENDC}")
            self.initialize()
    
    def intro(self):
        last_choice = None
        print(f"{ec.GREEN}{dt.date.today().strftime('%d/%m/%y')}{ec.ENDC}\n" + self.fun_fact)
        while True:
            choice = inquirer.list_input("",
                                        choices=['flow', 'summary', 'config', 'exit'],
                                        default=last_choice)
            if choice == 'flow':
                self.flow()
            elif choice == 'summary':
                self.summary()
            elif choice == 'config':
                self.config()
            elif choice == 'exit':
                return 0
            last_choice = choice

    def flow(self):
        last_choice = None
        while(True):
            choice = inquirer.list_input("New",
                                        choices=['spendings', 'savings', 'income', 'back'],
                                        default = last_choice)
            if choice == 'spendings':
                self.spendings_df = new_row_query(self.spendings_df, self.spendings_path)
            elif choice == 'income':
                self.income_df = new_row_query(self.income_df, self.income_path)
            elif choice == 'savings': 
                self.savings_df = new_row_query(self.savings_df, self.savings_path)
            elif choice == 'back':
                return
            last_choice = choice
    
    def config(self):
        last_choice = None
        while(True):
            choice = inquirer.list_input("", choices=['initialize', 'modify sources of income', 'modify spending categories', 'modify saving categories', 'back'],
                                        default = last_choice)
            if choice == 'initialize':
                self.initialize()
                break
            elif choice == 'modify sources of income':
                self.income_df = modify(self.income_df, self.income_path)
            elif choice == 'modify spending categories':
                self.spendings_df = modify(self.spendings_df, self.spendings_path)
            elif choice == 'modify saving categories':
                self.savings_df = modify(self.savings_df, self.savings_path)
            elif choice == 'back':
                return 0
            last_choice = choice 
    
    def initialize(self):
        income = []
        spendings = []
        savings = []
        print(f"{ec.BOLD}First, enter your sources of {ec.CYAN}income{ec.ENDC}{ec.BOLD} eg. job, freelance, crime{ec.ENDC}")
        income = init_prompt(income) 
        print(f"{ec.BOLD}Now, enter your {ec.RED}spending{ec.ENDC}{ec.BOLD} categories eg. food, bills, hobby{ec.ENDC}")
        spendings = init_prompt(spendings)
        print(f"{ec.BOLD}Lastly, enter your {ec.GREEN}saving{ec.ENDC}{ec.BOLD} categories eg. rent, future, guitar{ec.ENDC}")
        savings = init_prompt(savings)
        self.income_df = new_eco_df(income, self.income_path)
        self.spendings_df = new_eco_df(spendings, self.spendings_path)
        self.savings_df = new_eco_df(savings, self.savings_path)
        print(f"{ec.UNDERLINE}{ec.GREEN}You're set my friend!{ec.ENDC}\n")
        input("Continue...")

    def update_daily(self):
        self.daily_df = pd.concat([self.income_df, self.spendings_df, self.savings_df], 
                ignore_index=True, levels=['income', 'spendings', 'savings'], 
                copy=False).groupby('date', as_index=False).sum().reset_index(drop=True).drop('sum', axis=1)
        self.daily_df['in'] = self.income_df[['date', 'sum']].groupby('date').transform('sum')
        self.daily_df['out'] = self.spendings_df[['date', 'sum']].groupby('date').transform('sum')
        self.daily_df['saved'] = self.savings_df[['date', 'sum']].groupby('date').transform('sum')
        self.daily_df = self.daily_df.fillna(0)
        self.daily_df.to_csv(self.daily_path, index=False)

    def summary(self):
        try:
            self.update_daily()
            assert self.daily_df.shape[0] > 0
        except:
            print("No entries.")
            input("Continue...")
            return 0
        last_week_dates = [(dt.date.today() - dt.timedelta(days=x)).strftime("%d/%m/%y") for x in list(range(0, 7))]
        last_week = self.daily_df[self.daily_df.date.apply(lambda x: any(date for date in last_week_dates if date in x))]
        this_month = self.daily_df.loc[self.daily_df.date.str.contains(dt.date.today().strftime("%m/%y"))]
        print("============================================================================================")
        print(last_week)
        print("============================================================================================")
        print(f"{ec.BOLD}{ec.MAGENTA}WALLET:{ec.ENDC} {round((self.daily_df['in'].sum() - self.daily_df['out'].sum() - self.daily_df['saved'].sum()), 2)} PLN\n")
        print(f"{ec.BOLD}\nLast 7 days:{ec.ENDC}")
        print("------------------------------------------------------------------------------")
        print(f"{ec.BOLD}{ec.CYAN}EARNED:{ec.ENDC} {last_week['in'].sum()} PLN\t|\t",
                f"{ec.BOLD}{ec.RED}SPENT:{ec.ENDC} {last_week['out'].sum()} PLN\t|\t",
                f"{ec.BOLD}{ec.GREEN}SAVED:{ec.ENDC} {last_week['saved'].sum()} PLN")
        
        print(f"{ec.BOLD}\nThis month:{ec.ENDC}")
        print("------------------------------------------------------------------------------")
        print(f"{ec.BOLD}{ec.CYAN}EARNED:{ec.ENDC} {this_month['in'].sum()} PLN\t|\t",
                f"{ec.BOLD}{ec.RED}SPENT:{ec.ENDC} {this_month['out'].sum()} PLN\t|\t",
                f"{ec.BOLD}{ec.GREEN}SAVED:{ec.ENDC} {this_month['saved'].sum()} PLN")
       
        print(f"{ec.BOLD}\nOverall:{ec.ENDC}")
        print("------------------------------------------------------------------------------")
        print(f"{ec.BOLD}{ec.CYAN}EARNED:{ec.ENDC} {self.daily_df['in'].sum()} PLN\t|\t",
                f"{ec.BOLD}{ec.RED}SPENT:{ec.ENDC} {self.daily_df['out'].sum()} PLN\t|\t",
                f"{ec.BOLD}{ec.GREEN}SAVED:{ec.ENDC} {self.daily_df['saved'].sum()} PLN\n")
        input("Continue...")

def main():
    Eco().intro()

if __name__ == "__main__":
    main()
