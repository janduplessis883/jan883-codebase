import time
from loguru import logger

# = Decorators =================================================================


def time_it(func):
    def wrapper(*args, **kwargs):
        func_name = func.__name__
        logger.info(f"🖥️    Started: '{func_name}'")
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        elapsed_time = end_time - start_time
        func_name = func.__name__
        logger.info(f"✅ Completed: '{func_name}' ⚡️{elapsed_time:.6f} sec")
        return result

    return wrapper
