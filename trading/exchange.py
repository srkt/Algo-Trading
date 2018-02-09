from abc import abstractmethod


class Exchange(object):
    name = None

    def __init__(self, name):
        self.name = name

    @abstractmethod
    def get_data(self, ticker, from_date, end_date):
        pass
