from pyramid.config import Configurator
from scieloweb.resources import Root

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    zcml_file = settings.get('configure_zcml', 'configure.zcml')
    config = Configurator(root_factory=Root, settings=settings)
    config.include('pyramid_zcml')
    config.load_zcml(zcml_file)
    return config.make_wsgi_app()

