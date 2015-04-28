# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import time
import sys
try:
    import simplejson as json
except ImportError:
    import json
import requests
from distutils.version import StrictVersion

PY3 = sys.version_info[0] == 3


if PY3:
    def reraise(tp, value, tb=None):
        if value.__traceback__ is not tb:
            raise value.with_traceback(tb)
        raise value

else:
    exec('def reraise(tp, value, tb=None):\n raise tp, value, tb')


def touch(fname, times=None):
    dirname = '/'.join(fname.split('/')[:-1])
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    with file(fname, 'a'):
        os.utime(fname, times)


def get_from_api(uri):
    """
        Get an object from the api
    """
    api_uri = config.get('oarapi', 'uri')
    api_limit = config.get('oarapi', 'limit')
    headers = {'Accept': 'application/json'}
    r = requests.get(api_uri + uri + "?limit=" + api_limit, headers=headers)
    if r.status_code != 200:
        print("Could not get " + api_uri + uri)
        r.raise_for_status()
    if StrictVersion(requests.__version__) >= StrictVersion("2.0.0"):
        return r.json()
    else:
        return r.json


def get(uri, config, cache_file, cache_delay, reload_cache=False):
    """
        Get from the cache or from the api
    """
    cache_file = os.path.expanduser(cache_file)
    if (config.get('oarapi', 'caching') and not reload_cache
            and os.path.isfile(cache_file)
            and time.time() - os.path.getmtime(cache_file) < cache_delay):
        json_data = open(cache_file)
        return json.load(json_data)
    else:
        data = get_from_api(uri)
    if config.get('oarapi', 'caching'):
        touch(cache_file)
        chmod = True
        if os.path.isfile(cache_file):
            chmod = False
        file = open(cache_file, 'w')
        json.dump(data, file)
        file.close
        if chmod:
            os.chmod(cache_file, 0666)
    return data


def get_resources(config):
    cache_file = config.get('oarapi', 'caching_resources_file')
    cache_delay = config.getint('oarapi', 'caching_resources_delay')
    return get('/resources/details', cache_file, cache_delay)["items"]


def get_jobs(config):
    cache_file = config.get('oarapi', 'caching_jobs_file')
    cache_delay = config.getint('oarapi', 'caching_jobs_delay')
    return get('/jobs/details', cache_file, cache_delay)["items"]


def cprint(str, *args):
    """
        Custom print function to get rid of trailing newline and space
    """
    sys.stdout.write(str % args)


def init_colorama():
    from colorama import init
    init()
