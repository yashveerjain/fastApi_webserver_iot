import os

error_string = """
Error Type     = {type},
Error          = {e}
Exception Type = {exc_type}
File Name      = {fname}
Line Number    = {tb_lineno}
"""

def get_error_message(e, exc_info) -> str:
    exc_type, exc_obj, exc_tb = exc_info
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    return error_string.format(
        type=type(e), e=e, exc_type=exc_type, fname=fname, tb_lineno=exc_tb.tb_lineno
    )
