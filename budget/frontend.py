from datetime import date
from flask import Flask
from budget import (
    History,
    Event,
    Category,
    Title,
    SEK,
)

APP = Flask(__name__)


@APP.route('/')
def index():
    history = History()
    history.load(filename='data.sav')
    response = '<table>'
    for event in history.events_between(date_from=date(2018, 1, 1), date_to=date(2018, 1, 31)):
        response += f'''
        <tr>
            <td>{event.title.name}</td>
            <td style="text-align: right">{event.amount.amount}</td>
            <td>{event.category}</td>
        </tr>'''
    response += '</table>'
    return response


if __name__ == '__main__':
    APP.run(port=8081)
