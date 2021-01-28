import click
import inquirer
import pandas as pd
import datetime  as dt
import sys, os

tables_path = os.path.abspath(sys.argv[0] + "/../tables")
daily_path = tables_path + "/daily.csv"
sav_path = tables_path + "/savings.csv"

@click.group(invoke_without_command=True)
@click.pass_context
def budget(ctx):
    if ctx.invoked_subcommand is None:
        click.echo("SPENDINGS: food; water; tickets; bills; hobby; fun; drugs;")
        click.echo("EARNINGS: lessons; video; mix; fam; other;")
    else:
        pass

@click.command()
@click.option('-f', default = 0.0)
@click.option('-w', default = 0.0)
@click.option('-t', default = 0.0)
@click.option('-b', default = 0.0)
@click.option('-h', default = 0.0)
@click.option('-fun', default = 0.0)
@click.option('-d', default = 0.0)
@click.option('-l', default = 0.0)
@click.option('-v', default = 0.0)
@click.option('-m', default = 0.0)
@click.option('-fam', default = 0.0)
@click.option('-o', default = 0.0)
def flow(f, w, t, b, h, fun, d, l, v, m, fam, o):
    daily = pd.read_csv(daily_path)
    earned = round(float(l + v + m + fam + o), 2)
    spent = round(float(f + w + t + b + h + fun + d), 2)
    data = pd.Series([dt.date.today().strftime("%d/%m/%y"), f, w, t, b, h, fun, d, l, v, m, fam, o, earned, spent], index=daily.columns)
    daily.append(data, ignore_index=True).to_csv(daily_path, index = False)

@click.command()
@click.option('-r', default= 0.0)
@click.option('-f', default= 0.0)
def save(r, f):
    df = pd.read_csv(sav_path)
    data = pd.Series([dt.date.today().strftime("%d/%m/%y"), r, f])
    df.append(data, ignore_index=True).to_csv(sav_path, index = False)

@click.command()
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

budget.add_command(flow)
budget.add_command(report)
budget.add_command(save)

if __name__ == "__main__":
    if not os.path.exists(daily_path) or not os.path.exists(sav_path):
        b = {"date": [], "food": [], "water": [], "tickets": [], "bills": [], "hobby": [], "fun": [], "drugs": [], "lessons": [], "video": [], "mix": [], "fam": [], "other": [], "in": [], "out": []}
        pd.DataFrame(b).to_csv(daily_path, index = False)
        c = {"date": [], "rent": [], "future": []}
        pd.DataFrame(c).to_csv(sav_path, index = False)

    budget()
    #b = {"date": [], "food": [], "water": [], "tickets": [], "bills": [], "hobby": [], "fun": [], "drugs": [], "lessons": [], "video": [], "mix": [], "fam": [], "other": [], "in": [], "out": []}
