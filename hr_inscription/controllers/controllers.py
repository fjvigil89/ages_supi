# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import logging
import json
from odoo import http, _
from odoo.addons.auth_signup.models.res_users import SignupError
from odoo.addons.web.controllers.main import ensure_db, Home
from odoo.exceptions import UserError
from odoo.http import request
from datetime import datetime, date
from odoo import http, _, exceptions

from .serializers import Serializer
from .exceptions import QueryFormatError

from odoo.tools.image import image_data_uri

_logger = logging.getLogger(__name__)

from odoo import http

from odoo.http import request


def error_response(error, msg):
    return {
        "jsonrpc": "2.0",
        "id": None,
        "error": {
            "code": 200,
            "message": msg,
            "data": {
                "name": str(error),
                "debug": "",
                "message": msg,
                "arguments": list(error.args),
                "exception_type": type(error).__name__
            }
        }
    }


class AuthRegisterHome(Home):

    @http.route('/api/restart_password', type='json', auth='public', website=True, sitemap=False)
    def web_reset_password(self, *args, **kw):
        qcontext = self.get_auth_signup_qcontext()

        if 'error' not in qcontext and request.httprequest.method == 'POST':
            try:
                login = qcontext['data'].get('login')
                assert login, _("No login provided.")
                _logger.info(
                    "Password reset attempt for <%s> by user <%s> from %s",
                    login, request.env.user.login, request.httprequest.remote_addr)
                request.env['res.users'].sudo().reset_password(login)
                qcontext['message'] = _("An email has been sent with credentials to reset your password")
                return {
                    "jsonrpc": "2.0",
                    "id": login,
                    "data": {
                        "code": 200,
                        "message": "An email has been sent with credentials to reset your password",

                    }
                }
            except UserError as e:
                return {
                    "jsonrpc": "2.0",
                    # "id": login,
                    "data": {
                        "code": 200,
                        "message": e,

                    }
                }
            except SignupError:
                qcontext['error'] = _("Could not reset your password")
                _logger.exception('error when resetting password')
            except Exception as e:
                qcontext['error'] = str(e)
                return {
                    "jsonrpc": "2.0",
                    # "id": login,
                    "data": {
                        "code": 403,
                        "message": e,

                    }
                }

    @http.route('/api/register_inscription', type='json', auth='public', website=True, sitemap=False)
    def web_auth_register(self, *args, **kw):

        if kw.get('data'):
            if request.httprequest.method == 'POST':
                try:

                    inscription = request.env['inscription'].sudo().create(kw.get('data'))

                    return {
                        "jsonrpc": "2.0",
                        "id": inscription.id,
                        "name": inscription.name,
                        "data": {
                            "code": 200,
                            "message": "Inscripcion creada correctamente",

                        }
                    }
                except UserError as e:
                    if request.env["inscription"].sudo().search([("email", "=", kw['data'].get('email'))]):
                        return {
                            "jsonrpc": "2.0",
                            "data": {
                                "code": 403,
                                "message": "Este correo electrónico está en uso",

                            }
                        }
                    else:
                        return {
                            "jsonrpc": "2.0",
                            "data": {
                                "code": 403,
                                "message": "No se puede crear la cuenta",

                            }
                        }
