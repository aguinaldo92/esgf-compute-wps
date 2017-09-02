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

# WPS Settings
VERSION = setting('WPS_VERSION', '1.0.0')
SERVICE = setting('WPS_SERVICE', 'WPS')
LANG = setting('WPS_LANG', 'en-US')
TITLE = setting('WPS_TITLE', 'LLNL WPS')
NAME = setting('WPS_NAME', 'Lawerence Livermore National Laboratory')
SITE = setting('WPS_SITE', 'https://llnl.gov')

# ophidia settings
OPH_USER = setting('user' , 'oph-test')
OPH_PASSWD = setting('passwd' , 'abcd')
OPH_HOSTNAME = setting('hostname' , '127.0.0.1')
OPH_PORT = setting('port','11732')

this_dir = os.path.dirname(__file__)
workflows_dir_relpath = os.path.join(this_dir, '../ophidia/workflows/')
workflows_dir = os.path.normpath(workflows_dir_relpath)
workflows_dir += '/'
OPH_WORKFLOWS_PATH = setting('oph_workflows_path' , workflows_dir)
OPH_EXPORT_PATH = setting('oph_export_path' , '/usr/local/ophidia/apache-tomcat-6.0.45/content/thredds/public/ophidia_test_data/')
