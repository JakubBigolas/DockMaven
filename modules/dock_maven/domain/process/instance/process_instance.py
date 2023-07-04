import os
import subprocess
import time
from datetime import timedelta
from sys import stdout

from modules.dock_maven.error import DmvnError
from ..data.process_data import ProcessData
from ...app_context import AppContext


class ProcessInstance:

    def __init__(self, data: ProcessData):
        self.__data = data
        self.__app_context = AppContext.context()



    def execute(self):
        start_at = time.time()

        package                          = self.__evaluate(self.__data.package)
        app_name                         = self.__evaluate(self.__data.app_name)
        src_path                         = self.__evaluate(self.__data.src_path)
        mvn_image_name                   = self.__evaluate(self.__data.mvn_image_name)
        target_path                      = self.__evaluate(self.__data.target_path)
        mvn_container_env_app_name       = self.__evaluate(self.__data.mvn_container_env_app_name)
        mvn_container_env_target_dir     = self.__evaluate(self.__data.mvn_container_env_target_dir)
        mvn_container_env_build_cmd      = self.__evaluate(self.__data.mvn_container_env_build_cmd)
        mvn_container_env_build_profiles = self.__evaluate(self.__data.mvn_container_env_build_profiles)
        mvn_clean                        = self.__evaluate(self.__data.mvn_clean)

        print("Context params:")
        print(" - package                          ={}  ({})".format(package, self.__data.package))
        print(" - app_name                         ={}  ({})".format(app_name, self.__data.app_name))
        print(" - src_path                         ={}  ({})".format(src_path, self.__data.src_path))
        print(" - mvn_image_name                   ={}  ({})".format(mvn_image_name, self.__data.mvn_image_name))
        print(" - target_path                      ={}  ({})".format(target_path, self.__data.target_path))
        print(" - mvn_container_env_app_name       ={}  ({})".format(mvn_container_env_app_name, self.__data.mvn_container_env_app_name))
        print(" - mvn_container_env_target_dir     ={}  ({})".format(mvn_container_env_target_dir, self.__data.mvn_container_env_target_dir))
        print(" - mvn_container_env_build_cmd      ={}  ({})".format(mvn_container_env_build_cmd, self.__data.mvn_container_env_build_cmd))
        print(" - mvn_container_env_build_profiles ={}  ({})".format(mvn_container_env_build_profiles, self.__data.mvn_container_env_build_profiles))
        print(" - mvn_clean                        ={}".format(mvn_clean))
        print()

        target_dir = target_path + "/target"
        print("Recreate target dir {}".format(target_dir))
        self.__app_context.recreate_dir(target_dir)
        print()

        pom_path = f"{src_path}/pom.xml"
        print(f"Clean source {src_path}")
        self.__execute_cmd(f"mvn clean -f '{pom_path}'")
        print()


        mvn_container_name = f"mvn-builder-{app_name}"
        print("Starting builder container $mvn_container_name")
        self.__execute_cmd(f"docker kill '{mvn_container_name}' || exit 0")
        self.__execute_cmd(f"docker rm   '{mvn_container_name}' || exit 0")
        command = ""
        command = self.__append_cmd(command, f"docker run  --rm"                                                                               )
        command = self.__append_cmd(command, f"-e 'APP_NAME={mvn_container_env_app_name}'"       , mvn_container_env_app_name            )
        command = self.__append_cmd(command, f"-e 'TARGET_DIR={mvn_container_env_target_dir}'"     , mvn_container_env_target_dir          )
        command = self.__append_cmd(command, f"-e 'BUILD_CMD={mvn_container_env_build_cmd}'"      , mvn_container_env_build_cmd           )
        command = self.__append_cmd(command, f"-e 'BUILD_PROFILES={mvn_container_env_build_profiles}'" , mvn_container_env_build_profiles      )
        command = self.__append_cmd(command, f"-v '{src_path}:/usr/src/external/{app_name}'"           , src_path and app_name                 )
        command = self.__append_cmd(command, f"-v '{mvn_container_name}:/usr/src/mymaven/{app_name}'"  , mvn_container_name and app_name       )
        command = self.__append_cmd(command, f"-v '{target_path}:/build'"                              , target_path                           )
        command = self.__append_cmd(command, f"-v m2cache:/root/.m2"                                                                            )
        command = self.__append_cmd(command, f"--name '{mvn_container_name}' '{mvn_image_name}'"       , mvn_container_name and mvn_image_name )
        self.__execute_cmd(command)
        print()

        self.__print_end_process(start_at)



    def __evaluate(self, value):
        return os.path.expandvars(value) if value else ""



    def __execute_cmd(self, command: str):
        self.__print_cmd(command)
        result = subprocess.run(["bash"], input=command.replace("\n", " "), shell=True, capture_output=False, text=True)
        if result.returncode != 0:
            raise DmvnError("Command exit with code {}".format(result.returncode))
        print()



    def __print_cmd(self, command: str):
        print("> {}".format(command))
        stdout.flush()



    def __append_cmd(self, command, appendix, condition = True) -> str:
        if condition:
            if len(command) > 0:
                appendix = " \n  " + appendix
            return command + appendix

        return command



    def __print_end_process(self, start_at):
        end_at = time.time()
        delta = timedelta(milliseconds=(end_at - start_at))
        process_time = str(delta)
        if len(process_time) == 7:
            process_time = "0" + process_time
        print("End process in time {}".format(process_time))