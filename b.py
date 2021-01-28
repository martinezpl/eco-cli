import click
import inquirer
import pandas as pd
import datetime  as dt
import sys, os

tables_path = os.path.abspath(sys.argv[0] + "/../tables")
daily_path = tables_path + "/daily.csv"
sav_path = tables_path + "/savings.csv"

#TO DO:
#resolve the issue on income/spendings csv splitting
#implement functions
#command mode
#setup!!
#GH deploy :) 

def config():
    choice = inquirer.list_input("", choices=['initialize', 'add source of income', 'add spending category'])
    if choice == 'initialize':
        income = inquirer.text(message="Enter your sources of income divided by comma eg. 'job, youtube, crime'")
        spendings = inquirer.text(message="Enter your spending categories divided by comma eg. food, rent, hobby'")
        savings = inquirer.text(message="Enter your savings categories divided by comma eg. rent, future, guitar")
        cats = ['date'] + income.replace(' ', '').split(',') + spendings.replace(' ', '').split(',') + ['in', 'out']
        pd.DataFrame(columns=cats).to_csv(daily_path, index=False)
        savs = ['date'] + savings.replace(' ', '').split(',')
        pd.DataFrame(columns=savs).to_csv(sav_path, index=False)
        click.secho("You're set my friend!", fg='green')
    elif choice == 'add source of income':
        pass
    elif choice == 'add spending category':
        pass

def spending(df):
    choice = inquirer.list_input("",
            choices=list(df.columns)[1:-2])
def earning(df):
    choice = inquirer.list_input("",
            choices=list(df.columns)[1:-2])
def saving(df):
    choice = inquirer.list_input("",
             choices=list(df.columns)[1:])

def intro():
    choice = inquirer.list_input("fun fact: mitch caught a body bout a week ago",
                                choices=['flow', 'config'])
    if choice == 'flow':
        choice = inquirer.list_input("I made a new",
                                    choices=['spending', 'saving', 'earning'])
        if choice == 'spending':
            spending(pd.read_csv(daily_path))
        elif choice == 'earning':
            earning(pd.read_csv(daily_path))
        elif choice == 'saving':
            saving(pd.read_csv(sav_path))
    elif choice == 'config':
        config()


def flow(f, w, t, b, h, fun, d, l, v, m, fam, o):
    daily = pd.read_csv(daily_path)
    earned = round(float(l + v + m + fam + o), 2)
    spent = round(float(f + w + t + b + h + fun + d), 2)
    data = pd.Series([dt.date.today().strftime("%d/%m/%y"), f, w, t, b, h, fun, d, l, v, m, fam, o, earned, spent], index=daily.columns)
    daily.append(data, ignore_index=True).to_csv(daily_path, index = False)

def save(r, f):
    df = pd.read_csv(sav_path)
    data = pd.Series([dt.date.today().strftime("%d/%m/%y"), r, f])
    df.append(data, ignore_index=True).to_csv(sav_path, index = False)

def report():
    df = pd.read_csv(daily_path)
    sav = pd.read_csv(sav_path)
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
    assert os.path.exists(tables_path), "Have you lost your tables folder?" 
    intro()
