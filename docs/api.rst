=============
API Reference
=============

This tool will mainly work with an API to register access stats and to recover statistics from journals, issues and articles.

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


GET Services
============

The GET HTTP method will be used to request the access stats.

-------------------------------
Retrieve acceses from an article
-------------------------------

    **resource:** /api/v1/article

    Parameters
    ----------

    **code:** md5(article_title_english + 1st author name + 1s author surname)

    Query Sample
    ------------

    The code MD5 string was generated for physicalandsensoryevaluationofwheatandricebrancookiesvivianfeddern

        /api/v1/article?code=41469714ad84732ad79ffb7ccae00fc5

-------------------------------
Retrieve accesses from an issue
-------------------------------

    **resource:** /api/v1/issue

    **code:** md5(journal_id + year + volume + number)

    Query Sample
    ------------

    For this sample we are using the ISSN as journal id instead of the Latindex Journal ID.

    The MD5 string was generated for 1981-67232011001400004

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

    For this sample we are using the ISSN as journal id instead of the Latindex Journal ID.

    The MD5 string was generated for 1981-67232011001400004

        /api/v1/issue?code=1981-6723