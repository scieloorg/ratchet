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
            "2011-10-01": 100,
            "2011-10-02": 100,
            "2011-10-03": 100,
            "2012-11-01": 10,
            "2012-11-02": 10,
            "2012-11-03": 10,
            "2012-10": 300,
            "2012-11": 30,
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
            "2011-10-01": 100,
            "2011-10-02": 100,
            "2011-10-03": 100,
            "2012-11-01": 10,
            "2012-11-02": 10,
            "2012-11-03": 10,
            "2012-10": 300,
            "2012-11": 30,
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
            "2011-10-01": 100,
            "2011-10-02": 100,
            "2011-10-03": 100,
            "2012-11-01": 10,
            "2012-11-02": 10,
            "2012-11-03": 10,
            "2012-10": 300,
            "2012-11": 30,
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

    /api/v1/issue?code=1981-6723
