import sys


def error_message_detail(error: Exception, error_detail: sys) -> str:
    _, _, exc_tb = error_detail.exc_info()

    file_name: str = exc_tb.tb_frame.f_code.co_filename

    error_message: str = "Error occurred python script name [{0}] line number [{1}] error message [{2}]".format(
        file_name, exc_tb.tb_lineno, str(error)
    )

    return error_message


class WaferException(Exception):
    def __init__(self, error_message: Exception, error_detail: sys):
        """
        :param error_message: error message in string format
        """
        super().__init__(error_message)

        self.error_message: str = error_message_detail(
            error_message, error_detail=error_detail
        )

    def __str__(self):
        return self.error_message
