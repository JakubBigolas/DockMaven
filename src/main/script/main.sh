function main {

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
      --package                         ) default_package="$2"                          ; shift ; shift ;;
      --app-name                        ) default_app_name="$2"                         ; shift ; shift ;;
      --src-path                        ) default_scr_path="$2"                         ; shift ; shift ;;
      --mvn-image-name                  ) default_mvn_image_name="$2"                   ; shift ; shift ;;
      --mvn-container-env-app-name      ) default_mvn_container_env_APP_NAME="$2"       ; shift ; shift ;;
      --mvn-container-env-target-dir    ) default_mvn_container_env_TARGET_DIR="$2"     ; shift ; shift ;;
      --mvn-container-env-build-cmd     ) default_mvn_container_env_BUILD_CMD="$2"      ; shift ; shift ;;
      --mvn-container-env-build-profiles) default_mvn_container_env_BUILD_PROFILES="$2" ; shift ; shift ;;
      --mvn-clean                       ) default_mvn_clean="--mvn-clean"               ; shift         ;;
      --project                         ) selectedProjects+=("$2")                      ; shift ; shift ;;
      "") shift ;;
      *) echo "Unknown option $1" ; exit 1 ;;
    esac
  done

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

  else
    local project=
    for project in "${selectedProjects[@]}" ; do

      local project_package="$default_package"
      local project_app_name="$default_app_name"
      local project_scr_path="$default_scr_path"
      local project_mvn_image_name="$default_mvn_image_name"
      local project_mvn_container_env_APP_NAME="$default_mvn_container_env_APP_NAME"
      local project_mvn_container_env_TARGET_DIR="$default_mvn_container_env_TARGET_DIR"
      local project_mvn_container_env_BUILD_CMD="$default_mvn_container_env_BUILD_CMD"
      local project_mvn_container_env_BUILD_PROFILES="$default_mvn_container_env_BUILD_PROFILES"

      local packagesQueue=()
      local fullPackage="projects/$project"
            fullPackage="${fullPackage/"\\"//}"
      local lastPackage="${fullPackage/"/"*/}"

      packagesQueue+=("$lastPackage")
      while [[ "$lastPackage" != "$fullPackage" ]] ; do
        local nextPackage="${fullPackage/#"$lastPackage/"/}"
              nextPackage="${nextPackage/"/"*/}"
        lastPackage+="/$nextPackage"
        packagesQueue+=("$lastPackage")
      done

      for dir in "${packagesQueue[@]}" ; do

        local packageDir="$DMVN_PROJECTS_DIR/$dir"

        [[ -f "$packageDir/package"                          ]] && project_package="$(head -n 1                           "$packageDir/package"                          )"
        [[ -f "$packageDir/app-name"                         ]] && project_app_name="$(head -n 1                          "$packageDir/app-name"                         )"
        [[ -f "$packageDir/src-path"                         ]] && project_scr_path="$(head -n 1                          "$packageDir/src-path"                         )"
        [[ -f "$packageDir/mvn-image-name"                   ]] && project_mvn_image_name="$(head -n 1                    "$packageDir/mvn-image-name"                   )"
        [[ -f "$packageDir/mvn-container-env-app-name"       ]] && project_mvn_container_env_APP_NAME="$(head -n 1        "$packageDir/mvn-container-env-app-name"       )"
        [[ -f "$packageDir/mvn-container-env-target-dir"     ]] && project_mvn_container_env_TARGET_DIR="$(head -n 1      "$packageDir/mvn-container-env-target-dir"     )"
        [[ -f "$packageDir/mvn-container-env-build-cmd"      ]] && project_mvn_container_env_BUILD_CMD="$(head -n 1       "$packageDir/mvn-container-env-build-cmd"      )"
        [[ -f "$packageDir/mvn-container-env-build-profiles" ]] && project_mvn_container_env_BUILD_PROFILES="$(head -n 1  "$packageDir/mvn-container-env-build-profiles" )"

      done

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
