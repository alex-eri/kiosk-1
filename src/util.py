import time
from functools import wraps
import logging


def retry(ExceptionToCheck, tries=5, delay=3, backoff=2):
    def deco_retry(f):

        @wraps(f)
        def f_retry(*args, **kwargs):
            mtries, mdelay = tries, delay
            while mtries > 1:
                try:
                    return f(*args, **kwargs)
                except ExceptionToCheck as e:
                    msg = "try %d %s failed with %s, Retrying in %d seconds..." % \
                        (mtries, f.__name__, str(e), mdelay)
                    logging.error(msg)
                    time.sleep(mdelay)
                    mtries -= 1
                    mdelay *= backoff
            logging.warning( "Last try %s" % (f.__name__))
            return f(*args, **kwargs)

        return f_retry  # true decorator

    return deco_retry
