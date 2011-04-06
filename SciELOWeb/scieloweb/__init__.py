from pyramid.config import Configurator
from scieloweb.resources import Root
from pyramid.events import NewRequest, NewResponse
from pyramid.i18n import get_localizer 

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    zcml_file = settings.get('configure_zcml', 'configure.zcml')
    config = Configurator(root_factory=Root, settings=settings)
    config.include('pyramid_zcml')
    config.load_zcml(zcml_file)
    
    config.add_translation_dirs('scieloweb:locale/')
    config.set_locale_negotiator(custom_locale_negotiator)
    
    return config.make_wsgi_app()


def custom_locale_negotiator(request):
    settings = request.registry.settings
    locale = ''

    if 'language' in request.params:
        locale = request.params['language']
    elif 'language' in request.cookies.keys():
        locale = request.cookies['language']

    if locale not in settings['available_languages'].split():
        locale = settings['default_locale_name']

    return locale