from modules.dock_maven.error import DmvnError
from ....data.option_data import OptionData
from .option_handler_abstract import OptionHandlerAbstract
from ....data.option_param_data import OptionParamData


class OptionParamHandler(OptionHandlerAbstract):



    def handle(self, args: list) -> OptionData:
        args.pop(0) # omit option arg

        package = None
        list = False
        inspect = False

        if len(args) > 0:
            arg = args.pop(0)

            if arg == "list":
                list = True
            elif arg == "inspect":
                inspect = True
            else:
                raise DmvnError(f"Option {arg} unknown")

            while len(args) > 0:
                arg = args.pop(0)

                if package is None:
                    package = arg
                else:
                    raise DmvnError("Too much arguments for list option")

        return OptionParamData(package, inspect, list)



    def accepts(self, args: list) -> bool:
        return len(args) > 0 and args[0] == "param"
