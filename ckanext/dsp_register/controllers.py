# -*- coding: utf-8 -*-

__author__ = 'nispc'

import ckan.plugins.toolkit as toolkit

from ckan.plugins.toolkit import request, _
from ckan.controllers.admin import AdminController
import pylons.config as config
import urllib2
import urllib
import json

import requests

class MainController(AdminController):
    def __before__(self, action, **env):
        AdminController.__before__(self, action, **env)

        self.apikey = config.get('ckanext.dsp_register.apikey', None)
        self.username = config.get('ckanext.dsp_register.dsp_id', None)
        self.company = config.get('ckanext.dsp_register.company', None)
        self.site_url = config.get('ckanext.dsp_register.site_url', None)
        self.phone = config.get('ckanext.dsp_register.phone', None)
        self.email = config.get('ckanext.dsp_register.email', None)
        self.note = config.get('ckanext.dsp_register.note', None)
        self.uuid = config.get('ckanext.dsp_register.uuid', None)

    def register(self):
        data = request.POST
        if data:
            errors = {}

            email = request.params['email']
            company = request.params['company']
            phone = request.params['phone']
            note = request.params['note']
            site_url = request.params['site_url']

            data={
                    'email': email,
                    'phone': phone,
                    'company': company,
                    'note': note,
                    'site_url': site_url,
                    'uuid': self.uuid
            }


            if not all([email, company, phone, site_url]):
                if not email:
                    errors['email'] = [u'此為必填項目']
                if not company:
                    errors['company'] = [u'此為必填項目']
                if not site_url:
                    errors['site_url'] = [u'此為必填項目']
                if not phone:
                    errors['phone'] = [u'此為必填項目']

                return toolkit.render('yaka-admin/yaka-register.html', extra_vars={'data': data, 'errors': errors})


            try:
                res = requests.post('http://data.dsp.im/platforms', data=data)

                toolkit.get_action('config_option_update')({}, {
                    'ckanext.dsp_register.apikey': self.apikey,
                    'ckanext.dsp_register.dsp_id': self.username,
                    'ckanext.dsp_register.company': data['company'],
                    'ckanext.dsp_register.site_url': data['site_url'],
                    'ckanext.dsp_register.phone': data['phone'],
                    'ckanext.dsp_register.email': data['email'],
                    'ckanext.dsp_register.note': data['note'],
                    'ckanext.dsp_register.uuid': res.content

                })

                return toolkit.redirect_to('yaka-register')

            except Exception as e:
                return e

        else:
            data = {
                'company': self.company,
                'site_url': self.site_url,
                'phone': self.phone,
                'email': self.email,
                'note': self.note
            }

            if not self.apikey or not self.username:
                return toolkit.render('yaka-admin/yaka-register.html',
                                      extra_vars={'data': {}, 'errors': {}, 'notConnected': True})

            if all((self.company, self.site_url, self.phone, self.email)):
                registered = True
            else:
                registered = False

            return toolkit.render('yaka-admin/yaka-register.html', extra_vars={'data': data, 'errors': {}, 'Registered': registered})

    def send_and_active(self):
        pass
        # errors = {}
        #
        # email = request.params['email']
        # company = request.params['company']
        # phone = request.params['phone']
        # note = request.params['note']
        # site_url = request.params['site_url']
        #
        # data={
        #         'email': email,
        #         'phone': phone,
        #         'company': company,
        #         'note': note,
        #         'site_url': site_url,
        #         'uuid': self.uuid
        # }
        #
        #
        # if not all([email, company, phone, site_url]):
        #     if not email:
        #         errors['email'] = [u'此為必填項目']
        #     if not company:
        #         errors['company'] = [u'此為必填項目']
        #     if not company:
        #         errors['phone'] = [u'此為必填項目']
        #     if not company:
        #         errors['site_url'] = [u'此為必填項目']
        #
        #     return toolkit.render('yaka-admin/yaka-register.html', extra_vars={'data': data, 'errors': errors})
        #
        #
        # try:
        #     res = requests.post('http://data.dsp.im/platforms', data=data)
        #
        #     toolkit.get_action('config_option_update')({}, {
        #         'ckanext.dsp_register.apikey': self.apikey,
        #         'ckanext.dsp_register.dsp_id': self.username,
        #         'ckanext.dsp_register.company': data['company'],
        #         'ckanext.dsp_register.site_url': data['site_url'],
        #         'ckanext.dsp_register.phone': data['phone'],
        #         'ckanext.dsp_register.email': data['email'],
        #         'ckanext.dsp_register.note': data['note'],
        #         'ckanext.dsp_register.uuid': res.content
        #
        #     })
        #
        #     return toolkit.redirect_to('yaka-register')
        #
        # except Exception as e:
        #     return e

    def dsp_connect(self):
        data = request.POST
        error_summary = {}
        errors = {}

        print data

        if self.apikey and self.username:
            if data:
                return toolkit.redirect_to('yaka-register')
            else:
                data = {
                    'api_key': self.apikey,
                    'username': self.username
                }

                return toolkit.render('yaka-admin/dsp-connect.html',
                              extra_vars={'data': data, 'errors': {}, 'Connected': True})


        else:
            if 'save' in data:
                if not data['username']:
                    errors['username'] = [u'此為必填項目']
                if not data['api_key']:
                    errors['api_key'] = [u'此為必填項目']

                if data['username'] and data['api_key']:
                    data_string = urllib.quote(json.dumps({
                        'id': data['username']
                    }))

                    user_show_url = 'http://data.dsp.im/api/3/action/user_show'
                    request_ = urllib2.Request(user_show_url, headers={"Authorization": data['api_key']})
                    try:
                        response = urllib2.urlopen(request_, data_string)
                    except Exception as e:
                        error_summary[u'認證錯誤'] = u'使用者名稱或API Key錯誤'
                        return toolkit.render('yaka-admin/dsp-connect.html',
                                    extra_vars={'data': data, 'errors': errors, 'error_summary': error_summary})

                    response =  json.loads(response.read())
                    if response['success']:
                        if 'apikey' in response['result']:
                            toolkit.get_action('config_option_update')({}, {
                                'ckanext.dsp_register.dsp_id': data['username'],
                                'ckanext.dsp_register.apikey': data['api_key'],
                                'ckanext.dsp_register.company': self.company,
                                'ckanext.dsp_register.site_url': self.site_url,
                                'ckanext.dsp_register.phone': self.phone,
                                'ckanext.dsp_register.email': self.email,
                                'ckanext.dsp_register.note': self.note,
                                'ckanext.dsp_register.uuid': self.uuid
                            })

                            return toolkit.redirect_to('yaka-register')

                        else:
                            error_summary[u'認證錯誤'] = u'使用者名稱或API Key錯誤'

                            return toolkit.render('yaka-admin/dsp-connect.html',
                                    extra_vars={'data': data, 'errors': errors, 'error_summary': error_summary})

        return toolkit.render('yaka-admin/dsp-connect.html',
                              extra_vars={'data': {}, 'errors': {}})


    def dsp_disconnect(self):
        toolkit.get_action('config_option_update')({}, {
            'ckanext.dsp_register.dsp_id': '',
            'ckanext.dsp_register.apikey': '',
            'ckanext.dsp_register.company': '',
            'ckanext.dsp_register.site_url': '',
            'ckanext.dsp_register.phone': '',
            'ckanext.dsp_register.email': '',
            'ckanext.dsp_register.note': '',
            'ckanext.dsp_register.uuid': self.uuid
        })

        return toolkit.redirect_to('dsp-connect')

    def dsp_register(self):
        return toolkit.render('yaka-admin/dsp-register.html',  extra_vars={'data': {}, 'errors': {}})

    def home(self):
        return toolkit.render('yaka-admin/home.html')

