============
Architecture
============

Overview
========

.. image:: images/architecture.png

Description
===========

**Resource A and Resource B**

Any instance that have their own statistics context. They could be identified as "local resources"

**Global Resource**

An instance responsible to harvest the statistics from the "local resources" and create a Global accesses cosolidating accesses from more than one "local resource" into on centralized database.

To start Ratchet as a Global resource you must specify a text file with a list of the available local resources that will be fetched by the Global resouce.

For more information run::

    python ratchet --help