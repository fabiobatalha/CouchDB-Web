from pyramid.config import Configurator
import pyramid_zcml
from scieloweb import settings as app_settings

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    config.include(pyramid_zcml)
    config.load_zcml('configure.zcml')

    if app_settings.DEBUG:
        config.add_static_view(name='static', path='static')

    return config.make_wsgi_app()