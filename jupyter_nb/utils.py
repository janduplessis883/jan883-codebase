import inspect


def list_functions(module):
    """
    List all functions in the given module.

    Args:
    - module: The module to inspect.

    Returns:
    - A list of function names in the module.
    """
    functions = inspect.getmembers(module, inspect.isfunction)
    function_names = [function_name for function_name, function in functions]
    return function_names
