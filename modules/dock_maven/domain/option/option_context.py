from .parser.options_parser import OptionsParser
from .runner.option_runner import OptionRunner


class OptionContext:

    def parser(self) -> OptionsParser:
        return OptionsParser()

    def runner(self) -> OptionRunner:
        return OptionRunner()
