from modules.dock_maven.domain.package import PackageContext
from .options_runner_handler_abstract import OptionsRunnerHandlerAbstract
from ....data.option_data import OptionData
from ....data.option_list_data import OptionListData


class OptionListRunnerHandler(OptionsRunnerHandlerAbstract):

    def handle(self, option: OptionData):
        option: OptionListData = option
        packages = PackageContext()
        configs = packages.read_configs(option.package)
        self.print_package(packages, configs, packages.split_package(option.package), option.print_options)



    def print_package(self, packages: PackageContext, configs: dict, package: list, print_options: bool):
        print(packages.list_to_package(package))
        self.print_options(configs, print_options)
        self.print_sub_package(packages, configs, package, print_options)



    def print_options(self, configs: dict, print_options: bool):
        if print_options:
            if "options" in configs:
                options = configs["options"]
                if options:
                    for option in options:
                        for it in option:
                            print(" - {} : {}".format(it, option[it]))



    def print_sub_package(self, packages: PackageContext, configs: dict, package: list, print_options: bool):
        for config in configs:
            if config != "options":
                sub_package = list(package)
                sub_package.append(config)
                self.print_package(packages, configs[config], sub_package, print_options)



    def accepts(self, option: OptionData) -> bool:
        return isinstance(option, OptionListData)

