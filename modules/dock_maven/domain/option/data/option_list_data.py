from .option_data import OptionData


class OptionListData(OptionData):

    def __init__(self, package: str, print_options = False, print_buildable = False):
        super().__init__(package)
        self.__print_options   = print_options
        self.__print_buildable = print_buildable

    @property
    def print_options(self):
        return self.__print_options

    @property
    def print_buildable(self):
        return self.__print_buildable