import time

from .process_instance_helper import ProcessInstanceHelper
from ..data.process_data import ProcessData
from ...app_context import AppContext


class ProcessInstance:

    def __init__(self, data: ProcessData):
        self.__data = data
        self.__app_context = AppContext.context()
        self.__helper = ProcessInstanceHelper()



    def execute(self):
        start_at = time.time()
        data = self.__helper.evaluated(self.__data)

        self.__helper.print_contetx_params(data, self.__data)
        self.__helper.recreate_target_dir(data)
        self.__helper.clean_sources(data)
        self.__helper.run_mvn_builder(data)
        self.__helper.print_end_process(start_at)
