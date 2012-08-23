Ratchet
=======

Ratchet is an access statistics tool made over Tornado Framework plus MongoDB. This tool was made
thinking in create a common and easy to use tool/api to register accesses made to scientific 
publications, considering the accesses to the Journals, Issues and articles level.

Downloading Ratchet
===================

**Clonning from Github**

    git clone git://github.com/scieloorg/ratchet.git

**Downloading**

    https://github.com/scieloorg/ratchet/tags

How to Install
==============

Compatible with: 

 * OSX (Tested)
 * Linux (Tested)
 * Windows (Maybe! Good luck! Who knows?)

Pre-requirements
----------------

* virtualenv (http://www.virtualenv.org/en/latest/index.html#installation)
* pip (http://www.pip-installer.org/en/latest/installing.html)
* mongodb (http://www.mongodb.org/downloads)
* Tornado (http://www.tornadoweb.org/)

Creating Virtual Environment
----------------------------

    cd ratchet
    virtualenv --no-site-packages ratchet-env
    source ratchet-env/bin/activate

Installing the Applications
---------------------------

    pip install -r requirements.txt

Installing and Starting MongoDB
-------------------------------

MongoDB could be installed at the virtual environment ratchet-env if it is not installed in the server

**Installing MongoDB**

    cd ratchet-env/bin
    wget http://fastdl.mongodb.org/linux/mongodb-linux-x86_64-2.0.7.tgz
    tar -xvf mongodb-linux-x86_64-2.0.7.tgz
    ln -s mongodb-linux-x86_64-2.0.7/bin/mongod

**Starting MongoDB**

Just run the script!

    ./mongodb_start.sh

Running Server
==============

    python ratchet.py

By default, the server will run at localhost:8888 with the mongoDB server at localhost:27017.

For more details about how customize the server, run:

    python ratchet.py --help

Documentation
=============

All detailed documentations are available at: http://docs.scielo.org/projects/ratchet/en/latest/index.html

Use License
===========

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
