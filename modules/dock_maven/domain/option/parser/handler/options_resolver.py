from copy import deepcopy

from modules.dock_maven.error import DmvnError
from .option.option_handler_abstract import OptionHandlerAbstract
from .option.option_build_handler import OptionBuildHandler
from .option.option_list_handler import OptionListHandler
from .option.option_param_handler import OptionParamHandler

class OptionsResolver:

    def __init__(self):
        self.__handlers: list = [
            OptionBuildHandler(),
            OptionListHandler(),
            OptionParamHandler(),
        ]


    def resolve(self, args: list) -> OptionHandlerAbstract:
        args = deepcopy(args)
        result = [handler for handler in self.__handlers if handler.accepts(args)]
        if len(result) == 1:
            return result[0]
        else:
            raise DmvnError("Cannot resolve arguments {}".format(args))