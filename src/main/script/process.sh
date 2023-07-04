function process {
  local start_script="$(date +%s)"

  local package=
  local app_name=
  local scr_path=
  local mvn_clean=false
  local mvn_image_name=

  local mvn_container_env_APP_NAME=
  local mvn_container_env_TARGET_DIR=
  local mvn_container_env_BUILD_CMD=
  local mvn_container_env_BUILD_PROFILES=

  while [[ $# -gt 0 ]]; do
    case $1 in
      --package                         ) package="$2"                          ; shift ; shift ;;
      --app-name                        ) app_name="$2"                         ; shift ; shift ;;
      --src-path                        ) scr_path="$2"                         ; shift ; shift ;;
      --mvn-image-name                  ) mvn_image_name="$2"                   ; shift ; shift ;;
      --mvn-container-env-app-name      ) mvn_container_env_APP_NAME="$2"       ; shift ; shift ;;
      --mvn-container-env-target-dir    ) mvn_container_env_TARGET_DIR="$2"     ; shift ; shift ;;
      --mvn-container-env-build-cmd     ) mvn_container_env_BUILD_CMD="$2"      ; shift ; shift ;;
      --mvn-container-env-build-profiles) mvn_container_env_BUILD_PROFILES="$2" ; shift ; shift ;;
      --mvn-clean                       ) mvn_clean=true                        ; shift         ;;
      *) echo "Unknown option $1" ; exit 1 ;;
    esac
  done

  [[ -z "$package"  ]] && echo "package is required option" && exit 1
  [[ -z "$app_name" ]] && echo "app_name is required option" && exit 1
  [[ -z "$scr_path" ]] && echo "scr_path is required option" && exit 1

  dockerfile_path="$(pdocker image list -p -N --image "$package-$app_name" --package "$package/$app_name")"
  [[ ! -d "$dockerfile_path" ]] && echo "There is no docker image directory in path $dockerfile_path/Dockerfile" && exit 1

  local target_path="$dockerfile_path/target"
  local pom_path="$scr_path/pom.xml"
  local mvn_container_name="mvn-builder-$app_name"

  echo "@@@ build docker image with env"
  echo " - package                          =$package"
  echo " - app-name                         =$app_name"
  echo " - scr-path                         =$scr_path"
  echo " - mvn-image-name                   =$mvn_image_name"
  echo " - mvn_container_name               =$mvn_container_name"
  echo " - mvn_container_env_app-name       =$mvn_container_env_APP_NAME"
  echo " - mvn_container_env_target-dir     =$mvn_container_env_TARGET_DIR"
  echo " - mvn_container_env_build-cmd      =$mvn_container_env_BUILD_CMD"
  echo " - mvn_container_env_build-profiles =$mvn_container_env_BUILD_PROFILES"
  echo " - mvn-clean                        =$mvn_clean"
  echo " - dockerfile_path                  =$dockerfile_path"
  echo " - target_path                      =$target_path"
  echo " - pom_path                         =$pom_path"

  echo "@@@ recreate target dir $target_path"
  rm -r $target_path
  mkdir $target_path

  if [[ $mvn_clean = true ]] ; then
    echo "@@@ cleaning workspace $scr_path"
    mvn clean -f "$pom_path"
  fi

  local failCheck=false
  echo "@@@ starting builder container $mvn_container_name"
  docker kill "$mvn_container_name"
  docker rm   "$mvn_container_name"
  docker run  --rm \
    -e       APP_NAME="$mvn_container_env_APP_NAME"               \
    -e     TARGET_DIR="$mvn_container_env_TARGET_DIR"             \
    -e      BUILD_CMD="$mvn_container_env_BUILD_CMD"              \
    -e BUILD_PROFILES="$mvn_container_env_BUILD_PROFILES"         \
    -v     "$scr_path:/usr/src/external/$app_name"                \
    -v "$mvn_container_name:/usr/src/mymaven/$app_name"           \
    -v "$target_path":/builds                                     \
    -v        m2cache:/root/.m2                                   \
    --name "$mvn_container_name" $mvn_image_name || failCheck=true

  local end_script=`date +%s`;
  local diff=`expr $end_script - $start_script`;
  local hrs=`expr $diff / 360`;
  local min=`expr $diff / 60`;
  local sec=`expr $diff % 60`;
  echo build $image_name time: `printf %02d $hrs`:`printf %02d $min`:`printf %02d $sec`

  [[ $failCheck = true ]] && exit 1
  exit 0

}