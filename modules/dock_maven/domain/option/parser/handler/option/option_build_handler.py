from modules.dock_maven.domain.package import PackageContext
from modules.dock_maven.error import DmvnError
from ....data.option_build_data import OptionBuildData
from ....data.option_data import OptionData
from .option_handler_abstract import OptionHandlerAbstract

class OptionBuildHandler(OptionHandlerAbstract):



    def handle(self, args: list) -> OptionData:
        args.pop(0) # omit option arg
        packages = PackageContext()
        param_names = packages.param_names()

        package = None
        params = dict()

        if len(args) > 0:
            arg = args.pop(0)

            if arg == "clean":
                params["mvn-clean"] = "true"
            else:
                args.insert(0, arg)

            while len(args) > 0:
                arg: str = args.pop(0)

                # set package first
                if package is None:
                    package = arg

                # then
                else:
                    param = arg
                    if param.startswith("--"):
                        param = param[2:]

                    if param in param_names["required"] or param in param_names["optional"]:
                        params[param] = None if len(args) < 1 else args.pop(0)
                    else:
                        raise DmvnError("Unknown param {}".format(param))

        return OptionBuildData(package, params)


    def accepts(self, args: list) -> bool:
        return len(args) > 0 and args[0] == "build"
