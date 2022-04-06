# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import logging
import werkzeug

from odoo import http, _
from odoo.addons.auth_signup.models.res_users import SignupError
from odoo.addons.web.controllers.main import ensure_db, Home
from odoo.addons.base_setup.controllers.main import BaseSetup
from odoo.exceptions import UserError
from odoo.http import request

_logger = logging.getLogger(__name__)

from odoo import http

from odoo.http import request


class AuthRegisterHome(Home):

    @http.route('/web/register', type='json', auth='public', website=True, sitemap=False)
    def web_auth_register(self, *args, **kw):

        qcontext = self.get_auth_signup_qcontext()

        if qcontext.get('data'):
            if 'error' not in qcontext and request.httprequest.method == 'POST':
                try:

                    user = request.env['res.users'].sudo().create(qcontext.get('data'))

                    return {
                        "jsonrpc": "2.0",
                        "id": user.id,
                        "name": user.name,
                        "data": {
                            "code": 200,
                            "message": "Usuario creado correctamente",

                        }
                    }
                except UserError as e:
                    if request.env["res.users"].sudo().search([("login", "=", qcontext['data'].get('login'))]):
                        qcontext["error"] = _("Este correo electrónico está en uso")
                    else:
                        _logger.error("%s", e)
                        qcontext['error'] = _("No se puede crear la cuenta")
        else:

            if not qcontext.get('token') and not qcontext.get('signup_enabled'):
                raise werkzeug.exceptions.NotFound()

            if 'error' not in qcontext and request.httprequest.method == 'POST':
                try:
                    self.do_signup(qcontext)
                    # Send an account creation confirmation email
                    if qcontext.get('token'):
                        User = request.env['res.users']
                        user_sudo = User.sudo().search(
                            User._get_login_domain(qcontext.get('login')), order=User._get_login_order(), limit=1
                        )
                        template = request.env.ref('auth_signup.mail_template_user_signup_account_created',
                                                   raise_if_not_found=False)
                        if user_sudo and template:
                            template.sudo().send_mail(user_sudo.id, force_send=True)
                    return self.web_login(*args, **kw)
                except UserError as e:
                    qcontext['error'] = e.args[0]
                except (SignupError, AssertionError) as e:
                    if request.env["res.users"].sudo().search([("login", "=", qcontext.get("login"))]):
                        qcontext["error"] = _("Another user is already registered using this email address.")
                    else:
                        _logger.error("%s", e)
                        qcontext['error'] = _("Could not create a new account.")

            response = request.render('auth_signup.signup', qcontext)
            response.headers['X-Frame-Options'] = 'DENY'
            return response
