from .handler.options_runner_resolver import OptionsRunnerResolver
from ..data.option_data import OptionData


class OptionRunner:

    def __init__(self):
        self.__resolver = OptionsRunnerResolver()


    def run(self, option: OptionData):
        self.__resolver.resolve(option).handle(option)