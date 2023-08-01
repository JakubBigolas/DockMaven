import os
import subprocess
import time
from datetime import timedelta
from sys import stdout

from modules.dock_maven.error import DmvnError
from ..data.process_data import ProcessData
from ...app_context import AppContext


class ProcessInstanceHelper:

    def __init__(self):
        self.__app_context = AppContext.context()



    def evaluated(self, data: ProcessData) -> ProcessData:
        result = ProcessData()

        result.package                          = self.evaluate(data.package)
        result.app_name                         = self.evaluate(data.app_name)
        result.src_path                         = self.evaluate(data.src_path)
        result.mvn_image_name                   = self.evaluate(data.mvn_image_name)
        result.target_path                      = self.evaluate(data.target_path)
        result.mvn_container_env_app_name       = self.evaluate(data.mvn_container_env_app_name)
        result.mvn_container_env_target_dir     = self.evaluate(data.mvn_container_env_target_dir)
        result.mvn_container_env_build_cmd      = self.evaluate(data.mvn_container_env_build_cmd)
        result.mvn_container_env_build_profiles = self.evaluate(data.mvn_container_env_build_profiles)
        result.mvn_clean                        = self.evaluate(data.mvn_clean)

        return result



    def evaluate(self, value):
        return os.path.expandvars(value) if value else ""



    def execute_cmd(self, command: str):
        self.print_cmd(command)
        result = subprocess.run(["bash"], input=command.replace("\n", " "), shell=True, capture_output=False, text=True)
        if result.returncode != 0:
            raise DmvnError(None, result.returncode)
        print()



    def print_cmd(self, command: str):
        print("> {}".format(command))
        stdout.flush()



    def append_cmd(self, command, appendix, condition = True) -> str:
        if condition:
            if len(command) > 0:
                appendix = " \n  " + appendix
            command += appendix

        return command


    def print_contetx_params(self, data: ProcessData, original: ProcessData):
        print("Context params:")
        print(" - package                          ={}  ({})".format(data.package                          , original.package))
        print(" - app_name                         ={}  ({})".format(data.app_name                         , original.app_name))
        print(" - src_path                         ={}  ({})".format(data.src_path                         , original.src_path))
        print(" - mvn_image_name                   ={}  ({})".format(data.mvn_image_name                   , original.mvn_image_name))
        print(" - target_path                      ={}  ({})".format(data.target_path                      , original.target_path))
        print(" - mvn_container_env_app_name       ={}  ({})".format(data.mvn_container_env_app_name       , original.mvn_container_env_app_name))
        print(" - mvn_container_env_target_dir     ={}  ({})".format(data.mvn_container_env_target_dir     , original.mvn_container_env_target_dir))
        print(" - mvn_container_env_build_cmd      ={}  ({})".format(data.mvn_container_env_build_cmd      , original.mvn_container_env_build_cmd))
        print(" - mvn_container_env_build_profiles ={}  ({})".format(data.mvn_container_env_build_profiles , original.mvn_container_env_build_profiles))
        print(" - mvn_clean                        ={}"      .format(data.mvn_clean))
        print()



    def recreate_target_dir(self, data: ProcessData):
        target_dir = data.target_path + "/target"
        print("Recreate target dir {}".format(target_dir))
        self.__app_context.recreate_dir(target_dir)
        print()



    def clean_sources(self, data: ProcessData):
        if data.mvn_clean and data.mvn_clean.lower() == "true":
            pom_path = f"{data.src_path}/pom.xml"
            print(f"Clean source {data.src_path}")
            self.execute_cmd(f"mvn clean -f '{pom_path}'")
            print()



    def run_mvn_builder(self, data: ProcessData):
        print("Starting builder container $mvn_container_name")
        print()
        mvn_container_name = f"mvn-builder-{data.app_name}"
        self.execute_cmd(f"docker kill '{mvn_container_name}' || exit 0")
        self.execute_cmd(f"docker rm   '{mvn_container_name}' || exit 0")
        command = ""
        command = self.append_cmd(command, f"docker run  --rm"                                                                                          )
        command = self.append_cmd(command, f"-e 'APP_NAME={data.mvn_container_env_app_name}'"             , data.mvn_container_env_app_name             )
        command = self.append_cmd(command, f"-e 'TARGET_DIR={data.mvn_container_env_target_dir}'"         , data.mvn_container_env_target_dir           )
        command = self.append_cmd(command, f"-e 'BUILD_CMD={data.mvn_container_env_build_cmd}'"           , data.mvn_container_env_build_cmd            )
        command = self.append_cmd(command, f"-e 'BUILD_PROFILES={data.mvn_container_env_build_profiles}'" , data.mvn_container_env_build_profiles       )
        command = self.append_cmd(command, f"-v '{data.src_path}:/usr/src/external/{data.app_name}'"      , data.src_path and data.app_name             )
        command = self.append_cmd(command, f"-v '{mvn_container_name}:/usr/src/mymaven/{data.app_name}'"  , mvn_container_name and data.app_name        )
        command = self.append_cmd(command, f"-v '{data.target_path}/target:/builds'"                      , data.target_path                            )
        command = self.append_cmd(command, f"-v m2cache:/root/.m2"                                                                                      )
        command = self.append_cmd(command, f"--name '{mvn_container_name}' '{data.mvn_image_name}'"       , mvn_container_name and data.mvn_image_name  )
        self.execute_cmd(command)



    def print_end_process(self, start_at):
        end_at = time.time()
        delta = timedelta(milliseconds=(end_at - start_at))
        process_time = str(delta)
        if len(process_time) > 2 and process_time[2] == ":":
            process_time = "0" + process_time
        print("End process in time {}".format(process_time))
        print()
