from modules.dock_maven.domain.app_context import AppContext
from ....data.option_data import OptionData

class OptionsRunnerHandlerAbstract:

    def __init__(self):
        self.__app_context = AppContext.context()

    @property
    def app_context(self):
        return self.__app_context

    def handle(self, option: OptionData):
        raise NotImplementedError

    def accepts(self, option: OptionData) -> bool:
        raise NotImplementedError

