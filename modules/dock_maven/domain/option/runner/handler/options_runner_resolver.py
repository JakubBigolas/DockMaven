from copy import deepcopy

from modules.dock_maven.error import DmvnError
from .runner.option_help_runner_handler import OptionHelpRunnerHandler
from .runner.options_runner_handler_abstract import OptionsRunnerHandlerAbstract
from ...data.option_data import OptionData

from .runner.option_build_runner_handler import OptionBuildRunnerHandler
from .runner.option_list_runner_handler import OptionListRunnerHandler
from .runner.option_param_runner_handler import OptionParamRunnerHandler


class OptionsRunnerResolver:

    def __init__(self):
        self.__handlers: list = [
            OptionBuildRunnerHandler(),
            OptionListRunnerHandler(),
            OptionParamRunnerHandler(),
            OptionHelpRunnerHandler()
        ]

    def resolve(self, option: OptionData) -> OptionsRunnerHandlerAbstract:
        option = deepcopy(option)
        result = [handler for handler in self.__handlers if handler.accepts(option)]
        if len(result) == 1:
            return result[0]
        else:
            raise DmvnError("Cannot resolve option {}".format(option))