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
    "{
        u'code': u'1981-6723', 
        u'_id': ObjectId('50295ae0714e86b6a66ace04'), 
        u'journal': 
            {
                'y2012':
                    {
                        'm08': 
                            {
                                'd16': 7,
                                'd13': 26, 
                            },
                            total: 33
                    },
                    'total': 33 
            },
        u'type': u'journal', 
        u'bra': 33, 
    }"
    >>> 
    >>> 
    >>> urllib2.urlopen(req).read()
    ''
    >>> urllib2.urlopen("http://localhost:8888/api/v1/journal?code=1981-6723").read()
    "{
        u'code': u'1981-6723', 
        u'_id': ObjectId('50295ae0714e86b6a66ace04'), 
        u'journal': 
            {
                'y2012':
                    {
                        'm08': 
                            {
                                'd16': 7,
                                'd13': 27, 
                            },
                            total: 34
                    },
                    'total': 34
            },
        u'type': u'journal', 
        u'bra': 34,
    }"
    >>> 

Recovering a journal accesses via GET method::

    Python 2.6.6 (r266:84374, Aug 31 2010, 11:00:51) 
    [GCC 4.0.1 (Apple Inc. build 5493)] on darwin
    Type "help", "copyright", "credits" or "license" for more information.
    >>> import urllib2
    >>> 
    >>> urllib2.urlopen("http://localhost:8888/api/v1/journal?code=1981-6723").read()
    "{
        u'code': u'1981-6723', 
        u'_id': ObjectId('50295ae0714e86b6a66ace04'), 
        u'journal': 
            {
                'y2012':
                    {
                        'm08': 
                            {
                                'd16': 7,
                                'd13': 27, 
                            },
                            total: 34
                    },
                    'total': 34
            },
        u'type': u'journal', 
        u'bra': 34,
    }"
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
        u'journal': 
            {
                'y2012':
                    {
                        'm08': 
                            {
                                'd16': 7,
                                'd13': 27, 
                            },
                            total: 34
                    },
                    'total': 34
            }
        u'type': u'journal', 
        u'bra': 34,
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
    {
        u'code': u'1981-6723', 
        u'_id': ObjectId('50295ae0714e86b6a66ace04'), 
        u'journal': 
            {
                'y2012':
                    {
                        'm08': 
                            {
                                'd16': 7,
                                'd13': 26, 
                            },
                            total: 33
                    },
                    'total': 33 
            },
        u'type': u'journal', 
        u'bra': 33,    }

    :ratchet fabiobatalha$ php test_post.php 
    
    :ratchet fabiobatalha$ php test_get.php
    {
        u'code': u'1981-6723', 
        u'_id': ObjectId('50295ae0714e86b6a66ace04'), 
        u'journal': 
            {
                'y2012':
                    {
                        'm08': 
                            {
                                'd16': 7,
                                'd13': 27, 
                            },
                            total: 34
                    },
                    'total': 34
            },
        u'type': u'journal', 
        u'bra': 34,
    }

Recovering a journal accesses via GET method::

    test_get.php
    <?php
    print file_get_contents("http://localhost:8888/api/v1/journal?code=1981-6723");
    ?>

    :ratchet fabiobatalha$ php test_get.php
    {
        u'code': u'1981-6723', 
        u'_id': ObjectId('50295ae0714e86b6a66ace04'), 
        u'journal': 
            {
                'y2012':
                    {
                        'm08': 
                            {
                                'd16': 7,
                                'd13': 27, 
                            },
                            total: 34
                    },
                    'total': 34
            },
        u'type': u'journal', 
        u'bra': 34,
    }
