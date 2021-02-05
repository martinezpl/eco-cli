import click
import inquirer
import pandas as pd
import datetime  as dt
import sys, os

#TO DO:
#update_daily during reports
#implement functions
#command mode
#setup!!
#GH deploy :) 
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
        except:
            click.secho("~~~~~~~~ Hi! Let's customize the program to your lifestyle. ~~~~~~~", bold=True, color='blue')
            self.initialize()
        self.intro()
    
    def update_daily(self):
        self.daily_df = pd.concat([self.income_df, self.spendings_df, self.savings_df], 
                ignore_index=True, levels=['income', 'spendings', 'savings'], 
                copy=False).groupby('date', as_index=False).sum().reset_index(drop=True).drop('sum', axis=1)
        self.daily_df['in'] = self.income_df[['date', 'sum']].groupby('date').transform('sum')
        self.daily_df['out'] = self.spendings_df[['date', 'sum']].groupby('date').transform('sum')
        self.daily_df['saved'] = self.savings_df[['date', 'sum']].groupby('date').transform('sum')
        self.daily_df.to_csv(self.daily_path, index=False)

    def intro(self):
        while True:
            choice = inquirer.list_input("fun fact: mitch caught a body bout a week ago",
                                        choices=['flow', 'config', 'exit'])
            if choice == 'flow':
                while(True):
                    choice = inquirer.list_input("I made a new",
                                                choices=['spendings', 'savings', 'income', 'back'])
                    if choice == 'spendings':
                        self.spendings_df = self.spendings_df.append(self.query(self.spendings_df.columns), ignore_index=True)
                        self.spendings_df.to_csv(self.spendings_path, index=False)
                    elif choice == 'income':
                        self.income_df = self.income_df.append(self.query(self.income_df.columns), ignore_index=True)
                        self.income_df.to_csv(self.income_path, index=False)
                    elif choice == 'savings': 
                        self.savings_df = self.savings_df.append(self.query(self.savings_df.columns), ignore_index=True)
                        self.savings_df.to_csv(self.savings_path, index=False)
                    elif choice == 'back':
                        break
            elif choice == 'config':
                self.config()
            elif choice == 'exit':
                return 0

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
        pd.DataFrame().to_csv(self.daily_path, index=False)
        click.secho("You're set my friend!", fg='green')

    def config(self):
        while(True):
            choice = inquirer.list_input("", choices=['initialize', 'add source of income', 'add spendings category', 'back'])
            if choice == 'initialize':
                self.initialize()    
            elif choice == 'add source of income':
                pass
            elif choice == 'add spendings category':
                pass
            elif choice == 'back':
                return 0

    def query(self, columns):
        new_row = pd.Series(index=columns, dtype='object')
        while(True):
            choice = inquirer.list_input("",
                    choices=list(columns)[1:-1] + ['back'])
            if choice == 'back':
                break    
            else:
                try:
                    amount = round(float(inquirer.text(message = 'Amount')), 2)
                    new_row.at[choice] = amount
                except:
                    print("Don't be naughty!")
        if new_row.notna().any():
            new_row.at['sum'] = new_row.sum()
            new_row.at['date'] = dt.date.today().strftime("%d/%m/%y")
            return new_row
        return

    def flow(f, w, t, b, h, fun, d, l, v, m, fam, o):
        daily = pd.read_csv(daily_path)
        earned = round(float(l + v + m + fam + o), 2)
        spent = round(float(f + w + t + b + h + fun + d), 2)
        data = pd.Series([dt.date.today().strftime("%d/%m/%y"), f, w, t, b, h, fun, d, l, v, m, fam, o, earned, spent], index=daily.columns)
        daily.append(data, ignore_index=True).to_csv(daily_path, index = False)

    def save(r, f):
        df = pd.read_csv(savings_path)
        data = pd.Series([dt.date.today().strftime("%d/%m/%y"), r, f])
        df.append(data, ignore_index=True).to_csv(savings_path, index = False)

    def report():
        df = pd.read_csv(daily_path)
        sav = pd.read_csv(savings_path)
        last_week_dates = [(dt.date.today() - dt.timedelta(days=x)).strftime("%d/%m/%y") for x in list(range(0, 7))]
        mask = df.date.apply(lambda x: any(date for date in last_week_dates if date in x))
        week = df[mask]
        week_income = week["in"].sum()
        week_outcome = week["out"].sum()
        savings = sav['rent'].sum() + sav['future'].sum()
        print(week)
        click.secho("SAVINGS:", fg='yellow')
        click.echo("RENT: %s PLN            FUTURE: %s PLN" % (sav['rent'].sum(), sav['future'].sum()))
        click.secho("WALLET:", fg='cyan')
        click.echo("%s PLN" % round((week_income - week_outcome - savings), 2))
        click.secho("\nLast 7 days:", bold=True)
        click.echo("----------------------------------------------")
        click.secho("INCOME:", fg='green')
        click.secho("%s PLN" % week_income, blink = True)
        click.secho("SPENT:", fg='red')
        click.secho("%s PLN" % week_outcome, blink = True)

if __name__ == "__main__":
    Eco()
