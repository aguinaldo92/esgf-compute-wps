#! /usr/bin/env python

import os
import uuid
from contextlib import closing
from contextlib import nested

import cdms2
import cwt
import dask.array as da
import numpy as np
from celery import shared_task
from celery.utils.log import get_task_logger
from dask import delayed

from wps import models
from wps import settings
from wps.processes import cwt_shared_task
from wps.processes import register_process

logger = get_task_logger('wps.processes.simple')

__all__ = ['sum']

@register_process('SIMPLE.sum')
def sum(self, variable, **kwargs):
    status = self.initialize(credentials=True, **kwargs)

    status.job.started()

    print(vars(variable))

    input_var = op.inputs[0]

    var_name1 = input_var[0].var_name

    var_name2 = input_var[1].var_name
    
    out_local_path = self.generate_local_output()

    status.update('Beginning simple sum of two values')


    out_path = self.generate_output(out_local_path, **kwargs)

    out_var = int(var_name1 + var_name2)
    
    print('out var :')
    
    print( out_var)

    return out_var.parameterize()


