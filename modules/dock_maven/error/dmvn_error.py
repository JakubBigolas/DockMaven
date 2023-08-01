class DmvnError(RuntimeError):

    def __init__(self, error: str, error_code = 1):
        super().__init__(error)
        self.__error = error
        self.__error_code = error_code

    @property
    def error(self):
        return self.__error

    @property
    def error_code(self):
        return self.__error_code
