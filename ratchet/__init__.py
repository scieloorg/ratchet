import urlparse

import pymongo

from pyramid.config import Configurator


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)

    db_url = urlparse.urlparse(settings['mongo_uri'])

    config.registry.db = pymongo.Connection(
        host=db_url.hostname,
        port=db_url.port
    )

    db = config.registry.db[db_url.path[1:]]
    if db_url.username and db_url.password:
        db.authenticate(db_url.username, db_url.password)

    def add_db(request):
        return db['accesses']

    config.include('pyramid_chameleon')
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('index', '/')
    config.add_route('endpoints', '/api/v1/')
    config.add_route('general', '/api/v1/general/')
    config.add_route('general_bulk', '/api/v1/general/bulk/')
    config.add_route('journals', '/api/v1/journals/')
    config.add_route('journal', '/api/v1/journals/{code}/')
    config.add_request_method(add_db, 'db', reify=True)
    config.scan()

    return config.make_wsgi_app()
