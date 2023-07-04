from ....data.option_data import OptionData


class OptionHandlerAbstract:



    def handle(self, args: list) -> OptionData:
        raise NotImplementedError



    def accepts(self, args: list) -> bool:
        raise NotImplementedError
