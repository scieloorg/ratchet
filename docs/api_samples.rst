===============
API Use Samples
===============

Python Sample
=============

Registering a journal access via POST method::

    Python 2.6.6 (r266:84374, Aug 31 2010, 11:00:51) 
    [GCC 4.0.1 (Apple Inc. build 5493)] on darwin
    Type "help", "copyright", "credits" or "license" for more information.
    >>> import urllib2
    >>> req = urllib2.Request("http://localhost:8888/api/v1/journal","code=1981-6723&region=bra")
    >>>
    >>> urllib2.urlopen("http://localhost:8888/api/v1/journal?code=1981-6723").read()
    "{u'code': u'1981-6723', u'_id': ObjectId('50295ae0714e86b6a66ace04'), u'2012-08': 33, u'2012-08-16': 7, u'total': 33, u'type': u'journal', u'bra': 33, u'2012-08-13': 26}"
    >>> 
    >>> 
    >>> urllib2.urlopen(req).read()
    ''
    >>> urllib2.urlopen("http://localhost:8888/api/v1/journal?code=1981-6723").read()
    "{u'code': u'1981-6723', u'_id': ObjectId('50295ae0714e86b6a66ace04'), u'2012-08': 34, u'2012-08-16': 8, u'total': 34, u'type': u'journal', u'bra': 34, u'2012-08-13': 26}"
    >>> 

Recovering a journal accesses via GET method::

    Python 2.6.6 (r266:84374, Aug 31 2010, 11:00:51) 
    [GCC 4.0.1 (Apple Inc. build 5493)] on darwin
    Type "help", "copyright", "credits" or "license" for more information.
    >>> import urllib2
    >>> 
    >>> urllib2.urlopen("http://localhost:8888/api/v1/journal?code=1981-6723").read()
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

Registering a journal access via POST method::

    test_post.php
    <?php
    $postdata = http_build_query(
        array(
            'code' => '1981-6723',
            'region' => 'bra'
        )
    );

    $opts = array('http' =>
        array(
            'method'  => 'POST',
            'header'  => 'Content-type: application/x-www-form-urlencoded',
            'content' => $postdata
        )
    );

    $context = stream_context_create($opts);

    file_get_contents('http://localhost:8888/api/v1/journal?code=1981-6723&region=bra', false, $context);
    ?>

    :ratchet fabiobatalha$ php test_get.php
    {u'code': u'1981-6723', u'_id': ObjectId('50295ae0714e86b6a66ace04'), u'2012-08': 40, u'2012-08-16': 14, u'total': 40, u'type': u'journal', u'bra': 40, u'2012-08-13': 26}

    :ratchet fabiobatalha$ php test_post.php 
    
    :ratchet fabiobatalha$ php test_get.php
    {u'code': u'1981-6723', u'_id': ObjectId('50295ae0714e86b6a66ace04'), u'2012-08': 41, u'2012-08-16': 15, u'total': 41, u'type': u'journal', u'bra': 41, u'2012-08-13': 26}

Recovering a journal accesses via GET method::

    test_get.php
    <?php
    print file_get_contents("http://localhost:8888/api/v1/journal?code=1981-6723");
    ?>

    :ratchet fabiobatalha$ php test_get.php
    {u'code': u'1981-6723', u'_id': ObjectId('50295ae0714e86b6a66ace04'), u'2012-08': 35, u'2012-08-16': 9, u'total': 35, u'type': u'journal', u'bra': 35, u'2012-08-13': 26}
