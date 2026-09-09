import sys
import logging


class NetworkSecurityException(Exception):
    def __init__(self, error_message, error_details: sys):
        self.error_message = str(error_message)
        exc_info = error_details.exc_info()

        self.lineno = -1
        self.file_name = "unknown"

        if exc_info[2] is not None:
            exc_tb = exc_info[2]
            self.lineno = exc_tb.tb_lineno
            self.file_name = exc_tb.tb_frame.f_code.co_filename

    def __str__(self):
        return (
            f"Error occurred in Python script name [{self.file_name}] "
            f"line number [{self.lineno}] error message [{self.error_message}]"
        )


if __name__ == "__main__":
    try:
        logging.info("Enter the try block")
        a = 1 / 0
        print("This will not be printed")
    except Exception as e:
        raise NetworkSecurityException(e, sys) from e
