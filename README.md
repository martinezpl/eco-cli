# Eco CLI 

`eco` is a CLI tool for personal finance keeping. 

<img src="https://user-images.githubusercontent.com/64603095/109705701-58cce300-7b98-11eb-84cd-6eb0e73686d6.png" width="600" height="300" />

It provides a quick way to record your money flow through a simple interface. The records are arranged & kept in neat tables that are being stored in your local `$HOME/eco_tables` path. 

It takes about a minute an evening to keep your budget updated. Also, `eco` scraps a daily fun-fact to add a bit of motivation towards regular usage :) 

## Installation

Before installing, make sure you've added `pip` to your local __environment variable__. If you haven't, you will probably be notified during installation. Doing so allows `eco` to be a bash script. 

`pip install eco-cli`


## Usage

Simply type in `eco` in your terminal to invoke the program. First run will initialize a personalization process, in which you'll create flow categories. 

Use *flow* to register money flow. You can use *summary* for a quick budget peek, or, for a closer inspection, export the .csv files under `$HOME/eco_tables` to your tabular software of choice.  

Hints:

- __WALLET__ = *income - spendings - savings*

- Register income, before you register a saving.

- The three, main categories are a rolling sum (*running total*). Therefore, think of a saving category as of a sock. When you use your saved up money, you take the money out of the sock, so you **update the saving category with a negative number**. If you spent it - you register the amount taken as a spending. If you allocated it in a different sock - you update the right saving category.

![summary](https://user-images.githubusercontent.com/64603095/109706318-1657d600-7b99-11eb-8e29-cc45b16cf334.png)



