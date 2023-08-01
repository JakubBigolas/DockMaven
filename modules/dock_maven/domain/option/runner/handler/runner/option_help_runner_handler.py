from modules.dock_maven.domain.package import PackageContext
from .options_runner_handler_abstract import OptionsRunnerHandlerAbstract
from ....data.option_data import OptionData
from ....data.option_help_data import OptionHelpData
from ....data.option_list_data import OptionListData


class OptionHelpRunnerHandler(OptionsRunnerHandlerAbstract):

    def handle(self, option: OptionData):
        print("DockMaven (dmvn) ")
        print("")
        print("DockMaven provides solution for simplify usage maven with docker container \"maven-builder-*\"")
        print("")
        print("Usage: dmvn option package params...")
        print("")
        print("Options:")
        print("  list                  print selected package and subpackages")
        print("  param list            print all params collected for selected package")
        print("  param inspect         print all params collected for selected package")
        print("                        and info about missing required/optional params")
        print("  build                 start mvn container using params for selected package")
        print("  build clean           like build but with additional param --mvn-clean")
        print("")
        print("Params:")
        print("  Parameters are used ondy for build option")
        print("  may be set in config dir in file projects/configs.yaml")
        print("  or in command line after package as KEY VALUE sequence ")
        print("  required:")
        print("    --package'                          pdocker image package")
        print("    --app-name'                         pdocker image name")
        print("    --src-path'                         project scr path")
        print("    --target-path'                      target path for build result")
        print("    --mvn-image-name'                   image name of maven builder")
        print("    --mvn-container-env-target-dir'     target path (subdirectory of src)")
        print("    --mvn-container-env-app-name'       target file name (in src target subdirectory)")
        print("    --mvn-container-env-build-cmd'      maven build command")
        print("  optional:")
        print("    --mvn-clean'                        clean project scr before execution")
        print("    --mvn-container-env-build-profiles' maven profiles")
        print("")
        print("Package:")
        print("  Path to params set in 'options' list in config dir in file projects/configs.yaml")
        print("  For example: client/projects/app indicates that build process should read options from")
        print("  packages client, projects, app in order from parent to last child covering parameters that repeats")



    def accepts(self, option: OptionData) -> bool:
        return isinstance(option, OptionHelpData)

