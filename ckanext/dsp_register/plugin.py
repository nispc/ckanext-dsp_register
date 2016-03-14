# -*- coding: utf-8 -*-

import pylons.config as config

import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit

def config_option_update(context, data_dict=None):
    return {'success': False, 'msg': ''}

def check_if_registered():
    # registered = config.get('ckan.dsp_register.registered', False)
    company = config.get('ckanext.dsp_register.company', None)

    if company:
        return True
    else:
        return False

class Dsp_RegisterPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.ITemplateHelpers)
    plugins.implements(plugins.IRoutes)

    # IConfigurer

    def update_config(self, config_):

        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic', 'dsp_register')
        # toolkit.add_ckan_admin_tab(config, 'yaka-register', u'註冊Yaka')

    def update_config_schema(self, schema):
        ignore_missing = toolkit.get_validator('ignore_missing')
        boolean_validator = toolkit.get_validator('boolean_validator')

        schema.update({
            'ckanext.dsp_register.dsp_id': [unicode, ignore_missing],
            'ckanext.dsp_register.apikey': [unicode, ignore_missing],
            'ckanext.dsp_register.company': [unicode, ignore_missing],
            'ckanext.dsp_register.site_url': [unicode, ignore_missing],
            'ckanext.dsp_register.phone': [unicode, ignore_missing],
            'ckanext.dsp_register.email': [unicode, ignore_missing],
            'ckanext.dsp_register.note': [unicode, ignore_missing],
            'ckanext.dsp_register.uuid': [unicode, ignore_missing],
        })

        return schema

    # IRoutes
    def before_map(self, map):
        controller = 'ckanext.dsp_register.controllers:MainController'

        map.connect('yaka-admin', '/yaka-admin',
            controller=controller, action='home')

        map.connect('yaka-register', '/yaka-admin/yaka-register',
            controller=controller, action='register')

        map.connect('dsp-connect', '/yaka-admin/connect',
            controller=controller, action='dsp_connect')

        map.connect('dsp-register', '/yaka-admin/dsp-register',
            controller=controller, action='dsp_register')

        map.connect('dsp-disconnect', '/yaka-admin/dsp_disconnect',
            controller=controller, action='dsp_disconnect')

        map.connect('submit', '/yaka-admin/yaka-register/submit',
            controller=controller, action='send_and_active')

    #
    #     map.connect('dsp-register-check', '/installation/dsp-register/check',
    #         controller=controller, action='check')
    #
    #     map.connect('dsp-register-uncheck', '/installation/dsp-register/uncheck',
    #         controller=controller, action='uncheck')
    #
        return map


    def after_map(self, map):
        return map

    def get_helpers(self):
        return {'registered': check_if_registered}
