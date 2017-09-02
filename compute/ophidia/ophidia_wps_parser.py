#! /usr/bin/env python

import logging
import json
import re
import sys
from pprint import pprint
from wps import settings



__all__ = ['parse_workflow_parameters']

logger = logging.getLogger('ophidia_wps_parser.parse_workflow_parameters')

def parse_inputs(data_inputs):
    match = re.search('\[(.*)\]', data_inputs)

    kwargs = dict((x.split('=')[0], json.loads(x.split('=')[1])) for x in match.group(1).split(';'))
    return kwargs 


def parse_workflow_names(kwargs): 
    """ estrae una lista di nomi di identifier e li strasforma in una lista di workflows"""
    workflow_names = [ x.get("name").split('.')[1] for x in kwargs.get('operation', [])]
    pprint(workflow_names)
    workflows_names = [ "".join(x) for x in workflow_names]
    pprint(workflow_names)
    
    workflows = []
    for w in workflows_names:
        #~ print("w = {} {}".format(w,type(w)))
        w = w.encode('ascii','ignore') 
        w += ".json"
        print(settings.OPH_WORKFLOWS_PATH)
        w = settings.OPH_WORKFLOWS_PATH + w
        workflows.append(w)
        #~ print("w = {} {}".format(w,type(w)))
    
    #~ print(workflows)
    #~ print(len(workflows))
    
    #~ for w in workflows:
        #~ print("w_aggiunti = {} {}".format(w,type(w)))
    
    return workflows
    
def parse_uri(kwargs):
    nc_uri = [x.get("uri") for x in kwargs.get('variable', []) if x.get("uri")[-3:] == ".nc"]
    
    pprint(nc_uri)
    
    return nc_uri



def parse_workflow_parameters(self, data_inputs): 

    kwargs = self.parse_datainputs(data_inputs)
    
    #operation = [cwt.Process.from_dict(x) for x in kwargs.get('operation', [])]
    
    workflow_name = parse_workflow_names(kwargs)

    match_variables = re.search('\[(.*)\]', data_inputs)
    match = re.search('\[(.*)\]', match_variables.group(1))
    print('data_inputs')
    print(data_inputs)
    print('match')
    print(match)
    print('match_group1')
    print(match.group(1))
    
    
    #stringa_variabili = re.search('\{(.*)\}', match.group(1))
    #lista_variabili = stringa_variabili.split(',')
    semicolon_delimited = match.group(1).replace("},","};")
    kwargs = dict()
    #match_brackets = re.search('\{(.*)\},', match.group(1))
    #print(match_brackets.group())
    for i in semicolon_delimited.split(';'):
        print("semicolon_delimited :  {}".format(i) )
        y = i.replace("}","")
        i = y.replace("{","")
        print("i :  {}".format(i) )
        i_key = i.split(':')[0]
        i_value = i.split(':')[1]
        kwargs[i.split(':')[0]] = i.split(':')[1]
    # kwargs = dict(((x.split(':')[0], json.loads(x.split(':')[1])) for x in var.group(i)) for i in 1,2 )
    print('kwargs')
    pprint(kwargs)
    variables = [x for x in kwargs.get('value', [])]
    print('variables')
    pprint(variables)
    return variables
 
