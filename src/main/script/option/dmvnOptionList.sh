function dmvnOptionList {

  local project=
  local printFormatted=false

    while [[ $# -gt 0 ]]; do
      case $1 in

        # print in formatted version
        -f) printFormatted=true ; shift ;;

        *)
          [[ -n "$project" ]] && echo "ERROR: too much arguments" && exit 1
          project="$1"
          shift
          ;;

      esac
    done

  # predefine current configuration with default values
  local project_package=
  local project_app_name=
  local project_scr_path=
  local project_mvn_image_name=
  local project_mvn_container_env_APP_NAME=
  local project_mvn_container_env_TARGET_DIR=
  local project_mvn_container_env_BUILD_CMD=
  local project_mvn_container_env_BUILD_PROFILES=

  # prepare full package path to project configuration, starting from "projects/" directory
  local fullPackage="projects/$project"
        fullPackage="${fullPackage/"\\"//}"

  # create array from all available paths between first and last directory in full package path in ascending queue
  local packagesQueue=()
  local lastPackage="${fullPackage/"/"*/}"
  packagesQueue+=("$lastPackage")
  while [[ "$lastPackage" != "$fullPackage" ]] ; do
    local nextPackage="${fullPackage/#"$lastPackage/"/}"
          nextPackage="${nextPackage/"/"*/}"
    lastPackage+="/$nextPackage"
    packagesQueue+=("$lastPackage")
  done

  # for every path in array from all available paths, overwrite configuration variables (applied only for configuration file occurrences)
  for dir in "${packagesQueue[@]}" ; do

    local packageDir="$DMVN_PROJECTS_DIR/$dir"

    local package_package=
    local package_app_name=
    local package_scr_path=
    local package_mvn_image_name=
    local package_mvn_container_env_APP_NAME=
    local package_mvn_container_env_TARGET_DIR=
    local package_mvn_container_env_BUILD_CMD=
    local package_mvn_container_env_BUILD_PROFILES=

    [[ -f "$packageDir/package"                          ]] && package_package="$(head -n 1                           "$packageDir/package"                          )"
    [[ -f "$packageDir/app-name"                         ]] && package_app_name="$(head -n 1                          "$packageDir/app-name"                         )"
    [[ -f "$packageDir/src-path"                         ]] && package_scr_path="$(head -n 1                          "$packageDir/src-path"                         )"
    [[ -f "$packageDir/mvn-image-name"                   ]] && package_mvn_image_name="$(head -n 1                    "$packageDir/mvn-image-name"                   )"
    [[ -f "$packageDir/mvn-container-env-app-name"       ]] && package_mvn_container_env_APP_NAME="$(head -n 1        "$packageDir/mvn-container-env-app-name"       )"
    [[ -f "$packageDir/mvn-container-env-target-dir"     ]] && package_mvn_container_env_TARGET_DIR="$(head -n 1      "$packageDir/mvn-container-env-target-dir"     )"
    [[ -f "$packageDir/mvn-container-env-build-cmd"      ]] && package_mvn_container_env_BUILD_CMD="$(head -n 1       "$packageDir/mvn-container-env-build-cmd"      )"
    [[ -f "$packageDir/mvn-container-env-build-profiles" ]] && package_mvn_container_env_BUILD_PROFILES="$(head -n 1  "$packageDir/mvn-container-env-build-profiles" )"

    if [[ $printFormatted = true ]] ; then
      echo "$packageDir"
      [[ -f "$packageDir/package"                          ]] && printf "${C_YELLOW}package${C_WHITE}=${C_RESET}"                          && echo "$package_package"
      [[ -f "$packageDir/app-name"                         ]] && printf "${C_YELLOW}app-name${C_WHITE}=${C_RESET}"                         && echo "$package_app_name"
      [[ -f "$packageDir/src-path"                         ]] && printf "${C_YELLOW}src-path${C_WHITE}=${C_RESET}"                         && echo "$package_scr_path"
      [[ -f "$packageDir/mvn-image-name"                   ]] && printf "${C_YELLOW}mvn-image-name${C_WHITE}=${C_RESET}"                   && echo "$package_mvn_image_name"
      [[ -f "$packageDir/mvn-container-env-app-name"       ]] && printf "${C_YELLOW}mvn-container-env-app-name${C_WHITE}=${C_RESET}"       && echo "$package_mvn_container_env_APP_NAME"
      [[ -f "$packageDir/mvn-container-env-target-dir"     ]] && printf "${C_YELLOW}mvn-container-env-target-dir${C_WHITE}=${C_RESET}"     && echo "$package_mvn_container_env_TARGET_DIR"
      [[ -f "$packageDir/mvn-container-env-build-cmd"      ]] && printf "${C_YELLOW}mvn-container-env-build-cmd${C_WHITE}=${C_RESET}"      && echo "$package_mvn_container_env_BUILD_CMD"
      [[ -f "$packageDir/mvn-container-env-build-profiles" ]] && printf "${C_YELLOW}mvn-container-env-build-profiles${C_WHITE}=${C_RESET}" && echo "$package_mvn_container_env_BUILD_PROFILES"
      echo
    fi

    [[ -f "$packageDir/package"                          ]] && project_package="$package_package"
    [[ -f "$packageDir/app-name"                         ]] && project_app_name="$package_app_name"
    [[ -f "$packageDir/src-path"                         ]] && project_scr_path="$package_scr_path"
    [[ -f "$packageDir/mvn-image-name"                   ]] && project_mvn_image_name="$package_mvn_image_name"
    [[ -f "$packageDir/mvn-container-env-app-name"       ]] && project_mvn_container_env_APP_NAME="$package_mvn_container_env_APP_NAME"
    [[ -f "$packageDir/mvn-container-env-target-dir"     ]] && project_mvn_container_env_TARGET_DIR="$package_mvn_container_env_TARGET_DIR"
    [[ -f "$packageDir/mvn-container-env-build-cmd"      ]] && project_mvn_container_env_BUILD_CMD="$package_mvn_container_env_BUILD_CMD"
    [[ -f "$packageDir/mvn-container-env-build-profiles" ]] && project_mvn_container_env_BUILD_PROFILES="$package_mvn_container_env_BUILD_PROFILES"

  done

  [[ $printFormatted = true ]] && echo "Final result: "

  # run maven process using project, sub projects and default parametrization
  [[ -n "$project_package"                          ]] && echo "--package"                          && eval echo "$project_package"
  [[ -n "$project_app_name"                         ]] && echo "--app-name"                         && eval echo "$project_app_name"
  [[ -n "$project_scr_path"                         ]] && echo "--src-path"                         && eval echo "$project_scr_path"
  [[ -n "$project_mvn_image_name"                   ]] && echo "--mvn-image-name"                   && eval echo "$project_mvn_image_name"
  [[ -n "$project_mvn_container_env_APP_NAME"       ]] && echo "--mvn-container-env-app-name"       && eval echo "$project_mvn_container_env_APP_NAME"
  [[ -n "$project_mvn_container_env_TARGET_DIR"     ]] && echo "--mvn-container-env-target-dir"     && eval echo "$project_mvn_container_env_TARGET_DIR"
  [[ -n "$project_mvn_container_env_BUILD_CMD"      ]] && echo "--mvn-container-env-build-cmd"      && eval echo "$project_mvn_container_env_BUILD_CMD"
  [[ -n "$project_mvn_container_env_BUILD_PROFILES" ]] && echo "--mvn-container-env-build-profiles" && eval echo "$project_mvn_container_env_BUILD_PROFILES"


}