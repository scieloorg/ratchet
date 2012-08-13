=============
API Reference
=============

This tool will mainly work with an API to register access stats and to recover statistics from journals, issues and articles.

POST Services
=============

The post http method will be used to register the access stats.

-------
Article
-------

**resource:** /api/v1/article

**Parameters**

**code:** md5(article_title_english + 1st author name + 1s author surname)

**journal:** journal_id - Latindex Journal ID

**issue:** md5(journal_id + year + volume + number)

**region:** 3 letters iso country code

Query Sample
------------

For this sample we are using the ISSN as journal id instead of the Latindex Journal ID.

The code MD5 string was generated for physicalandsensoryevaluationofwheatandricebrancookiesvivianfeddern

The issue MD5 string was generated for 1981-67232011001400004

/api/v1/article?code=41469714ad84732ad79ffb7ccae00fc5&region=bra&journal=1981-6723&issue=a891dc829a40e104c112fd3b0f100e25

---
PDF
---

**resource:** /api/v1/pdf

**Parameters**

**code:** md5(article_title_english + 1st author name + 1s author surname)

**journal:** Latindex Journal ID

**issue:** md5(latindex journal id + year + volume + number)

**region:** 3 letters iso country code 

**access_date:** access date iso format (YYYY-MM-DD)

Query Sample
------------

For this sample we are using the ISSN as journal id instead of the Latindex Journal ID.

The code MD5 string was generated for physicalandsensoryevaluationofwheatandricebrancookiesvivianfeddern

The issue MD5 string was generated for 1981-67232011001400004

/api/v1/pdf?code=41469714ad84732ad79ffb7ccae00fc5&region=bra&journal=1981-6723&issue=a891dc829a40e104c112fd3b0f100e25&access_date=2012-08-09

-----
Issue
-----

**resource:** /api/v1/issue

**Parameters**

**code:** md5(latindex journal id + year + volume + number + S for supplement)

**journal:** Latindex Journal ID

**region:** 3 letters iso country code 

Query Sample
------------

For this sample we are using the ISSN as journal id instead of the Latindex Journal ID.

**Registering access to an ordinary issue**

The MD5 string was generated for 1981-67232011001400004

/api/v1/issue?code=a891dc829a40e104c112fd3b0f100e25&region=bra&journal=1981-6723

**Registering access to an supplement issue**

The MD5 string was generated for 1981-67232011001400004S

/api/v1/issue?code=464071f8104ff633a7c5359d6e29f1c8&region=bra&journal=1981-6723

-------
Journal
-------

**resource:** /api/v1/journal

**Parameters**

**code:** latindex Journal ID

**region:** 3 letters iso country code (http://en.wikipedia.org/wiki/ISO_3166-1)

Query Sample
------------

/api/v1/journal?code=1981-6723&region=bra


GET Services
============

The GET HTTP method will be used to request the access stats.

-------
Article
-------

**resource:** /api/v1/article

**Parameters**

**code:** md5(article_title_english + 1st author name + 1s author surname)

Query Sample
------------

The code MD5 string was generated for physicalandsensoryevaluationofwheatandricebrancookiesvivianfeddern

/api/v1/article?code=41469714ad84732ad79ffb7ccae00fc5

-----
Issue
-----

**resource:** /api/v1/issue

**code:** md5(journal_id + year + volume + number)

Query Sample
------------

For this sample we are using the ISSN as journal id instead of the Latindex Journal ID.

The MD5 string was generated for 1981-67232011001400004

/api/v1/issue?code=a891dc829a40e104c112fd3b0f100e25

-------
Journal
-------

**resource:** /api/v1/journal

**Parameters**

**code:** latindex Journal ID

Query Sample
------------

For this sample we are using the ISSN as journal id instead of the Latindex Journal ID.

The MD5 string was generated for 1981-67232011001400004

/api/v1/issue?code=1981-6723