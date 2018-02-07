from datetime import date
from pyramid.response import Response
from pyramid.config import Configurator
from wsgiref.simple_server import make_server
from budget import (
    History,
    Event,
    Category,
    Title,
    SEK,
)


class Budget:
    def __init__(self, request):
        self.request = request
        self.history = History()
        self.history.load(filename='data.sav')


class Events(Budget):
    def __call__(self):
        response = '<table>'
        for event in self.history.events_between(date_from=date(2018, 1, 1), date_to=date(2018, 1, 31)):
            response += f'''
            <tr>
                <td>{event.title.name}</td>
                <td style="text-align: right">{event.amount.amount}</td>
                <td>{event.category}</td>
            </tr>'''
        response += '</table>'
        return Response(response)


class Categories(Budget):
    def __call__(self):
        return Response(str([x.name for x in self.history.categories]))


if __name__ == '__main__':
    with Configurator() as config:
        config.add_route('index', '/')
        config.add_view(Events, route_name='index')
        config.add_route('categories', '/categories')
        config.add_view(Categories, route_name='categories')
        app = config.make_wsgi_app()
    server = make_server('0.0.0.0', 8081, app)
    server.serve_forever()
