import inspect
import os
import sys


def stackclimber(height=0):           # http://stackoverflow.com/a/900404/48251
    """
    Obtain the name of the caller's module. Uses the inspect module to find
    the caller's position in the module hierarchy. With the optional height
    argument, finds the caller's caller, and so forth.
    """
    caller = inspect.stack()[height+1]
    scope = caller[0].f_globals
    path = scope['__name__'].split('__main__')[0].strip('.')
    if path == '':
        if scope['__package__']:
            path = scope['__package__']
        else:
            path = os.path.basename(sys.argv[0]).split('.')[0]
    return path
