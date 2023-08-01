from modules.dock_maven.domain.app_context import AppContext
from modules.dock_maven.domain.option import OptionContext


class App:

    def __init__(self):
        self.__options = OptionContext()

    def execute(self, args: list):

        AppContext.context().ensure_configs_exists()

        option = self.__options.parser().parse(args)

        if option is not None:
            self.__options.runner().run(option)
