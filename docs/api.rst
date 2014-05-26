=============
API Reference
=============

    This tool will mainly work as an API to register access stats and to recover statistics from journals, issues and articles.

POST Services
=============

    The post http method will be used to register the access stats.

-------------------------------
Register an article html access
-------------------------------

    **resource:** /api/v1/general

Mandatory Parameters
--------------------

    **code:** any code that uniquely represents an article

    **journal:** any code that uniquely represents a journal

    **issue:**  any code that uniquely represents an issue

    **type_doc:** Must be **article**
    
    **page:** Must be **fulltext**


Optional Parameters
-------------------

    **access_date** access date iso format (YYYY-MM-DD)
    
    **region:** 3 letters iso country code

Query Sample
------------

    /api/v1/article?code=1981-67232014000100002&region=bra&journal=1981-6723&issue=1981-672320140001&type=article_doc&page=fulltext

------------------------------
Register a PDF download access
------------------------------

    **resource:** /api/v1/general

Mandatory Parameters
--------------------

    **code:** any code that uniquely represents an article

    **journal:** any code that uniquely represents a journal

    **issue:**  any code that uniquely represents an issue

    **type_doc:** Must be **article**

    **page:** Must be **download**


Optional Parameters
-------------------

    **access_date** access date iso format (YYYY-MM-DD)
    
    **region:** 3 letters iso country code


Query Sample
------------

    /api/v1/article?code=1981-67232014000100002&region=bra&journal=1981-6723&issue=1981-672320140001&type_doc=article&page=download

-------------------------------
Register a Abstract html access
-------------------------------

    **resource:** /api/v1/general

Mandatory Parameters
--------------------

    **code:** any code that uniquely represents an article

    **journal:** any code that uniquely represents a journal

    **issue:**  any code that uniquely represents an issue

    **type_doc:** Must be **article**

    **page:** Must be **abstract**


Optional Parameters
-------------------

    **access_date** access date iso format (YYYY-MM-DD)
    
    **region:** 3 letters iso country code


Query Sample
------------

    /api/v1/article?code=1981-67232014000100002&region=bra&journal=1981-6723&issue=1981-672320140001&type_doc=article&page=abstract

------------------------
Register an issue access
------------------------

    **resource:** /api/v1/general

Parameters
----------

    **code:** any code that uniquely represents an article

    **journal:** any code that uniquely represents a journal

    **type_doc:** Must be **toc**

    **page:** Must be **toc**

Optional Parameters
-------------------

    **access_date** access date iso format (YYYY-MM-DD)
    
    **region:** 3 letters iso country code


Query Sample
------------

    /api/v1/issue?code=1981-672320140001&region=bra&journal=1981-6723&type_doc=toc&page=toc

-------------------------
Register a journal access
-------------------------

    **resource:** /api/v1/general

Parameters
----------

    **code:** any code that uniquely represents a journal

    **type_doc:** Must be **journal**

    **page:** Must be **journal**

Optional Parameters
-------------------

    **access_date** access date iso format (YYYY-MM-DD)
    
    **region:** 3 letters iso country code

Query Sample
------------

    /api/v1/journal?code=1981-6723&region=bra&type_doc=journal&page=journal

---------------------
Bulk General Accesses 
---------------------

    **resource:** /api/v1/general/bulk

Parameters for pdf accesses into an article resource
-----------------------------------------------------

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
            "pdf.total": 330,
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

Parameters for abstract accesses into an article resource
---------------------------------------------------------

    **data:** Accesses from a specific document in JSON format.::

        {
            "code": "S0034-89102009000400003",
            "journal": "0034-8910",
            "issue": "0034-891020090004",
            "abstract.y2011.m10.d01": 100,
            "abstract.y2011.m10.d02": 100,
            "abstract.y2011.m10.d03": 100,
            "abstract.y2012.m11.d01": 10,
            "abstract.y2012.m11.a02": 10,
            "abstract.y2012.m11.a03": 10,
            "abstract.y2012.m10.total": 300,
            "abstract.y2012.m11.total": 30,
            "abstract.y2012.total": 330,
            "abstract.total": 330,
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

Parameters for html accesses into an article resource
-----------------------------------------------------

    **data:** Accesses from a specific document in JSON format.::

        {
            "code": "S0034-89102009000400003",
            "journal": "0034-8910",
            "issue": "0034-891020090004",
            "html.y2011.m10.d01": 100,
            "html.y2011.m10.d02": 100,
            "html.y2011.m10.d03": 100,
            "html.y2012.m11.d01": 10,
            "html.y2012.m11.a02": 10,
            "html.y2012.m11.a03": 10,
            "html.y2012.m10.total": 300,
            "html.y2012.m11.total": 30,
            "html.y2012.total": 330,
            "html.total": 330,
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

Parameters for other accesses into an article resource
------------------------------------------------------

    **data:** Accesses from a specific document in JSON format.::

        {
            "code": "S0034-89102009000400003",
            "journal": "0034-8910",
            "issue": "0034-891020090004",
            "other.y2011.m10.d01": 100,
            "other.y2011.m10.d02": 100,
            "other.y2011.m10.d03": 100,
            "other.y2012.m11.d01": 10,
            "other.y2012.m11.a02": 10,
            "other.y2012.m11.a03": 10,
            "other.y2012.m10.total": 300,
            "other.y2012.m11.total": 30,
            "other.y2012.total": 330,
            "other.total": 330,
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