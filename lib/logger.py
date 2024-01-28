import sys
import logging
import logging as log

def get_logger():
    for handler in log.root.handlers[:]:
        log.root.removeHandler(handler)        
    log.basicConfig(format="[ %(levelname)s ] %(message)s", level=log.INFO, stream=sys.stdout)
    return log