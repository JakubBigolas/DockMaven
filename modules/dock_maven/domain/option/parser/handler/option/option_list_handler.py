from ....data.option_data import OptionData
from modules.dock_maven.error import DmvnError
from .option_handler_abstract import OptionHandlerAbstract
from ....data.option_list_data import OptionListData

class OptionListHandler(OptionHandlerAbstract):



    def handle(self, args: list) -> OptionData:
        args.pop(0) # omit option arg

        package = None
        print_options   = False
        print_buildable = False

        while len(args) > 0:
            arg = args.pop(0)

            if arg == "-o":
                print_options = True
            elif arg == "-b":
                print_buildable = True
            elif package is None:
                package = arg
            else:
                raise DmvnError("Too much arguments for list option")

        return OptionListData(package, print_options, print_buildable)


    def accepts(self, args: list) -> bool:
        return len(args) > 0 and args[0] == "list"
