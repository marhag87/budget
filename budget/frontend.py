from flask import Flask
from budget import Budget

APP = Flask(__name__)


@APP.route('/')
def index():
    budget = Budget()
    budget.insert_events()
    budget.create_category('Groceries')
    budget.create_category('Electronics')
    budget.create_category('Games')
    budget.set_category(1, 1)
    budget.set_category(3, 2)
    budget.set_category(19, 3)
    response = '<table>'
    previous_category = ''
    for title, date, amount, balance, category in budget.get_events(2018, 1):
        if previous_category != category:
            previous_category = category
            response += f'<tr><td style="font-weight: bold">{category}</td><td></td></tr>'
        amount = amount/100.0
        response += f'<tr><td>{title}</td><td style="text-align: right">{amount:.2f}</td></tr>'
    response += '</table>'
    return response


if __name__ == '__main__':
    APP.run(port=8081)
