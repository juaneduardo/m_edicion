#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from mimetypes import guess_type
import urllib

import envoy
from flask import Flask, Markup, abort, render_template

import app_config
from render_utils import flatten_app_config, make_context
app = Flask(app_config.PROJECT_NAME)

# Example application views
@app.route('/')
def index():
    import feedparser
    noticias_tumblr = "http://periodismodedatos.tumblr.com/rss"
    feed = feedparser.parse( noticias_tumblr )

    return render_template('index.html', feed=feed, **make_context())


@app.route('/manual.html')
def manual():
    """
    Example view demonstrating rendering a simple HTML page.
    """
    return render_template('manual.html', **make_context())

@app.route('/colaborar.html')
def colaborar():
    """
    Example view demonstrating rendering a simple HTML page.
    """
    return render_template('colaborar.html', **make_context())

@app.route('/indice.html')
def indice():
    """
    Example view demonstrating rendering a simple HTML page.
    """
    return render_template('indice.html', **make_context())

@app.route('/participantes.html')
def participantes():
    """
    Example view demonstrating rendering a simple HTML page.
    """
    return render_template('participantes.html', **make_context())

# Render LESS files on-demand
@app.route('/less/<string:filename>')
def _less(filename):
    try:
        with open('less/%s' % filename) as f:
            less = f.read()
    except IOError:
        abort(404)

    r = envoy.run('node_modules/.bin/lessc -', data=less)

    return r.std_out, 200, { 'Content-Type': 'text/css' }

# Render JST templates on-demand
@app.route('/js/templates.js')
def _templates_js():
    r = envoy.run('node_modules/.bin/jst --template underscore jst')

    return r.std_out, 200, { 'Content-Type': 'application/javascript' }

# Render application configuration
@app.route('/js/app_config.js')
def _app_config_js():
    config = flatten_app_config()
    js = 'window.APP_CONFIG = ' + json.dumps(config)
    
    return js, 200, { 'Content-Type': 'application/javascript' }

# Server arbitrary static files on-demand
@app.route('/<path:path>')
def _static(path):
    try:
        with open('www/%s' % path) as f:
            print guess_type(path)[0]
            return f.read(), 200, { 'Content-Type': guess_type(path)[0] }
    except IOError:
        abort(404)

@app.template_filter('urlencode')
def urlencode_filter(s):
    """
    Filter to urlencode strings.
    """
    if type(s) == 'Markup':
        s = s.unescape()
        
    s = s.encode('utf8')
    s = urllib.quote_plus(s)

    return Markup(s)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=app_config.DEBUG)
