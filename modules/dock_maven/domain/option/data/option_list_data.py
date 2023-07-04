from .option_data import OptionData


class OptionListData(OptionData):

    def __init__(self, package: str, print_options = False):
        super().__init__(package)
        self.__print_options = print_options

    @property
    def print_options(self):
        return self.__print_options
