from .option_data import OptionData


class OptionParamData(OptionData):

    def __init__(self, package: str, inspect = False, list = False):
        super().__init__(package)
        self.__list = list
        self.__inspect = inspect

    @property
    def list(self):
        return self.__list

    @property
    def inspect(self):
        return self.__inspect
