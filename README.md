Ratchet
=======

Ratchet is an access statistics tool made over Tornado Framework plus MongoDB. This tool was made
thinking in create a common and easy to use tool/api to register accesses made to scientific 
publications, considering the accesses to the Journals, Issues and articles level.


How to Install
==============

Pre-requirements
----------------

* virtualenv (http://www.virtualenv.org/en/latest/index.html#installation)
* pip (http://www.pip-installer.org/en/latest/installing.html)

Creating Virtual Environment
----------------------------

code-block::

    mkdir ratched
    cd ratchet
    virtualenv --no-site-packages ratchet-env
    source ratchet-env/bin/activate
    pip install -r requirements.txt

