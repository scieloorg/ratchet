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

    Creating a virtual environment::

        cd ratchet
        virtualenv --no-site-packages ratchet-env
        source ratchet-env/bin/activate

Installing the Applications
---------------------------

    Installing the requirements::
    
        source ratchet-env/bin/activate
        pip install -r requirements.txt

Installing and Starting MongoDB
-------------------------------

MongoDB could be installed at the virtual environment ratchet-env if it is not installed in the server

**Installing MongoDB**::

    cd ratchet-env/bin
    wget http://fastdl.mongodb.org/linux/mongodb-linux-x86_64-2.0.7.tgz
    tar -xvf mongodb-linux-x86_64-2.0.7.tgz
    ln -s mongodb-linux-x86_64-2.0.7/bin/mongod

**Starting MongoDB**

    Just run the script!::

        ./mongodb_start.sh

Running Server
==============

    Just run::
    
        python ratchet.py

By default, the server will run at localhost:8888 with the mongoDB server at localhost:27017.

For more details about how customize the server, run::

    python ratchet.py --help
