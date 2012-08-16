===============
API Use Samples
===============

Python Sample
=============

Sample using python::

    import


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