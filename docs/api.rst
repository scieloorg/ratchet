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

Mandatory Parameters
--------------------

    **code:** any code that uniquely represents an article

    **journal:** any code that uniquely represents a journal

    **issue:**  any code that uniquely represents an issue

Optional Parameters
-------------------

    **access_date** access date iso format (YYYY-MM-DD)
    
    **region:** 3 letters iso country code

Query Sample
------------

    /api/v1/article?code=41469714ad84732ad79ffb7ccae00fc5&region=bra&journal=1981-6723&issue=a891dc829a40e104c112fd3b0f100e25

---------------------
Register a PDF access
---------------------

    **resource:** /api/v1/pdf

Mandatory Parameters
--------------------

    **code:** any code that uniquely represents an article

    **journal:** any code that uniquely represents a journal

    **issue:**  any code that uniquely represents an issue


Optional Parameters
-------------------

    **access_date** access date iso format (YYYY-MM-DD)
    
    **region:** 3 letters iso country code


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

Optional Parameters
-------------------

    **access_date** access date iso format (YYYY-MM-DD)
    
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

Optional Parameters
-------------------

    **access_date** access date iso format (YYYY-MM-DD)
    
    **region:** 3 letters iso country code

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
            "bra.y2012.m11.a01": 20,
            "bra.y2012.m11.a02": 200,
            "bra.y2012.m11.total": 220,
            "bra.y2012.total": 220,
            "bra.total": 220,
            "mex.y2012.m11.a01": 10,
            "mex.y2012.m11.a02": 110,
            "mex.y2012.m11.total": 110,
            "mex.y2012.total": 110,
            "mex.total": 110
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
            "pdf.y2011.m10.d01": 100,
            "pdf.y2011.m10.d02": 100,
            "pdf.y2011.m10.d03": 100,
            "pdf.y2012.m11.d01": 10,
            "pdf.y2012.m11.a02": 10,
            "pdf.y2012.m11.a03": 10,
            "pdf.y2012.m10.total": 300,
            "pdf.y2012.m11.total": 30,
            "pdf.y2012.total": 330,
            "total": 330,
            "bra.y2012.m11.a01": 20,
            "bra.y2012.m11.a02": 200,
            "bra.y2012.m11.total": 220,
            "bra.y2012.total": 220,
            "bra.total": 220,
            "mex.y2012.m11.a01": 10,
            "mex.y2012.m11.a02": 110,
            "mex.y2012.m11.total": 110,
            "mex.y2012.total": 110,
            "mex.total": 110
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
            "bra.y2012.m11.a01": 20,
            "bra.y2012.m11.a02": 200,
            "bra.y2012.m11.total": 220,
            "bra.y2012.total": 220,
            "bra.total": 220,
            "mex.y2012.m11.a01": 10,
            "mex.y2012.m11.a02": 110,
            "mex.y2012.m11.total": 110,
            "mex.y2012.total": 110,
            "mex.total": 110
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
            "bra.y2012.m11.a01": 20,
            "bra.y2012.m11.a02": 200,
            "bra.y2012.m11.total": 220,
            "bra.y2012.total": 220,
            "bra.total": 220,
            "mex.y2012.m11.a01": 10,
            "mex.y2012.m11.a02": 110,
            "mex.y2012.m11.total": 110,
            "mex.y2012.total": 110,
            "mex.total": 110
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

    Response sample::

    {
        "code": "1575-18132006000600004", 
        "type": "article", 
        "pdf": {
            "y2011": {
                "total": 2, 
                "m01": {
                    "d15": 2, 
                    "total": 2
                }
            }
        }, 
        "journal": "1575-1813",
        "total": 2,
        "issue": "1575-181320060006"
    }

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

    Response sample::

    {
        "total": 17,
        "type": "issue",
        "journal": "0102-311X",
        "code": "0102-311X19870004",
        "issue": {
            "y2011": {
                "m04": {
                    "d07": 1, 
                    "total": 1
                }, 
                "total": 17,
                "m02": {
                    "total": 3,
                    "d23": 1, 
                    "d17": 1, 
                    "d13": 1
                },
                "m03": {
                    "d14": 1,
                    "d11": 1,
                    "d12": 1,
                    "d13": 1,
                    "d21": 1,
                    "total": 9,
                    "d26": 4
                }, 
                "m01": {
                    "d14": 1,
                    "d15": 1,
                    "total": 4,
                    "d25": 1,
                    "d31": 1
                }
            }
        }
    }

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

    Response sample::

    {
        "code": "1575-1813", 
        "y2011": {
            "total": 78, 
            "m01": {
                "d15": 78, 
                "total": 78
            }
        }, 
        "sci_pdf": {
            "y2011": {
                "total": 78, 
                "m01": {
                    "d15": 78, 
                    "total": 78
                }
            }
        }
    }

---------------------------------------------------------
Retrieve accesses from any document using general request
---------------------------------------------------------

    **resource:** /api/v1/general

Parameters
----------

    **code:** any document code

    or
    
    **type:** any document type [journal, issue, article]

Query Sample
------------

    /api/v1/journal?code=1981-6723

    Response sample::

    {
        "code": "1575-1813", 
        "y2011": {
            "total": 78, 
            "m01": {
                "d15": 78, 
                "total": 78
            }
        }, 
        "sci_pdf": {
            "y2011": {
                "total": 78, 
                "m01": {
                    "d15": 78, 
                    "total": 78
                }
            }
        }
    }