import click
import inquirer
import pandas as pd
import datetime  as dt
import sys, os

tables_path = os.path.abspath(sys.argv[0] + "/../tables")
daily_path = tables_path + "/daily.csv"
sav_path = tables_path + "/savings.csv"

def intro(ctx):
    choice = inquirer.list_input("Public or private?",
                              choices=['public', 'private'])

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
    if not os.path.exists(daily_path) or not os.path.exists(sav_path):
        if not os.path.exists(tables_path):
            os.system('mkdir ' + tables_path)
        b = {"date": [dt.date.today()], "food": [0.0], "water": [0.0], "tickets": [0.0], "bills": [0.0], "hobby": [0.0], "fun": [0.0], "drugs": [0.0], "lessons": [0.0], "video": [0.0], "mix": [0.0], "fam": [0.0], "other": [0.0], "in": [0.0], "out": [0.0]}
        pd.DataFrame(b).to_csv(daily_path, index = False)
        c = {"date": [dt.date.today()], "rent": [0.0], "future": [0.0]}
        pd.DataFrame(c).to_csv(sav_path, index = False)

    report()
