from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render

import pywps
from pywps import Pywps

from lxml import etree

import os
import re
import json
import settings

os.environ['PYWPS_PROCESSES'] = os.path.join(settings.WPS_SERVER_DIR, 'processes')

def strip_tag_namespace(tag):
    if re.match('^{.*}', tag):
        return re.sub('^{.*}', '', tag)

    return tag

def execute_process(method, query_string):
    service = Pywps(method)

    service_inputs = service.parseRequest(query_string)

    return service.performRequest(service_inputs)

def view_main(request):
    return render(request, 'wps/index.html')

def api_processes(request):
    service_response = execute_process(pywps.METHOD_GET, 'version=1.0&service=wps&request=getcapabilities')

    root = etree.fromstring(service_response)

    ns = {
        'wps': 'http://www.opengis.net/wps/1.0.0',
        'ows': 'http://www.opengis.net/ows/1.1',
    }

    process_offerings = root.xpath('/wps:Capabilities/wps:ProcessOfferings/*', namespaces=ns)

    processes = []

    for offering in process_offerings:
        process = {}

        processes.append(process)

        for entry in offering:
            tag_cleaned = strip_tag_namespace(entry.tag)

            process[tag_cleaned] = entry.text    

    return JsonResponse({'processes': processes})

def wps(request):
    service_response = execute_process(pywps.METHOD_GET, request.META['QUERY_STRING'])

    return HttpResponse(service_response, content_type='text/xml')