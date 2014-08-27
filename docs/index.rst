.. Ratchet documentation master file, created by
   sphinx-quickstart on Mon Aug 13 15:57:38 2012.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Ratchet's documentation!
===================================

About
-----

Ratchet is an access statistics tool made over Tornado Framework plus MongoDB. This tool was made thinking to create a common and easy to use tool/api to register and recover accesses made to scientific publications, considering the accesses to the Journals, Issues and articles.

Motivation
----------

The main motivation in develop this tool was to create a more reliable tool that makes use of hightend technologies in the process of register and recover access statistics from websites. The motivation includes yet the focus in develop tools using technologies that make posible the contribution of the developer community considering the use of popular programing languages and the possibility to develop a webservices layer to allow user to have access to the statistics information.

Contents:

.. toctree::
   :maxdepth: 2

   architecture.rst
   concepts.rst
   api.rst
   api_samples.rst
   howtoinstall.rst
   
API Wrapper
-----------

The Ratchet RESTFul API has also a wrapper library written in python that may be used to make the harvesting of data easier.

http://scielo.readthedocs.org/projects/ratchetapipy/en/latest/

License
-------

FreeBSD 2-clause::

    Copyright (c) 2012, SciELO <scielo-dev@googlegroups.com>
    All rights reserved.

    Redistribution and use in source and binary forms, with or without modification,
    are permitted provided that the following conditions are met:

        Redistributions of source code must retain the above copyright notice,
        this list of conditions and the following disclaimer.

        Redistributions in binary form must reproduce the above copyright notice,
        this list of conditions and the following disclaimer in the documentation
        and/or other materials provided with the distribution.

    THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
    ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
    WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
    IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT,
    INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT
    NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA,
    OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
    WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
    ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY
    OF SUCH DAMAGE.

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

