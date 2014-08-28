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
            "mex.total": 110,
            "type": "article"
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
            "mex.total": 110,
            "type": "article"
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
            "mex.total": 110,
            "type": "article"
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
            "mex.total": 110,
            "type": "article"
        }

Query Sample
------------

    /api/v1/journal/bulk?data=<JSON DATA>

GET Services
============

    The GET HTTP method will be used to request the access stats.

---------------------------------------------------------
Retrieve accesses from any resource using general request
---------------------------------------------------------

    **resource:** /api/v1/general

Parameters
----------

    **code:** any document code

    or
    
    **type:** any resource type [journal, issue, article]

Query Sample
------------

    /api/v1/general?code=1981-6723

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

----------------------------------------
Retrieve accesses from journals resource
----------------------------------------

    **resource:** /api/v1/journals/

Parameters
----------

    No parameters expected

Query Sample
------------

    /api/v1/journals/

    Response sample::

        {
            meta: {
                previous: "/api/v1/journals?offset=0",
                next: "/api/v1/journals?offset=40",
                total: 334,
                limit: 20,
                offset: 20
            },
            objects: [
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
            ...
            ]
        }

-----------------------------------------------------------------
Retrieve accesses from a specific journal using journals resource
-----------------------------------------------------------------

    **resource:** /api/v1/journals/

Parameters
----------

    No parameters expected

Query Sample
------------

    /api/v1/journals/1981-6723/

    Response sample::

        {
            meta: {
                previous: null,
                next: null,
                total: 1,
                limit: 20,
                offset: 0
            },
            objects: [
                {
                    "code": "1981-6723", 
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
            ]
        }

--------------------------------------
Retrieve accesses from issues resource
--------------------------------------

    **resource:** /api/v1/issues/

Parameters
----------

    No parameters expected

Query Sample
------------

    /api/v1/issues/

    Response sample::

        {
            meta: {
                previous: "/api/v1/journals?offset=0",
                next: "/api/v1/journals?offset=40",
                total: 334,
                limit: 20,
                offset: 20
            },
            objects: [
                {
                    "code": "1575-18130004", 
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
            ...
            ]
        }

-------------------------------------------------------------
Retrieve accesses from a specific issue using issues resource
-------------------------------------------------------------

    **resource:** /api/v1/issues/

Parameters
----------

    No parameters expected

Query Sample
------------

    /api/v1/issues/1575-18130004/

    Response sample::

        {
            meta: {
                previous: null,
                next: null,
                total: 1,
                limit: 20,
                offset: 0
            },
            objects: [
                {
                    "code": "1981-67230004", 
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
            ]
        }

----------------------------------------
Retrieve accesses from articles resource
----------------------------------------

    **resource:** /api/v1/articles/

Parameters
----------

    No parameters expected

Query Sample
------------

    /api/v1/articles/

    Response sample::

        {
            meta: {
                previous: "/api/v1/journals?offset=0",
                next: "/api/v1/journals?offset=40",
                total: 334,
                limit: 20,
                offset: 20
            },
            objects: [
                {
                    "code": "S1575-1813000400005", 
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
            ...
            ]
        }

-----------------------------------------------------------------
Retrieve accesses from a specific article using articles resource
-----------------------------------------------------------------

    **resource:** /api/v1/articles/

Parameters
----------

    No parameters expected

Query Sample
------------

    /api/v1/articles/1575-1813000400005/

    Response sample::

        {
            meta: {
                previous: null,
                next: null,
                total: 1,
                limit: 20,
                offset: 0
            },
            objects: [
                {
                    "code": "1981-67230004", 
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
            ]
        }