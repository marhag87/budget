from datetime import (
    date,
    datetime,
)
from money import Money
from typing import (
    List,
    Optional,
)
import pickle


class InvalidMoney(Exception):
    """The money entered is invalid"""
    pass


class InvalidDate(Exception):
    """The date entered is invalid"""
    pass


class SEK(Money):
    def __init__(self, *, amount='0'):
        super().__init__(amount=amount, currency='SEK')


class History:
    def __init__(self) -> None:
        self.history: List['Event'] = []
        self.titles: List['Title'] = []
        self.categories: List['Category'] = []

    def add_event(self, *, event: 'Event') -> None:
            self.history.append(event)

    def events_between(self, *, date_from: date, date_to: date) -> List['Event']:
        return [x for x in self.history if date_from <= x.transaction_date <= date_to]

    def create_title(self, *, new_title: str, category: Optional['Category'] = None) -> 'Title':
        if new_title in [x.name for x in self.titles]:
            for title in self.titles:
                if title.name == new_title:
                    return title
        added_title = Title(name=new_title, default_category=category)
        self.titles.append(added_title)
        return added_title

    def save(self, *, filename: str) -> None:
        with open(filename, 'wb') as file:
            pickle.dump(self, file, pickle.HIGHEST_PROTOCOL)

    def load(self, *, filename: str) -> None:
        with open(filename, 'rb') as file:
            loaded = pickle.load(file)
            self.history = loaded.history
            self.titles = loaded.titles
            self.categories = loaded.categories

    def load_events(self, *, filename: str) -> None:
        with open(filename) as file:
            lines = file.readlines()
            while lines:
                title = self.create_title(new_title=lines.pop(0).strip())
                self.add_event(
                    event=Event(
                        title=title,
                        transaction_date=lines.pop(0).strip(),
                        posting_date=lines.pop(0).strip(),
                        amount=lines.pop(0).strip(),
                        balance=lines.pop(0).strip(),
                    )
                )


class Title:
    def __init__(self, *, name: str, default_category: Optional['Category']) -> None:
        self.name: str = name
        self.default_category: Category = default_category

    @property
    def category(self) -> 'Category':
        return self.default_category

    @category.setter
    def category(self, category: 'Category') -> None:
        self.default_category = category


class Category:
    def __init__(self, *, name: str) -> None:
        self.name: str = name

    @property
    def dict(self):
        return {
            'name': self.name,
        }


class Event:
    def __init__(self, *, title: Title, transaction_date: str, posting_date: str,
                 amount: str, balance: str, category: Optional['Category'] = None) -> None:
        self.title = title
        self.transaction_date = self.clean_date(date_string=transaction_date)
        self.posting_date = self.clean_date(date_string=posting_date)
        self.amount = self.launder_money(money_string=amount)
        self.balance = self.launder_money(money_string=balance)
        self.overridden_category = category

    @property
    def dict(self) -> dict:
        return {
            'title': self.title.name,
            'transaction_date': self.transaction_date,
            'posting_date': self.posting_date,
            'amount': self.amount,
            'balance': self.balance,
            'default_category': self.title.category.name if self.title.category is not None else None,
            'overridden_category': self.overridden_category.name if self.overridden_category is not None else None,
        }

    @staticmethod
    def launder_money(*, money_string: str) -> SEK:
        money_string = money_string.replace(' ', '')
        money_string = money_string.replace(',', '.')
        if money_string == '':
            raise InvalidMoney
        return SEK(amount=money_string)

    @staticmethod
    def clean_date(*, date_string: str) -> date:
        if date_string == '':
            raise InvalidDate
        return datetime.strptime(date_string, "%Y-%m-%d").date()


if __name__ == '__main__':
    history = History()
    history.load_events(filename='events.txt')
    # history.save(filename='data.sav')
    # history.load(filename='data.sav')
    for event in history.events_between(date_from=date(2018, 1, 1), date_to=date(2018, 1, 31)):
        print(event.dict)
