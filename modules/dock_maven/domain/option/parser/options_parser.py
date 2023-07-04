from ..data.option_data import OptionData
from .handler.options_resolver import OptionsResolver

class OptionsParser:

    def __init__(self):
        self.__resolver = OptionsResolver()


    def parse(self, args: list) -> OptionData:
        return self.__resolver.resolve(args).handle(args)
