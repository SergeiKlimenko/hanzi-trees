import os
import sys
import logging
INTERP = os.path.expanduser('/home/kangximaster/kangxi/bin/python3')
if sys.executable != INTERP:
    os.execl(INTERP, INTERP, *sys.argv)
# append current dir to module path
cwd = os.getcwd()
sys.path.append(cwd)
# assuming this module is in the same dir as passenger_wsgi, this now works!
sys.path.append('app')
import app

# create a logfile in the current directory
logfilename = os.path.join(cwd, 'passenger_wsgi.log')
# configure the logging
logging.basicConfig(filename=logfilename, level=logging.DEBUG)
logging.info("Running %s", sys.executable)

def application(environ, start_response):
    logging.info("Application called:")
    logging.info("environ: %s", str(environ))
    results = []
    try:
        results = app.app(environ, start_response)
        logging.info("App executed successfully")
    except Exception as inst:
        logging.exception("Error: %s", str(type(inst)))
    logging.info("Application call done")
    return results

