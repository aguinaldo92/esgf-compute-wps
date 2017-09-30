#! /usr/bin/env python

import os

from functools import partial

from django.conf import settings

from os.path import normpath

setting = partial(getattr, settings)


# General Settings
OAUTH2_CALLBACK = setting('WPS_OAUTH2_CALLBACK', 'https://aims2.llnl.gov/auth/callback')

HOSTNAME = setting('WPS_EXTERNAL_HOSTNAME', '0.0.0.0')
PORT = setting('WPS_EXTERNAL_PORT', '8000')

CACHE_PATH = setting('WPS_CACHE_PATH', '/data/cache')

ENDPOINT = setting('WPS_ENDPOINT', 'http://0.0.0.0:8000/wps')
STATUS_LOCATION = setting('WPS_STATUS_LOCATION', 'http://0.0.0.0:8000/wps/job/{job_id}')

OUTPUT_LOCAL_PATH = setting('WPS_OUTPUT_LOCAL_PATH', '/data/public')
OUTPUT_URL = setting('WPS_OUTPUT_URL', 'http://0.0.0.0:8000/wps/output/{file_name}')

DAP = setting('WPS_DAP', False)
DAP_URL = setting('WPS_DAP_URL', 'https://0.0.0.0:8000/{file_name}')

CA_PATH = setting('WPS_CA_PATH', '/tmp/certs')

ADMIN_EMAIL = 'admin@wps.llnl.gov'

LOGIN_URL = 'http://0.0.0.0:8000/wps/home/login'

CREATE_SUBJECT = 'Welcome to ESGF compute server'
CREATE_MESSAGE = """
Thank you for creating an account for the ESGF compute server. Please login into your account <a href="{login_url}">here</a>.

If you have any questions or concerns please email the <a href="mailto:{admin_email}">server admin</a>.
"""

# WPS Settings
VERSION = setting('WPS_VERSION', '1.0.0')
SERVICE = setting('WPS_SERVICE', 'WPS')
LANG = setting('WPS_LANG', 'en-US')
TITLE = setting('WPS_TITLE', 'LLNL WPS')
NAME = setting('WPS_NAME', 'Lawerence Livermore National Laboratory')
SITE = setting('WPS_SITE', 'https://llnl.gov')

# ophidia settings
OPH_USER = setting('OPH_USER' , 'oph-test')
OPH_PASSWD = setting('OPH_PASSWD' , 'abcd')
OPH_HOSTNAME = setting('OPH_HOSTNAME' , '127.0.0.1')
OPH_PORT = setting('OPH_PORT','11732')

OPH_WORKFLOW_NAME = setting('OPH_WORKFLOW_NAME' , os.path.normpath(os.path.join(os.path.dirname(__file__), '../workflows/')) + '/{wname}.json' )
OPH_EXPORT_PATH = setting('OPH_EXPORT_PATH' , '/usr/local/ophidia/apache-tomcat-6.0.45/content/thredds/public/ophidia_test_data/')

# THREDDS SETTINGS
THREDDS_DAP_URL = setting('THREDDS_DAP_URL', 'http://127.0.0.1:8080/thredds/dodsC/testOphidia/{file_name}.nc') 
