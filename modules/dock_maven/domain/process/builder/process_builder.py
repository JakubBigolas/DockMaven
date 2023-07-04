from typing_extensions import Self

from modules.dock_maven.domain.process.data.process_data import ProcessData
from modules.dock_maven.domain.process.instance.process_instance import ProcessInstance


class ProcessBuilder:

    def __init__(self):
        self.__data = ProcessData()



    def build(self) -> ProcessInstance:
        result = ProcessInstance(self.__data)
        self.__data = ProcessData()
        return result



    def from_params(self, params: dict) -> Self:

        self.__data.package                          = self.__from_param(params, "package"                         , self.__data.package                         )
        self.__data.app_name                         = self.__from_param(params, "app-name"                        , self.__data.app_name                        )
        self.__data.src_path                         = self.__from_param(params, "src-path"                        , self.__data.src_path                        )
        self.__data.mvn_image_name                   = self.__from_param(params, "mvn-image-name"                  , self.__data.mvn_image_name                  )
        self.__data.target_path                      = self.__from_param(params, "target-path"                     , self.__data.target_path                     )
        self.__data.mvn_container_env_app_name       = self.__from_param(params, "mvn-container-env-app-name"      , self.__data.mvn_container_env_app_name      )
        self.__data.mvn_container_env_target_dir     = self.__from_param(params, "mvn-container-env-target-dir"    , self.__data.mvn_container_env_target_dir    )
        self.__data.mvn_container_env_build_cmd      = self.__from_param(params, "mvn-container-env-build-cmd"     , self.__data.mvn_container_env_build_cmd     )
        self.__data.mvn_container_env_build_profiles = self.__from_param(params, "mvn-container-env-build-profiles", self.__data.mvn_container_env_build_profiles)
        self.__data.mvn_clean                        = self.__from_param(params, "mvn-clean"                       , self.__data.mvn_clean)

        return self



    def __from_param(self, params: dict, param: str, default):
        return default if param not in params else params[param]
