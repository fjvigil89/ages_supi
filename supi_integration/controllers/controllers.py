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

    @http.route('/web/restart_password', type='json', auth='public', website=True, sitemap=False)
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

    @http.route('/web/register', type='json', auth='public', website=True, sitemap=False)
    def web_auth_register(self, *args, **kw):

        # qcontext = self.get_auth_signup_qcontext()

        if kw.get('data'):
            if request.httprequest.method == 'POST':
                try:

                    user = request.env['res.users'].sudo().create(kw.get('data'))

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
                    if request.env["res.users"].sudo().search([("login", "=", kw['data'].get('login'))]):
                        return {
                            "jsonrpc": "2.0",
                            # "id": user.id,
                            # "name": user.name,
                            "data": {
                                "code": 403,
                                "message": "Este correo electrónico está en uso",

                            }
                        }
                        # qcontext["error"] = _("Este correo electrónico está en uso")
                    else:
                        return {
                            "jsonrpc": "2.0",
                            # "id": user.id,
                            # "name": user.name,
                            "data": {
                                "code": 403,
                                "message": "No se puede crear la cuenta",

                            }
                        }

    @http.route(
        '/api/studies_today_and_later',
        type='http', auth='user', methods=['GET'], csrf=False)
    def get_studies_today_and_later(self, **params):
        try:
            today = datetime.utcnow().date()
            print(today)
            records = request.env['planograma'].search([('date_start', '=', today)])
            planos_today = request.env['planograma'].search([('date_start', '=', today)])
            planos_later = request.env['planograma'].search([('date_start', '>', today)])
            records_later = request.env['planograma'].search([('date_start', '>', today)])
            try:
                serializer = Serializer(records, many=True)
                serializer_later = Serializer(records_later, many=True)
                salas_hoy = []
                salas_manana = []

                for item in planos_today:
                    if item.place_id.id not in salas_hoy:
                        salas_hoy.append(item.place_id.id)
                for item in planos_later:
                    if item.place_id.id not in salas_hoy:
                        salas_manana.append(item.place_id.id)

                serializer_salas_today = Serializer(planos_today.mapped('place_id'), many=True)
                serializer_salas_later = Serializer(planos_later.mapped('place_id'), many=True)
                res = {

                    "count_salas_today": len(salas_hoy),  # Cantidad de salas para hoy
                    "count_salas_later": len(salas_manana),  # Cantidad de salas proximas
                    "salas_hoy": serializer_salas_today.data,  # Datos salas hoy
                    "salas_later": serializer_salas_later.data,  # Datos salas proximas
                    "count_today": len(records),
                    "count_later": len(records_later),
                    "studies_today": serializer.data,  # Planogramas hoy
                    "studies_later": serializer_later.data  # Planogramas proximos
                }
                return http.Response(
                    json.dumps(res),
                    status=200,
                    mimetype='application/json'
                )
            except (SyntaxError, QueryFormatError) as e:
                res = error_response(e, e.msg)
                return http.Response(
                    json.dumps(res),
                    status=200,
                    mimetype='application/json'
                )
        except KeyError as e:
            msg = "Wrong values"
            res = error_response(e, msg)
            return http.Response(
                json.dumps(res),
                status=200,
                mimetype='application/json'
            )

    @http.route(
        '/api/studies_data_by_sala',
        type='http', auth='user', methods=['GET'], csrf=False)
    def get_studies_by_sala_today_and_later(self, **params):
        try:
            place_id = params["place_id"]
            print(place_id)
            today = datetime.utcnow().date()
            print(today)
            records = request.env['planograma'].search([('date_start', '=', today), ('place_id', '=', int(place_id))])
            planos_today = request.env['planograma'].search(
                [('date_start', '=', today), ('place_id', '=', int(place_id))])
            planos_later = request.env['planograma'].search(
                [('date_start', '>', today), ('place_id', '=', int(place_id))])
            records_later = request.env['planograma'].search(
                [('date_start', '>', today), ('place_id', '=', int(place_id))])
            try:
                serializer = Serializer(records.mapped('study_id'), many=True)
                serializer_later = Serializer(records_later.mapped('study_id'), many=True)
                salas_hoy = []
                salas_manana = []

                for item in planos_today:
                    if item.place_id.id not in salas_hoy:
                        salas_hoy.append(item.place_id.id)
                for item in planos_later:
                    if item.place_id.id not in salas_hoy:
                        salas_manana.append(item.place_id.id)

                serializer_salas_today = Serializer(planos_today.mapped('place_id'), many=True)
                serializer_salas_later = Serializer(planos_later.mapped('place_id'), many=True)
                res = {

                    # "count_salas_today": len(salas_hoy),  # Cantidad de salas para hoy
                    # "count_salas_later": len(salas_manana),  # Cantidad de salas proximas
                    # "salas_hoy": serializer_salas_today.data,  # Datos salas hoy
                    # "salas_later": serializer_salas_later.data,  # Datos salas proximas
                    # "count_today": len(records),
                    # "count_later": len(records_later),
                    "studies_today": serializer.data,  # Planogramas hoy
                    "studies_later": serializer_later.data  # Planogramas proximos
                }
                return http.Response(
                    json.dumps(res),
                    status=200,
                    mimetype='application/json'
                )
            except (SyntaxError, QueryFormatError) as e:
                res = error_response(e, e.msg)
                return http.Response(
                    json.dumps(res),
                    status=200,
                    mimetype='application/json'
                )
        except KeyError as e:
            msg = "Wrong values"
            res = error_response(e, msg)
            return http.Response(
                json.dumps(res),
                status=200,
                mimetype='application/json'
            )

    @http.route(
        '/api/study_variable_id',
        type='http', auth='user', methods=['GET'], csrf=False)
    def get_studies_by_variable_id(self, **params):
        try:
            variable_id = params["variable_id"]
            records = request.env['study'].search([('variable_id', '=', int(variable_id))])
            try:
                serializer = Serializer(records.mapped('variable_id'), many=True)

                res = {
                    "data": serializer.data,  # Planogramas hoy
                }
                return http.Response(
                    json.dumps(res),
                    status=200,
                    mimetype='application/json'
                )
            except (SyntaxError, QueryFormatError) as e:
                res = error_response(e, e.msg)
                return http.Response(
                    json.dumps(res),
                    status=200,
                    mimetype='application/json'
                )
        except KeyError as e:
            msg = "Wrong values"
            res = error_response(e, msg)
            return http.Response(
                json.dumps(res),
                status=200,
                mimetype='application/json'
            )

    @http.route(
        '/api/get_comunas',
        type='http', auth='user', methods=['GET'], csrf=False)
    def get_comunas(self, **params):
        try:
            user_id = params["user_id"]
            today = datetime.utcnow().date()
            records = request.env['planograma'].search(
                [('date_start', '=', today), ('state', '=', 'ready'), ('user_id', '=', int(user_id))]).mapped(
                'place_id').mapped('comuna_id')

            records_later = request.env['planograma'].search(
                [('date_start', '>', today), ('state', '=', 'ready'), ('user_id', '=', int(user_id))]).mapped(
                'place_id').mapped('comuna_id')

            try:
                serializer = Serializer(records, query='{name,id,state_id{id,name}}', many=True)
                serializer_later = Serializer(records_later, query='{name,id,state_id{id,name}}', many=True)

                res = {
                    "comunas_studies_today": serializer.data,  # Cantidad de salas para hoy
                    "comunas_studies_later": serializer_later.data,  # Cantidad de salas para hoy
                }
                return http.Response(
                    json.dumps(res),
                    status=200,
                    mimetype='application/json'
                )
            except (SyntaxError, QueryFormatError) as e:
                res = error_response(e, e.msg)
                return http.Response(
                    json.dumps(res),
                    status=200,
                    mimetype='application/json'
                )
        except KeyError as e:
            msg = "Wrong values"
            res = error_response(e, msg)
            return http.Response(
                json.dumps(res),
                status=200,
                mimetype='application/json'
            )

    @http.route(
        '/api/get_salas_by_comuna',
        type='http', auth='user', methods=['GET'], csrf=False)
    def get_salas_by_comuna(self, **params):
        try:
            comuna_id = params["comuna_id"]
            user_id = params["user_id"]
            today = datetime.utcnow().date()
            records = request.env['planograma'].search(
                [('date_start', '=', today), ('state', '=', 'ready'), ('user_id', '=', int(user_id)),
                 ('place_id.comuna_id', '=', int(comuna_id))])

            records_later = request.env['planograma'].search(
                [('date_start', '>', today), ('state', '=', 'ready'), ('user_id', '=', int(user_id)),
                 ('place_id.comuna_id', '=', int(comuna_id))])
            try:
                serializer = Serializer(records, query='{place_id{id,name,folio,geo{lat,long},state_id{id,name}}}',
                                        many=True)
                serializer_later = Serializer(records_later,
                                              query='{place_id{id,name,folio,geo{lat,long},state_id{id,name}}}',
                                              many=True)

                res = {
                    "salas_studies_today": serializer.data,  # Cantidad de salas para hoy
                    "salas_studies_later": serializer_later.data,  # Cantidad de salas para hoy
                }
                return http.Response(
                    json.dumps(res),
                    status=200,
                    mimetype='application/json'
                )
            except (SyntaxError, QueryFormatError) as e:
                res = error_response(e, e.msg)
                return http.Response(
                    json.dumps(res),
                    status=200,
                    mimetype='application/json'
                )
        except KeyError as e:
            msg = "Wrong values"
            res = error_response(e, msg)
            return http.Response(
                json.dumps(res),
                status=200,
                mimetype='application/json'
            )

    @http.route(
        '/api/get_studies_by_place',
        type='http', auth='user', methods=['GET'], csrf=False)
    def get_studies_by_place(self, **params):
        try:
            place_id = params["place_id"]
            user_id = params["user_id"]
            today = datetime.utcnow().date()
            records = request.env['planograma'].search(
                [('date_start', '=', today), ('state', '=', 'ready'), ('user_id', '=', int(user_id)),
                 ('place_id', '=', int(place_id))])

            records_later = request.env['planograma'].search(
                [('date_start', '>', today), ('state', '=', 'ready'), ('user_id', '=', int(user_id)),
                 ('place_id', '=', int(place_id))])
            try:
                serializer = Serializer(records,
                                        query='{study_id{id,name,variable_id{id,name,id_variable,type}}}',
                                        many=True)
                serializer_later = Serializer(records_later,
                                              query='{study_id{id,name,variable_id{id,name,id_variable,type}}}',
                                              many=True)

                res = {
                    "studies_today": serializer.data,  # Cantidad de salas para hoy
                    "studies_later": serializer_later.data,  # Cantidad de salas para hoy
                }
                return http.Response(
                    json.dumps(res),
                    status=200,
                    mimetype='application/json'
                )
            except (SyntaxError, QueryFormatError) as e:
                res = error_response(e, e.msg)
                return http.Response(
                    json.dumps(res),
                    status=200,
                    mimetype='application/json'
                )
        except KeyError as e:
            msg = "Wrong values"
            res = error_response(e, msg)
            return http.Response(
                json.dumps(res),
                status=200,
                mimetype='application/json'
            )

    @http.route(
        '/api/get_products_by_categ_id',
        type='http', auth='user', methods=['GET'], csrf=False)
    def get_products_by_categ_id(self, **params):
        try:
            categ_id = params["categ_id"]
            sala_id = params["sala_id"]
            study_id = params["study_id"]
            user_id = params["user_id"]
            today = datetime.utcnow().date()
            records = request.env['planograma'].search(
                [('date_start', '=', today), ('state', '=', 'ready'), ('user_id', '=', int(user_id)),
                 ('place_id', '=', int(sala_id)), ('study_id', '=', int(study_id)),
                 ('product_id.categ_id', '=', int(categ_id))])

            try:
                serializer = Serializer(records,
                                        query='{id,state,quebrado,cartel,cautivo,c_erroneo,image,product_id{id,name,default_code,barcode,lst_price,pack,image_1920}}',
                                        many=True)
                # serializer_later = Serializer(records_later,
                #                               query='{product_id{id,name,default_code,barcode,image_1920}}',
                #                               many=True)

                res = {
                    "products_today": serializer.data,  # Cantidad de salas para hoy
                    # "products_later": serializer_later.data,  # Cantidad de salas para hoy
                }
                return http.Response(
                    json.dumps(res),
                    status=200,
                    mimetype='application/json'
                )
            except (SyntaxError, QueryFormatError) as e:
                res = error_response(e, e.msg)
                return http.Response(
                    json.dumps(res),
                    status=200,
                    mimetype='application/json'
                )
        except KeyError as e:
            msg = "Wrong values"
            res = error_response(e, msg)
            return http.Response(
                json.dumps(res),
                status=200,
                mimetype='application/json'
            )

    @http.route(
        '/api/get_categories_of_products_by_study',
        type='http', auth='user', methods=['GET'], csrf=False)
    def get_categories_of_products_by_study(self, **params):
        try:
            study_id = params["study_id"]
            user_id = params["user_id"]
            today = datetime.utcnow().date()
            records = request.env['planograma'].search(
                [('date_start', '=', today), ('state', '=', 'ready'), ('user_id', '=', int(user_id)),
                 ('study_id', '=', int(study_id))])

            records_later = request.env['planograma'].search(
                [('date_start', '>', today), ('state', '=', 'ready'), ('user_id', '=', int(user_id)),
                 ('study_id', '=', int(study_id))])
            try:
                serializer = Serializer(records.mapped('product_id'),
                                        query='{categ_id{id,name}}',
                                        many=True)
                serializer_later = Serializer(records.mapped('product_id'),
                                              query='{categ_id{id,name}}',
                                              many=True)

                res = {
                    "categorias_today": serializer.data,  # Cantidad de salas para hoy
                    "categorias_later": serializer_later.data,  # Cantidad de salas para hoy
                }
                return http.Response(
                    json.dumps(res),
                    status=200,
                    mimetype='application/json'
                )
            except (SyntaxError, QueryFormatError) as e:
                res = error_response(e, e.msg)
                return http.Response(
                    json.dumps(res),
                    status=200,
                    mimetype='application/json'
                )
        except KeyError as e:
            msg = "Wrong values"
            res = error_response(e, msg)
            return http.Response(
                json.dumps(res),
                status=200,
                mimetype='application/json'
            )

    @http.route(
        '/api/update_planogramas/',
        type='json', auth="user", methods=['PUT'], csrf=False)
    def update_planogramas(self, **post):
        try:
            data = post['data']
        except KeyError:
            msg = "`data` parameter is not found on PUT request body"
            raise exceptions.ValidationError(msg)
        try:
            for item in data:
                planograma = request.env['planograma'].search([('id', '=', item.get('id'))])
                planograma.update({
                    'quebrado': item.get('quebrado'),
                    'cartel': item.get('cartel'),
                    'cautivo': item.get('cautivo'),
                    'c_erroneo': item.get('c_erroneo'),
                    'image': item.get('image'),
                    'state': item.get('state'),
                })
                planograma.product_id.sudo().update({
                    'lst_price': item.get('product_id').get('lst_price'),
                    'pack': item.get('product_id').get('pack'),
                })

            return "updated"
        except Exception as e:
            # TODO: Return error message(e.msg) on a response
            return False
