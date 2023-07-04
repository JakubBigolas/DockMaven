from copy import deepcopy

from .option_data import OptionData


class OptionBuildData(OptionData):

    def __init__(self, package: str, params: dict):
        super().__init__(package)
        self.__params = params

    @property
    def params(self):
        return deepcopy(self.__params)
