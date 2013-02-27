=============
API Reference
=============

    This tool will mainly work as an API to register access stats and to recover statistics from journals, issues and articles.

POST Services
=============

    The post http method will be used to register the access stats.

--------------------------
Register an article access
--------------------------

    **resource:** /api/v1/article

Parameters
----------

    **code:** any code that uniquely represents an article

    **journal:** any code that uniquely represents a journal

    **issue:**  any code that uniquely represents an issue

    **region:** 3 letters iso country code

Query Sample
------------

    /api/v1/article?code=41469714ad84732ad79ffb7ccae00fc5&region=bra&journal=1981-6723&issue=a891dc829a40e104c112fd3b0f100e25

---------------------
Register a PDF access
---------------------

    **resource:** /api/v1/pdf

Parameters
----------

    **code:** any code that uniquely represents an article

    **journal:** any code that uniquely represents a journal

    **issue:**  any code that uniquely represents an issue

    **region:** 3 letters iso country code

    **access_date:** access date iso format (YYYY-MM-DD)

Query Sample
------------

    /api/v1/pdf?code=41469714ad84732ad79ffb7ccae00fc5&region=bra&journal=1981-6723&issue=a891dc829a40e104c112fd3b0f100e25&access_date=2012-08-09

------------------------
Register an issue access
------------------------

    **resource:** /api/v1/issue

Parameters
----------

    **code:** any code that uniquely represents an article

    **journal:** any code that uniquely represents a journal

    **region:** 3 letters iso country code


Query Sample
------------

    /api/v1/issue?code=a891dc829a40e104c112fd3b0f100e25&region=bra&journal=1981-6723

-------------------------
Register a journal access
-------------------------

    **resource:** /api/v1/journal

Parameters
----------

    **code:** latindex Journal ID

    **region:** 3 letters iso country code (http://en.wikipedia.org/wiki/ISO_3166-1)

Query Sample
------------

    /api/v1/journal?code=1981-6723&region=bra


---------------------
Bulk Article Accesses 
---------------------

    **resource:** /api/v1/article/bulk

Parameters
----------

    **data:** Accesses from a specific document in JSON format.::

        {
            "code": "S0034-89102009000400003",
            "journal": "0034-8910",
            "issue": "0034-891020090004",
            "article.y2011.m10.d01": 100,
            "article.y2011.m10.d02": 100,
            "article.y2011.m10.d03": 100,
            "article.y2012.m11.d01": 10,
            "article.y2012.m11.a02": 10,
            "article.y2012.m11.a03": 10,
            "article.y2012.m10.total": 300,
            "article.y2012.m11.total": 30,
            "article.y2012.total": 330,
            "total": 330,
            "bra": 200,
            "mex": 100,
            "arg": 10,
            "col": 20
        }

Query Sample
------------

    /api/v1/article/bulk?data=<JSON DATA>


------------------
Bulk PDF Downloads 
------------------

    **resource:** /api/v1/pdf/bulk

Parameters
----------

    **data:** Accesses from a specific document in JSON format.::

        {
            "code": "S0034-89102009000400003",
            "journal": "0034-8910",
            "issue": "0034-891020090004",
            "download.y2011.m10.d01": 100,
            "download.y2011.m10.d02": 100,
            "download.y2011.m10.d03": 100,
            "download.y2012.m11.d01": 10,
            "download.y2012.m11.a02": 10,
            "download.y2012.m11.a03": 10,
            "download.y2012.m10.total": 300,
            "download.y2012.m11.total": 30,
            "download.y2012.total": 330,
            "total": 330,
            "bra": 200,
            "mex": 100,
            "arg": 10,
            "col": 20
        }

Query Sample
------------

    /api/v1/article/bulk?data=<JSON DATA>

-------------------
Bulk Issue Accesses 
-------------------

    **resource:** /api/v1/issue/bulk

Parameters
----------

    **data:** Accesses from a specific document in JSON format.::

        {
            "code": "S0034-891020090004",
            "journal": "0034-8910",
            "issue.y2011.m10.d01": 100,
            "issue.y2011.m10.d02": 100,
            "issue.y2011.m10.d03": 100,
            "issue.y2012.m11.d01": 10,
            "issue.y2012.m11.a02": 10,
            "issue.y2012.m11.a03": 10,
            "issue.y2012.m10.total": 300,
            "issue.y2012.m11.total": 30,
            "issue.y2012.total": 330,
            "total": 330,
            "bra": 200,
            "mex": 100,
            "arg": 10,
            "col": 20
        }

Query Sample
------------

    /api/v1/issue/bulk?data=<JSON DATA>

---------------------
Bulk Journal Accesses 
---------------------

    **resource:** /api/v1/journal/bulk

Parameters
----------

    **data:** Accesses from a specific document in JSON format.::

        {
            "code": "0034-8910",
            "journal.y2011.m10.d01": 100,
            "journal.y2011.m10.d02": 100,
            "journal.y2011.m10.d03": 100,
            "journal.y2012.m11.d01": 10,
            "journal.y2012.m11.a02": 10,
            "journal.y2012.m11.a03": 10,
            "journal.y2012.m10.total": 300,
            "journal.y2012.m11.total": 30,
            "journal.y2012.total": 330,
            "total": 330,
            "bra": 200,
            "mex": 100,
            "arg": 10,
            "col": 20
        }

Query Sample
------------

    /api/v1/journal/bulk?data=<JSON DATA>

GET Services
============

    The GET HTTP method will be used to request the access stats.

----------------------
Checking Resource Type
----------------------

    **resource:** /

Query Sample
------------

    /

    Response Sample for **local** resource::

        {
            Another Ratchet Local Resource
        }

    Response Sample for **global** resource::

        {
            Another Ratchet Global Resource
        }

-------------------------------
Cheking the available resources
-------------------------------

    alert::

        Available when the api is configured as a Global Resource

    **resource:** /api/v1/resources

Query Sample
------------

    /api/v1/resources

    Response Sample::

        {
            'http://127.0.0.1:8880/': 'online', 
            'http://127.0.0.1:8890/': 'online', 
            'http://127.0.0.1:8860/': 'online', 
            'http://127.0.0.1:8870/': 'offline'
        }


--------------------------------
Retrieve acceses from an article
--------------------------------

    **resource:** /api/v1/article

Parameters
----------

    **code:** any code that uniquely represents an article

Query Sample
------------

    /api/v1/article?code=41469714ad84732ad79ffb7ccae00fc5

-------------------------------
Retrieve accesses from an issue
-------------------------------

    **resource:** /api/v1/issue

Parameters
----------

    **code:** any code that uniquely represents an issue

Query Sample
------------

    /api/v1/issue?code=a891dc829a40e104c112fd3b0f100e25

--------------------------------
Retrieve accesses from a journal
--------------------------------

    **resource:** /api/v1/journal

Parameters
----------

    **code:** latindex Journal ID

Query Sample
------------

    /api/v1/journal?code=1981-6723
