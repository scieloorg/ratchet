===============
API Use Samples
===============

Python Sample
=============

Registering a journal access via POST method::

    import

Recovering a journal accesses via GET method::

    Python 2.6.6 (r266:84374, Aug 31 2010, 11:00:51) 
    [GCC 4.0.1 (Apple Inc. build 5493)] on darwin
    Type "help", "copyright", "credits" or "license" for more information.
    >>> import urllib2
    >>> 
    >>> urllib2.urlopen("http://localhost:8888/api/v1/journal?code=1981-6723&region=bra").read()
    "{u'code': u'1981-6723', u'_id': ObjectId('50295ae0714e86b6a66ace04'), u'2012-08': 29, u'2012-08-16': 3, u'total': 29, u'type': u'journal', u'bra': 29, u'2012-08-13': 26}"
    >>> 

Curl Sample
===========

Registering a journal access via POST method::

    :ratchet fabiobatalha$ curl -X POST "http://localhost:8888/api/v1/journal?code=1981-6723&region=bra"
    :ratchet fabiobatalha$ 

Recovering a journal accesses via GET method::

    :ratchet fabiobatalha$ curl -X GET http://localhost:8888/api/v1/journal?code=1981-6723

    {
        u'code': u'1981-6723', 
        u'_id': ObjectId('50295ae0714e86b6a66ace04'), 
        u'2012-08': 28, 
        u'2012-08-16': 2, 
        u'total': 28, 
        u'type': u'journal', 
        u'bra': 28, 
        u'2012-08-13': 26
    }

PHP Sample
==========