class OptionData:

    def __init__(self, package: str):
        self.__package = package

    @property
    def package(self):
        return self.__package