from modules.dock_maven.domain.option import OptionContext


class App:

    def __init__(self):
        self.__options = OptionContext()

    def execute(self, args: list):

        option = self.__options.parser().parse(args)
        if option is not None:
            self.__options.runner().run(option)

        # dmvn build pack/age                                       // build maven project with package and parent packages params
        # dmvn build clean pack/age additional...command...list     // clean and build maven project with package and parent packages params and additional arguments from cmd
        # dmvn list pack/age                                        // list package and all subpackages
        # dmvn param list    pack/age                               // list of all set params for package
        # dmvn param inspect pack/age                               // read all params in package print then with theirs location, print unknown and missing params


        # dmvn create packa/age                                     // create package with parent packages
        # dmvn create packa/age -p                                  // create package with parent packages and all missing params to package
        # dmvn remove pack/age                                      // remove package with subpackages
        # dmvn param rm      pack/age pname                         // remove param in package
        # dmvn param set     pack/age pname pvalue                  // set param in package
