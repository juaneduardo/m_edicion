#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Project-wide application configuration.

DO NOT STORE SECRETS, PASSWORDS, ETC. IN THIS FILE.
They will be exposed to users. Use environment variables instead.
"""

import os

PROJECT_NAME = 'Manual de Periodismo de Datos Iberoamericano'
DEPLOYED_NAME = '' 
REPOSITORY_NAME = 'm_edicion'

PRODUCTION_S3_BUCKETS = ['manual.periodismodedatos.org']
PRODUCTION_SERVERS = ['manual.periodismodedatos.org']

STAGING_S3_BUCKETS = ['stage-apps.npr.org']
STAGING_SERVERS = ['cron-staging.nprapps.org']

S3_BUCKETS = []
SERVERS = []
DEBUG = True

PROJECT_DESCRIPTION = 'Manual de Periodismo de Datos Iberoamericano.'
SHARE_URL = 'http://%s/%s' % (PRODUCTION_S3_BUCKETS[0], DEPLOYED_NAME)


TWITTER = {
    'TEXT': PROJECT_NAME,
    'URL': SHARE_URL
}

FACEBOOK = {
    'TITLE': PROJECT_NAME,
    'URL': SHARE_URL,
    'DESCRIPTION': PROJECT_DESCRIPTION,
    'IMAGE_URL': '',
    'APP_ID': '451757221525971'
}

NPR_DFP = {
    'STORY_ID': '',
    'TARGET': ''
}

GOOGLE_ANALYTICS_ID = 'UA-39350524-1'

def configure_targets(deployment_target):
    """
    Configure deployment targets. Abstracted so this can be
    overriden for rendering before deployment.
    """
    global S3_BUCKETS
    global SERVERS
    global DEBUG

    if deployment_target == 'production':
        S3_BUCKETS = PRODUCTION_S3_BUCKETS
        SERVERS = PRODUCTION_SERVERS
        DEBUG = False
    else:
        S3_BUCKETS = STAGING_S3_BUCKETS
        SERVERS = STAGING_SERVERS
        DEBUG = True

DEPLOYMENT_TARGET = os.environ.get('DEPLOYMENT_TARGET', None)

configure_targets(DEPLOYMENT_TARGET)
