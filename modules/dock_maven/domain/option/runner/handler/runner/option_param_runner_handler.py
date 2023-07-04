from modules.dock_maven.domain.package import PackageContext
from .options_runner_handler_abstract import OptionsRunnerHandlerAbstract
from ....data.option_data import OptionData
from ....data.option_param_data import OptionParamData


class OptionParamRunnerHandler(OptionsRunnerHandlerAbstract):

    def handle(self, option: OptionData):
        self.list(option)
        self.inspect(option)



    def list(self, option: OptionParamData):
        if option and option.list:
            packages = PackageContext()
            params = packages.read_params(option.package)
            for param in params:
                print("{}={}".format(param, params[param]))



    def inspect(self, option: OptionParamData):
        if option and option.inspect:
            packages = PackageContext()
            root = packages.split_package(option.package)
            configs = packages.read_configs()
            result = list()

            result.extend(self.options_inspection(packages, configs, "[root]"))

            while len(root) > 0:
                node = root.pop(0)

                if node in configs:
                    configs = configs[node]
                else:
                    return

                result.extend(self.options_inspection(packages, configs, node))

            for line in result:
                print(line)

            missing = packages.check_missing_params(packages.read_params(option.package))

            if len(missing["required"]) > 0:
                print("Missing required parameters")
                for it in missing["required"]:
                    print("  {}".format(it))
                print("")

            if len(missing["optional"]) > 0:
                print("Missing optional parameters")
                for it in missing["optional"]:
                    print("  {}".format(it))
                print("")



    def options_inspection(self, packages: PackageContext, configs: dict, node: str):
        result = list()
        result.append("package: {}".format(node))
        options = packages.read_options(configs)
        for it in options:
            result.append("  {}={}".format(it, options[it]))
        result.append("")
        return result



    def accepts(self, option: OptionData) -> bool:
        return isinstance(option, OptionParamData)

