from modules.dock_maven.domain.package import PackageContext
from modules.dock_maven.domain.process import ProcessContext
from modules.dock_maven.error import DmvnError
from .options_runner_handler_abstract import OptionsRunnerHandlerAbstract
from ....data.option_build_data import OptionBuildData
from ....data.option_data import OptionData

class OptionBuildRunnerHandler(OptionsRunnerHandlerAbstract):



    def handle(self, option: OptionData):
        option: OptionBuildData = option
        packages = PackageContext()

        print("Start maven build process for package: {}".format(option.package))
        print()

        params = packages.read_params(option.package)

        if len(option.params) > 0:
            for cmd_param in option.params:
                params[cmd_param] = option.params[cmd_param]

        missing = packages.check_missing_params(params)

        if len(missing["optional"]) > 0:
            print("There are still optional parameters that might be used:")
            for miss in missing["optional"]:
                print("  {}".format(miss))
            print()

        if len(missing["required"]) > 0:
            error = "ERROR: missing required parameters:\n"
            for miss in missing["required"]:
                error += "  " + miss + ",\n"
            raise DmvnError(error[:-2])

        processes = ProcessContext()
        process = processes.builder().from_params(params).build()
        process.execute()




    def accepts(self, option: OptionData) -> bool:
        return isinstance(option, OptionBuildData)

