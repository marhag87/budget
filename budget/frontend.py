from datetime import date
from flask import (
    Flask,
    request,
    render_template,
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
APP = Flask(__name__, static_url_path='/static')


@APP.route('/')
def index():
    return render_template('index.html')


@APP.route('/events')
def events():
    return render_template(
        'events.html',
        events=HISTORY.events_between(date_from=date(2018, 1, 1), date_to=date(2018, 1, 31)),
        categories=HISTORY.categories,
    )


@APP.route('/categories', methods=['GET', 'POST'])
def categories():
    if request.method == 'POST':
        category = request.form.get('category')
        if category is not None:
            HISTORY.create_category(name=category)
            HISTORY.save(filename='data.sav')

    return render_template(
        'categories.html',
        categories=HISTORY.categories,
    )


if __name__ == '__main__':
    APP.run('0.0.0.0', 8081)
