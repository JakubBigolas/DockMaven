function dmvnHelp {

  echo -e "DockMaven (dmvn) "
  echo -e ""
  echo -e "DockMaven provides solution for simplify usage maven with docker container \"maven-builder-*\""
  echo -e ""
  echo -e "Usage: dmvn [arguments...]|[list]"
  echo -e ""
  echo -e "Options:"
  toolHelpOptionPrint 'list *'                             'prints configuration from selected package,'                              20
  toolHelpOptionPrint ''                                   'to print every package separated use additional argument -f '            20
  echo -e ""
  echo -e "Arguments:"
  toolHelpOptionPrint '--help|help|-?'                     'print help info and exit'                                                20
  toolHelpOptionPrint '--version|version|-v'               'print version info and exit'                                             20
  toolHelpOptionPrint '--mvn-projects-dir'                 'print maven project configuration path variable and exit'                20
  toolHelpOptionPrint '--project'                          'select maven project configuration path'                                 20
  toolHelpOptionPrint ''                                   'notice that configuration will not be applied only for selected package' 20
  toolHelpOptionPrint ''                                   'but every package starting from "projects/" directory to selected path'  20
  toolHelpOptionPrint '--mvn-clean'                        'clean project scr before execution'                                      20
  toolHelpOptionPrint '--package'                          'pdocker image package'                                                   20
  toolHelpOptionPrint '--app-name'                         'pdocker image name'                                                      20
  toolHelpOptionPrint '--src-path'                         'project scr path'                                                        20
  toolHelpOptionPrint '--mvn-image-name'                   'image name of maven builder'                                             20
  toolHelpOptionPrint '--mvn-container-env-app-name'       'target file name (in target directory)'                                  40
  toolHelpOptionPrint '--mvn-container-env-target-dir'     'target path (subdirectory of src)'                                       40
  toolHelpOptionPrint '--mvn-container-env-build-cmd'      'maven build command'                                                     40
  toolHelpOptionPrint '--mvn-container-env-build-profiles' 'maven profiles'                                                          40
  echo -e ""

}