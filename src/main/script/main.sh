function main {

  # default process parametrization variables
  local default_package=
  local default_app_name=
  local default_scr_path=
  local default_mvn_clean=
  local default_mvn_image_name=
  local default_mvn_container_env_APP_NAME=
  local default_mvn_container_env_TARGET_DIR=
  local default_mvn_container_env_BUILD_CMD=
  local default_mvn_container_env_BUILD_PROFILES=

  local selectedProjects=()

  while [[ $# -gt 0 ]]; do
    case $1 in

      # print help info and exit
      --help|help|"-?"                  ) dmvnHelp ; exit 0 ;;

      # print version info and exit
      --version|-v|version              ) echo "1.0.1" ; exit 0 ;;

      # print maven projects configuration directory path and exit
      --mvn-projects-dir                ) echo "$DMVN_PROJECTS_DIR" ; exit 0 ;;

      # print configuration from selected path
      list) shift ; dmvnOptionList "$@" ; exit 0 ;;

      # maven builder process parametrization
      --package                         ) default_package="$2"                          ; shift ; shift ;;
      --app-name                        ) default_app_name="$2"                         ; shift ; shift ;;
      --src-path                        ) default_scr_path="$2"                         ; shift ; shift ;;
      --mvn-image-name                  ) default_mvn_image_name="$2"                   ; shift ; shift ;;
      --mvn-container-env-app-name      ) default_mvn_container_env_APP_NAME="$2"       ; shift ; shift ;;
      --mvn-container-env-target-dir    ) default_mvn_container_env_TARGET_DIR="$2"     ; shift ; shift ;;
      --mvn-container-env-build-cmd     ) default_mvn_container_env_BUILD_CMD="$2"      ; shift ; shift ;;
      --mvn-container-env-build-profiles) default_mvn_container_env_BUILD_PROFILES="$2" ; shift ; shift ;;
      --mvn-clean                       ) default_mvn_clean="--mvn-clean"               ; shift         ;;

      # maven configuration project selection
      --project                         )
        if [[ "$2" =~ \* ]] ; then
          local projectsDir="${DMVN_PROJECTS_DIR//\\//}/projects"
          local subProjects=$(eval echo "$projectsDir/$2")
          subProjects=${subProjects//" $projectsDir/"/$'\n'}
          subProjects=${subProjects/#"$projectsDir/"/}
          readarray -t subProjects < <(echo "$subProjects")
          for subProject in "${subProjects[@]}" ; do
            [[ -d "$projectsDir/$subProject" ]] && selectedProjects+=("$subProject")
          done
        else
          selectedProjects+=("$2")
        fi

        shift ; shift ;;

      # ommit empty args
      "") shift ;;

      # Error unknown arg
      *) echo "Unknown option $1" ; exit 1 ;;

    esac
  done

  # if there is no project selected run maven process using parametrization from command args
  if [[ "${#selectedProjects[@]}" = 0 ]] ; then

    process                                                                        \
    --package                          "$default_package"                          \
    --app-name                         "$default_app_name"                         \
    --src-path                         "$default_scr_path"                         \
    --mvn-image-name                   "$default_mvn_image_name"                   \
    --mvn-container-env-app-name       "$default_mvn_container_env_APP_NAME"       \
    --mvn-container-env-target-dir     "$default_mvn_container_env_TARGET_DIR"     \
    --mvn-container-env-build-cmd      "$default_mvn_container_env_BUILD_CMD"      \
    --mvn-container-env-build-profiles "$default_mvn_container_env_BUILD_PROFILES" \
    $default_mvn_clean

  # if there is any configuration project selected then for each:
  else

    echo "@@@ dmvn build queue: "
    local project=
    for project in "${selectedProjects[@]}" ; do
      echo " - $project"
    done

    local project=
    for project in "${selectedProjects[@]}" ; do

      # predefine current configuration with default values
      local project_package="$default_package"
      local project_app_name="$default_app_name"
      local project_scr_path="$default_scr_path"
      local project_mvn_image_name="$default_mvn_image_name"
      local project_mvn_container_env_APP_NAME="$default_mvn_container_env_APP_NAME"
      local project_mvn_container_env_TARGET_DIR="$default_mvn_container_env_TARGET_DIR"
      local project_mvn_container_env_BUILD_CMD="$default_mvn_container_env_BUILD_CMD"
      local project_mvn_container_env_BUILD_PROFILES="$default_mvn_container_env_BUILD_PROFILES"

      # override default values with project values
      local configFromProject=()
      readarray -t configFromProject < <(   dmvnOptionList "$project"   )
      local index=0
      while [[ $index -lt ${#configFromProject[@]} ]] ; do

        item="${configFromProject[index]}"
        value="${configFromProject[index + 1]}"
        case $item in
          --package)                          project_package="$value"                          && index=$((index + 1)) ;;
          --app-name)                         project_app_name="$value"                         && index=$((index + 1)) ;;
          --src-path)                         project_scr_path="$value"                         && index=$((index + 1)) ;;
          --mvn-image-name)                   project_mvn_image_name="$value"                   && index=$((index + 1)) ;;
          --mvn-container-env-app-name)       project_mvn_container_env_APP_NAME="$value"       && index=$((index + 1)) ;;
          --mvn-container-env-target-dir)     project_mvn_container_env_TARGET_DIR="$value"     && index=$((index + 1)) ;;
          --mvn-container-env-build-cmd)      project_mvn_container_env_BUILD_CMD="$value"      && index=$((index + 1)) ;;
          --mvn-container-env-build-profiles) project_mvn_container_env_BUILD_PROFILES="$value" && index=$((index + 1)) ;;
        esac
        index=$((index + 1))

      done

      # run maven process using project, sub projects and default parametrization
      process                                                                        \
      --package                          "$project_package"                          \
      --app-name                         "$project_app_name"                         \
      --src-path                         "$project_scr_path"                         \
      --mvn-image-name                   "$project_mvn_image_name"                   \
      --mvn-container-env-app-name       "$project_mvn_container_env_APP_NAME"       \
      --mvn-container-env-target-dir     "$project_mvn_container_env_TARGET_DIR"     \
      --mvn-container-env-build-cmd      "$project_mvn_container_env_BUILD_CMD"      \
      --mvn-container-env-build-profiles "$project_mvn_container_env_BUILD_PROFILES" \
      $default_mvn_clean

    done
  fi

}
