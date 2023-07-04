import os
import shutil

from config import get_app_config


class AppContext:

    def __init__(self, context_path: str):
        self.__context_path = context_path
        self.__projects_dir = context_path + "/projects"



    def read_configs(self):
        return self.__load_file(self.__projects_dir, "configs.yaml")



    def save_configs(self, configs: str):
        configs = "" if configs is None else configs
        self.__save_file(self.__projects_dir, "configs.yaml", configs)




    def __load_file(self, path, fname):
        try:
            file = open(path + "/" + fname, "rt")
            result = file.read() if file.readable() else None
            file.close()
            return result
        except:
            return None



    def __save_file(self, path, fname, text):
        file = open(path + "/" + fname, "wt")
        file.write(text)
        file.close()



    def __remove_file(self, path, fname):
        try:
            os.remove(path + "/" + fname)
        except:
            pass



    def recreate_dir(self, path):
        if os.path.isdir(path):
            shutil.rmtree(path)
        os.makedirs(path)



    # STATIC



    @staticmethod
    def __load_config(config: dict, variable: str, default) -> str :
        """
            Try to load variable from config.py file or if there is no such argument tries to load from env variables
            :param variable name
            :param default If there is no value for name in both sources returns default value
        """
        try:
            return config[variable] if config is not None and config[variable] else os.environ[variable]
        except KeyError:
            return default



    @staticmethod
    def context_from(config: dict):
        return AppContext(AppContext.__load_config(config, "DMVN_PROJECTS_DIR", "~/dmvn"))



    @staticmethod
    def context():
        return AppContext.context_from(get_app_config())


