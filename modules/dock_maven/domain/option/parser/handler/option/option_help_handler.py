from ....data.option_data import OptionData
from .option_handler_abstract import OptionHandlerAbstract
from ....data.option_help_data import OptionHelpData


class OptionHelpHandler(OptionHandlerAbstract):



    def handle(self, args: list) -> OptionData:
        return OptionHelpData(None)



    def accepts(self, args: list) -> bool:
        return len(args) == 1 and args[0] in ("help", "--help", "-?")
