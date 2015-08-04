import cdms2
import cdutil

from celery import Celery
from modules import configuration
from base_task import DomainBasedTask
from engines.kernels.manager import kernelMgr
from modules.utilities import *

app = Celery( 'tasks', broker=configuration.CDAS_CELERY_BROKER, backend=configuration.CDAS_CELERY_BACKEND )

app.conf.update(
    CELERY_TASK_SERIALIZER='json',
    CELERY_ACCEPT_CONTENT=['json','pickle'],  # Ignore other content
    CELERY_RESULT_SERIALIZER='pickle',
)

@app.task(base=DomainBasedTask,name='tasks.execute')
def execute( run_args ):
    result = kernelMgr.run( run_args )
    return result

@app.task(base=DomainBasedTask,name='tasks.mergeResults')
def mergeResults( result_list ):
    return result_list

@app.task(base=DomainBasedTask,name='tasks.simpleTest')
def simpleTest( input_list ):
    return [ int(v)*3 for v in input_list ]


