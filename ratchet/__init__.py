import urlparse

from pyramid.config import Configurator

from ratchet import controller

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)

    def add_controller(request):
        return controller.Ratchet(settings['mongo_uri'])

    config.include('pyramid_chameleon')
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('index', '/')
    config.add_route('endpoints', '/api/v1/')
    config.add_route('general', '/api/v1/general/')
    config.add_route('general_bulk', '/api/v1/general/bulk/')
    config.add_route('journals', '/api/v1/journals/')
    config.add_route('journal', '/api/v1/journals/{code}/')
    config.add_route('issues', '/api/v1/issues/')
    config.add_route('issue', '/api/v1/issues/{code}/')
    config.add_route('articles', '/api/v1/articles/')
    config.add_route('article', '/api/v1/articles/{code}/')
    config.add_request_method(add_controller, 'controller', reify=True)
    config.scan()

    return config.make_wsgi_app()
