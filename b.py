import click
import inquirer
import pandas as pd
import datetime  as dt
import sys, os
#TO DO:
#implement functions
#command mode
#setup!!
#GH deploy :) 
class Eco:

    def __init__(self):
        tables_path = os.path.abspath(sys.argv[0] + "/../tables")
        assert os.path.exists(tables_path), "Have you lost your tables folder?" 
        
        self.tables_path = tables_path
        self.income_path = tables_path + "/income.csv"
        self.spending_path = tables_path + "/spending.csv"
        self.saving_path = tables_path + "/savings.csv"

        self.income_df = pd.read_csv(self.income_path)
        self.spending_df = pd.read_csv(self.spending_path)
        self.saving_df = pd.read_csv(self.saving_path)
        self.intro()
    
    def intro(self):
        while True:
            choice = inquirer.list_input("fun fact: mitch caught a body bout a week ago",
                                        choices=['flow', 'config', 'exit'])
            if choice == 'flow':
                choice = inquirer.list_input("I made a new",
                                            choices=['spending', 'saving', 'income'])
                if choice == 'spending':
                    self.spending_df = self.spending_df.append(self.query(self.spending_df.columns), ignore_index=True)
                    self.spending_df.to_csv(self.spending_path, index=False)
                elif choice == 'income':
                    self.query(self.income_df.columns)
                elif choice == 'saving':
                    self.query(self.saving_df.columns)
            elif choice == 'config':
                self.config()
            elif choice == 'exit':
                return 0


    def config(self):
        while(True):
            choice = inquirer.list_input("", choices=['initialize', 'add source of income', 'add spending category', 'back'])
            if choice == 'initialize':
                income = inquirer.text(message="Enter your sources of income divided by comma eg. 'job, youtube, crime'")
                spending = inquirer.text(message="Enter your spending categories divided by comma eg. food, rent, hobby'")
                savings = inquirer.text(message="Enter your savings categories divided by comma eg. rent, future, guitar")
                income_cats = ['date'] + income.replace(' ', '').split(',') + ['sum']
                spending_cats = ['date'] + spending.replace(' ', '').split(',') + ['sum']
                sav_cats = ['date'] + savings.replace(' ', '').split(',') + ['sum']
                pd.DataFrame(columns=income_cats).to_csv(self.income_path, index=False)
                pd.DataFrame(columns=spending_cats).to_csv(self.spending_path, index=False)
                pd.DataFrame(columns=sav_cats).to_csv(self.saving_path, index=False)
                click.secho("You're set my friend!", fg='green')
            elif choice == 'add source of income':
                pass
            elif choice == 'add spending category':
                pass
            elif choice == 'back':
                intro()

    def query(self, columns):
        new_row = pd.Series(index=columns, dtype='object')
        while(True):
            choice = inquirer.list_input("",
                    choices=list(columns)[1:-1] + ['back'])
            if choice == 'back':
                break    
            else:
                amount = round(float(inquirer.text(message = 'Amount')), 2)
                new_row.at[choice] = amount
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
        df = pd.read_csv(saving_path)
        data = pd.Series([dt.date.today().strftime("%d/%m/%y"), r, f])
        df.append(data, ignore_index=True).to_csv(saving_path, index = False)

    def report():
        df = pd.read_csv(daily_path)
        sav = pd.read_csv(saving_path)
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
