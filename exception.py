# -*- coding: utf-8 -*-
#                           ██╗██████╗ ██╗           
#                           ██║╚════██╗██║           
#                           ██║ █████╔╝██║           
#                      ██   ██║██╔═══╝ ██║           
#                      ╚█████╔╝███████╗███████╗      
#                       ╚════╝ ╚══════╝╚══════╝      
#                       https://jusdeliens.com
#
# Designed with 💖 by Jusdeliens
# Under CC BY-NC-ND 4.0 licence  
# https://creativecommons.org/licenses/by-nc/4.0/deed.en 

# Allow import without error 
# "relative import with no known parent package"
# In vscode, add .env file with PYTHONPATH="..." 
# with the same dir to allow intellisense
import os
import sys
__workdir__ = os.path.dirname(os.path.abspath(__file__))
sys.path.append(__workdir__)

import inspect
import time

def toBeImplemented(message=None):
    """
    Raise an exception NotImplementedError
    To be used in interface method bodies or 
    anywhere else where a todo is required
    before use.
    """
    stack = inspect.stack()
    if ( message == None ):
        message = ""
    elif (len(message) > 0 and message[0] != "\n"):
        message = "\n" + message        
    raise NotImplementedError(f"🚧 {stack[1][3]}() not implemented yet!{message}")


def retry(maxRetries=1, sleepBetween=1):
    """
    Decorates any function to be called maxRetries
    time if an exception is raised
    ## Sample
    ```python
    @retry(maxRetries=2, sleepBetween=1)
    def might_fail():
        print("might_fail")
        raise Exception
    ```
    """
    def retry_decorator(func):
        def __wrapper(*args, **kwargs):
            for _ in range(maxRetries):
                try:
                    func(*args, **kwargs)
                except:
                    time.sleep(sleepBetween)
        return __wrapper
    return retry_decorator