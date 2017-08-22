#! /usr/bin/env python

import logging
import json
import re
import sys
from pprint import pprint


__all__ = ['parse_input']

logger = logging.getLogger('simple.parse_input')


def parse_input(data_inputs): 

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
 
