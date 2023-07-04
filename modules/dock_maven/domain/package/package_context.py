import yaml

from modules.dock_maven.domain.app_context import AppContext


class PackageContext:



    def split_package(self, package) -> list:
        package = self.normalize_package(package)
        items = package.split("/")
        return [it for it in items if len(it) > 0]



    def list_to_package(self, package: list) -> str:
        package_name = ""
        for item in package:
            package_name += item + "/"
        if len(package_name) > 0:
            package_name = package_name[:-1]
        return package_name



    def normalize_package(self, package: str) -> str:
        package = "" if package is None else package
        package = package.replace("\\", "/")
        package = package.replace("//", "/")
        package = package.strip()
        return package



    def read_configs(self, package: str = None):
        app_context = AppContext.context()
        configs_str: str = app_context.read_configs()
        configs: dict = yaml.safe_load(configs_str)["root"]

        if package:
            root = self.split_package(package)
            if len(root) > 0:
                while len(root) > 0:
                    item = root.pop(0)

                    if item in configs:
                        configs = configs[item]
                    else:
                        configs = dict()
                        break

        return configs



    def read_params(self, package: str) -> dict:
        root = self.split_package(package)
        configs = self.read_configs()
        result = dict()

        self.__read_options(configs, result)

        while len(root) > 0:
            node = root.pop(0)

            if node in configs:
                configs = configs[node]
            else:
                return dict()

            self.__read_options(configs, result)

        return result



    def read_options(self, configs: dict) -> dict:
        result = dict()
        self.__read_options(configs, result)
        return result



    def __read_options(self, configs: dict, out: dict):
        if "options" in configs:
            options = configs["options"]
            if options:
                for option in options:
                    for it in option:
                        out[it] = option[it]



    def check_missing_params(self, params: dict):
        result = dict()
        result["required"] = list()
        result["optional"] = list()

        params_names = self.param_names()

        for it in params_names["required"]:
            if it not in params or params[it] is None or len(params[it].strip()) < 1:
                result["required"].append(it)

        for it in params_names["optional"]:
            if it not in params or params[it] is None or len(params[it].strip()) < 1:
                result["optional"].append(it)

        return result



    def param_names(self) -> dict:
        return {
            "required": [
                "package",
                "app-name",
                "src-path",
                "mvn-image-name",
                "target-path",
                "mvn-container-env-app-name",
                "mvn-container-env-target-dir",
                "mvn-container-env-build-cmd",
            ],
            "optional": [
                "mvn-container-env-build-profiles",
                "mvn-clean"
            ]
        }
