from datetime import date
from flask import (
    Flask,
    request,
)
from budget import (
    History,
    Event,
    Category,
    Title,
    SEK,
)

HISTORY = History()
HISTORY.load(filename='data.sav')
APP = Flask(__name__)


@APP.route('/')
def events():
    response = '<a href="/categories">Categories</a><br/><br/>'
    response += '<table>'
    for event in HISTORY.events_between(date_from=date(2018, 1, 1), date_to=date(2018, 1, 31)):
        response += f'''
        <tr>
            <td>{event.title.name}</td>
            <td style="text-align: right">{event.amount.amount}</td>
            <td>{event.category}</td>
        </tr>'''
    response += '</table>'
    return response


@APP.route('/categories', methods=['GET', 'POST'])
def categories():
    if request.method == 'POST':
        category = request.form.get('category')
        if category is not None:
            HISTORY.create_category(name=category)
            HISTORY.save(filename='data.sav')

    response = '<a href="/">Events</a><br/><br/>'
    response += str([x.name for x in HISTORY.categories])
    response += '''
    <form action="/categories" method="post">
        Add category: <input type="text" name="category">
        <input type="submit">
    </form>
    '''
    return response


if __name__ == '__main__':
    APP.run('0.0.0.0', 8081)
