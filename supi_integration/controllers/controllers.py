# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import json
import logging
from datetime import datetime
from datetime import timedelta

import pytz
from odoo.addons.auth_signup.models.res_users import SignupError
from odoo.addons.web.controllers.main import Home

from odoo import _, exceptions
from odoo.exceptions import UserError
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

    def get_date_by_tz(self, val_date, format_a=None):
        utc_timestamp = pytz.utc.localize(val_date, is_dst=False)
        context_tz = pytz.timezone('Chile/Continental')
        if not format_a:
            return utc_timestamp.astimezone(context_tz).date()
        else:
            return utc_timestamp.astimezone(context_tz).strftime(format_a).date()

    @staticmethod
    def get_tipo_dato(tipo_dato):
        tipo_dato_text = ''
        if tipo_dato == '1':
            tipo_dato_text = "text"
        if tipo_dato == '2':
            tipo_dato_text = "int"
        if tipo_dato == '3':
            tipo_dato_text = "double"
        if tipo_dato == '4':
            tipo_dato_text = "Boolean"
        if tipo_dato == '5':
            tipo_dato_text = "select"
        if tipo_dato == '6':
            tipo_dato_text = "Precio"
        if tipo_dato == '7':
            tipo_dato_text = "Radiobutton"
        if tipo_dato == '8':
            tipo_dato_text = "Date"
        if tipo_dato == '9':
            tipo_dato_text = "Mecánica"
        if tipo_dato == '10':
            tipo_dato_text = "Estado"
        if tipo_dato == '11':
            tipo_dato_text = "Promoción"
        return tipo_dato_text

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

                    users = request.env['res.users'].sudo().search([('login', '=', kw.get('data').get('login'))])
                    if users:
                        return {
                            "jsonrpc": "2.0",
                            "data": {
                                "code": 403,
                                "message": "Este correo electrónico está en uso",
                            }
                        }

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
        '/api/get_comunas',
        type='http', auth='user', methods=['GET'], csrf=False)
    def get_comunas(self, **params):
        try:
            user_id = params["user_id"]
            today = datetime.utcnow()
            today = self.get_date_by_tz(today)

            start = today - timedelta(days=today.weekday())
            end = start + timedelta(days=6)

            # PARA HOY
            comunas_ids = request.env['planning'].search(
                [('date_end', '<=', today), ('state', '=', 'ready')]).mapped(
                'planning_salas_ids').mapped('place_id').mapped('comuna_id')

            final_data = []
            data_today = []
            comunas_append = []
            for comuna in comunas_ids:

                red = False
                count_red = 0
                blue = False
                count_blue = 0
                yellow = False
                count_yellow = 0
                green = False
                count_green = 0
                brown = False
                count_brown = 0
                planning_salas_ids = request.env['planning'].search(
                    [('date_end', '<=', today), ('state', '=', 'ready')]).mapped(
                    'planning_salas_ids').filtered(lambda x: x.place_id.comuna_id.id == comuna.id).filtered(
                    lambda x: x.auditor_id.id == int(user_id)).filtered(lambda x: x.state == 'prepared')

                for planning_sala in planning_salas_ids:
                    # SI LA NATURALEZA ES 0 (O sea de productos)
                    if planning_sala.planning_id.planograma_id.study_id_naturaleza == '0':
                        for planning_product in planning_sala.planning_products_ids:
                            if planning_product.variable_id.tipo_estudio == '4':
                                # cold_equipment
                                red = True
                                count_red += 1
                            if planning_product.variable_id.tipo_estudio == '5':
                                # exhibitions
                                blue = True
                                count_blue += 1
                            if planning_product.variable_id.tipo_estudio == '2':
                                # price
                                yellow = True
                                count_yellow += 1
                            if planning_product.variable_id.tipo_estudio == '1':
                                # osa
                                green = True
                                count_green += 1
                            if planning_product.variable_id.tipo_estudio == '3':
                                # facing
                                brown = True
                                count_brown += 1
                    else:
                        for variable in planning_sala.planning_id.planograma_id.variables_estudios_ids:
                            if variable.variable_id.tipo_estudio == '4':
                                # cold_equipment
                                red = True
                                count_red += 1
                            if variable.variable_id.tipo_estudio == '5':
                                # exhibitions
                                blue = True
                                count_blue += 1
                            if variable.variable_id.tipo_estudio == '2':
                                # price
                                yellow = True
                                count_yellow += 1
                            if variable.variable_id.tipo_estudio == '1':
                                # osa
                                green = True
                                count_green += 1
                            if variable.variable_id.tipo_estudio == '3':
                                # facing
                                brown = True
                                count_brown += 1
                comuna_data = {
                    'comuna_id': comuna.id,
                    "nombre_comuna": comuna.name,
                    "ROJO": red,
                    "count_rojo": count_red,
                    "AZUL": blue,
                    "count_azul": count_blue,
                    "AMARILLO": yellow,
                    "count_amarillo": count_yellow,
                    "VERDE": green,
                    "count_verde": count_green,
                    "CARMELITA": brown,
                    "count_carmelita": count_brown,
                }
                if comuna.id not in comunas_append:
                    comunas_append.append(comuna.id)
                    data_today.append(comuna_data)

            # end_final = end + timedelta(days=7)
            comunas_ids = request.env['planning'].search(
                [('date_end', '>', today), ('state', '=', 'ready')]).mapped(
                'planning_salas_ids').mapped('place_id').mapped('comuna_id')
            data_later = []
            comunas_append_later = []
            for comuna in comunas_ids:

                red = False
                count_red = 0
                blue = False
                count_blue = 0
                yellow = False
                count_yellow = 0
                green = False
                count_green = 0
                brown = False
                count_brown = 0
                planning_salas_ids = request.env['planning'].search(
                    [('date_end', '>', today), ('state', '=', 'ready')]).mapped(
                    'planning_salas_ids').filtered(lambda x: x.place_id.comuna_id.id == comuna.id).filtered(
                    lambda x: x.auditor_id.id == int(user_id)).filtered(lambda x: x.state == 'prepared')

                for planning_sala in planning_salas_ids:
                    # SI LA NATURALEZA ES 0 (O sea de productos)
                    if planning_sala.planning_id.planograma_id.study_id_naturaleza == '0':
                        for planning_product in planning_sala.planning_products_ids:
                            if planning_product.variable_id.tipo_estudio == '4':
                                # cold_equipment
                                red = True
                                count_red += 1
                            if planning_product.variable_id.tipo_estudio == '5':
                                # exhibitions
                                blue = True
                                count_blue += 1
                            if planning_product.variable_id.tipo_estudio == '2':
                                # price
                                yellow = True
                                count_yellow += 1
                            if planning_product.variable_id.tipo_estudio == '1':
                                # osa
                                green = True
                                count_green += 1
                            if planning_product.variable_id.tipo_estudio == '3':
                                # facing
                                brown = True
                                count_brown += 1
                    else:
                        for variable in planning_sala.planning_id.planograma_id.variables_estudios_ids:
                            if variable.variable_id.tipo_estudio == '4':
                                # cold_equipment
                                red = True
                                count_red += 1
                            if variable.variable_id.tipo_estudio == '5':
                                # exhibitions
                                blue = True
                                count_blue += 1
                            if variable.variable_id.tipo_estudio == '2':
                                # price
                                yellow = True
                                count_yellow += 1
                            if variable.variable_id.tipo_estudio == '1':
                                # osa
                                green = True
                                count_green += 1
                            if variable.variable_id.tipo_estudio == '3':
                                # facing
                                brown = True
                                count_brown += 1
                comuna_data = {
                    'comuna_id': comuna.id,
                    "nombre_comuna": comuna.name,
                    "ROJO": red,
                    "count_rojo": count_red,
                    "AZUL": blue,
                    "count_azul": count_blue,
                    "AMARILLO": yellow,
                    "count_amarillo": count_yellow,
                    "VERDE": green,
                    "count_verde": count_green,
                    "CARMELITA": brown,
                    "count_carmelita": count_brown,
                }
                if comuna.id not in comunas_append_later:
                    comunas_append_later.append(comuna.id)
                    data_later.append(comuna_data)
            try:
                res = {
                    "Comunas de hoy": data_today,  # Cantidad de salas para hoy
                    "Comunas de Semana Próxima": data_later,  # Cantidad de salas para hoy

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
            type = params["type"]
            today = datetime.utcnow()

            today = self.get_date_by_tz(today)
            start = today - timedelta(days=today.weekday())
            end = start + timedelta(days=6)
            planning_salas_ids = request.env['planning'].search(
                [('date_end', '<=', today), ('state', '=', 'ready')]).mapped(
                'planning_salas_ids').filtered(lambda x: x.place_id.comuna_id.id == int(comuna_id)).filtered(
                lambda x: x.state == 'prepared').filtered(
                lambda x: x.auditor_id.id == int(user_id))
            data = []
            salas_append = []
            for planning_salas in planning_salas_ids:
                if planning_salas.planning_id.planograma_id.study_id_naturaleza == '0':
                    for variable in planning_salas.mapped('planning_products_ids').mapped('variable_id'):
                        if variable.tipo_estudio == type:
                            sala_data = {
                                'id': planning_salas.place_id.id,
                                'folio': planning_salas.place_id.folio or '',
                                'planning_sala_id': planning_salas.id,
                                'name': planning_salas.place_id.name or '',
                                'lat': planning_salas.place_id.lat or '',
                                'long': planning_salas.place_id.long or '',
                                'address': planning_salas.place_id.address or '',
                                'image': planning_salas.place_id.url_image or '',
                            }
                            if planning_salas.place_id.id not in salas_append:
                                salas_append.append(planning_salas.place_id.id)
                                data.append(sala_data)
                else:
                    for variable in planning_salas.planning_id.planograma_id.variables_estudios_ids:
                        if variable.variable_id.tipo_estudio == type:
                            sala_data = {
                                'id': planning_salas.place_id.id,
                                'folio': planning_salas.place_id.folio or '',
                                'planning_sala_id': planning_salas.id,
                                'name': planning_salas.place_id.name or '',
                                'lat': planning_salas.place_id.lat or '',
                                'long': planning_salas.place_id.long or '',
                                'address': planning_salas.place_id.address or '',
                                'image': planning_salas.place_id.url_image or '',
                            }
                            if planning_salas.place_id.id not in salas_append:
                                salas_append.append(planning_salas.place_id.id)
                                data.append(sala_data)

            planning_salas_ids = request.env['planning'].search(
                [('date_end', '>', today), ('state', '=', 'ready')]).mapped(
                'planning_salas_ids').filtered(lambda x: x.place_id.comuna_id.id == int(comuna_id)).filtered(
                lambda x: x.state == 'prepared').filtered(
                lambda x: x.auditor_id.id == int(user_id))
            data_later = []

            for planning_salas in planning_salas_ids:
                if planning_salas.planning_id.planograma_id.study_id_naturaleza == '0':
                    for variable in planning_salas.mapped('planning_products_ids').mapped('variable_id'):
                        if variable.tipo_estudio == type:
                            sala_data = {
                                'id': planning_salas.place_id.id,
                                'folio': planning_salas.place_id.folio or '',
                                'planning_sala_id': planning_salas.id,
                                'name': planning_salas.place_id.name or '',
                                'lat': planning_salas.place_id.lat or '',
                                'long': planning_salas.place_id.long or '',
                                'address': planning_salas.place_id.address or '',
                                'image': planning_salas.place_id.url_image or '',
                            }
                            if planning_salas.place_id.id not in salas_append:
                                salas_append.append(planning_salas.place_id.id)
                                data.append(sala_data)
                else:
                    for variable in planning_salas.planning_id.planograma_id.variables_estudios_ids:
                        if variable.variable_id.tipo_estudio == type:
                            sala_data = {
                                'id': planning_salas.place_id.id,
                                'folio': planning_salas.place_id.folio or '',
                                'planning_sala_id': planning_salas.id,
                                'name': planning_salas.place_id.name or '',
                                'lat': planning_salas.place_id.lat or '',
                                'long': planning_salas.place_id.long or '',
                                'address': planning_salas.place_id.address or '',
                                'image': planning_salas.place_id.url_image or '',
                            }
                            if planning_salas.place_id.id not in salas_append:
                                salas_append.append(planning_salas.place_id.id)
                                data_later.append(sala_data)
            try:
                res = {'hoy': data, 'next': data_later}
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
        '/api/get_quiz',
        type='http', auth='user', methods=['GET'], csrf=False)
    def get_quiz(self, **params):
        try:
            id_sala_planificada = params["id_sala_planificada"]
            planning_sala = request.env['planning.salas'].search([('id', '=', int(id_sala_planificada))])

            vals_return = {
                "Id_SalaPlanificada": planning_sala.id,
                "data": [
                    {
                        "quiz1_id": planning_sala.id_quiz_1.id,
                        "Pregunta": planning_sala.id_quiz_1.question or '',
                        "opcion_respuesta1_correcta": planning_sala.id_quiz_1.correct_answer or '',
                        "opcion_respuesta2": planning_sala.id_quiz_1.answer1 or '',
                        "opcion_respuesta3": planning_sala.id_quiz_1.answer2 or '',
                        "respuesta_seleccionada_por_auditor": planning_sala.answer_quiz_1 or ''
                    },
                    {
                        "quiz2_id": planning_sala.id_quiz_2.id,
                        "Pregunta": planning_sala.id_quiz_2.question or '',
                        "opcion_respuesta1_correcta": planning_sala.id_quiz_2.correct_answer or '',
                        "opcion_respuesta2": planning_sala.id_quiz_2.answer1 or '',
                        "opcion_respuesta3": planning_sala.id_quiz_2.answer2 or '',
                        "respuesta_seleccionada_por_auditor": planning_sala.answer_quiz_2 or ''
                    },
                    {
                        "quiz3_id": planning_sala.id_quiz_3.id,
                        "Pregunta": planning_sala.id_quiz_3.question or '',
                        "opcion_respuesta1_correcta": planning_sala.id_quiz_3.correct_answer or '',
                        "opcion_respuesta2": planning_sala.id_quiz_3.answer1 or '',
                        "opcion_respuesta3": planning_sala.id_quiz_3.answer2 or '',
                        "respuesta_seleccionada_por_auditor": planning_sala.answer_quiz_3 or ''
                    }
                ]
            }
            try:
                res = {
                    "params": vals_return,
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
            type = params["type"]
            today = datetime.utcnow()
            today = self.get_date_by_tz(today)

            start = today - timedelta(days=today.weekday())
            end = start + timedelta(days=6)

            planning_salas_ids = request.env['planning'].search(
                [('date_end', '<=', today), ('state', '=', 'ready')]).mapped(
                'planning_salas_ids').filtered(lambda x: x.place_id.id == int(place_id)).filtered(
                lambda x: x.state == 'prepared').filtered(
                lambda x: x.auditor_id.id == int(user_id))
            data = []
            for planning_salas in planning_salas_ids:

                if planning_salas.planning_id.planograma_id.study_id.type == type:
                    Tipo_estudio = ''
                    if planning_salas.planning_id.planograma_id.study_id.type == '2':
                        Tipo_estudio = "Precio"
                    if planning_salas.planning_id.planograma_id.study_id.type == '3':
                        Tipo_estudio = "Facing"
                    if planning_salas.planning_id.planograma_id.study_id.type == '1':
                        Tipo_estudio = "OSA"

                    if planning_salas.planning_id.planograma_id.study_id.type == '4':
                        Tipo_estudio = "Equipos de frio"

                    if planning_salas.planning_id.planograma_id.study_id.type == '5':
                        Tipo_estudio = "Exhibitions"

                    Naturaleza = ''

                    if planning_salas.planning_id.planograma_id.study_id.naturaleza == '0':
                        Naturaleza = "Productos"

                    if planning_salas.planning_id.planograma_id.study_id.naturaleza == '1':
                        Naturaleza = "Muebles sin productos"

                    if planning_salas.planning_id.planograma_id.study_id.naturaleza == '2':
                        Naturaleza = "Muebles con productos"

                    if planning_salas.planning_id.planograma_id.study_id.naturaleza == '3':
                        Naturaleza = "Salas"

                    variables = []

                    if planning_salas.planning_id.planograma_id.study_id.naturaleza == '0':
                        for variable in planning_salas.mapped('planning_products_ids').mapped('variable_id'):
                            tipo_dato = self.get_tipo_dato(variable.tipo_dato)

                            vals_val = {
                                'id_variable': variable.id,
                                'name_variable': variable.name or '',
                                'label_visual': variable.label_visual or '',
                                'Tipo_Dato': tipo_dato or '',
                                'valores_combo': variable.valores_combobox.split(
                                    ',') if variable.valores_combobox else [],
                                'icono': variable.url_icon,
                                "xN1": variable.xN1,
                                "xN2": variable.xN2,
                                "logica_muestreo": variable.logica_muestreo.expresion or '',
                                "logica_muestreo_message": variable.logica_muestreo.error_description or '',
                                "valor_x_defecto": variable.valor_x_defecto or '',
                            }
                            variables.append(vals_val)
                    else:
                        for variable in planning_salas.planning_id.planograma_id.variables_estudios_ids:
                            tipo_dato = self.get_tipo_dato(variable.variable_id.tipo_dato)
                            vals_val = {
                                'id_variable': variable.variable_id.id,
                                'name_variable': variable.variable_id.name or '',
                                'label_visual': variable.variable_id.label_visual or '',
                                'Tipo_Dato': tipo_dato or '',
                                'valores_combo': variable.variable_id.valores_combobox.split(
                                    ',') if variable.variable_id.valores_combobox else [],
                                "order": variable.no_order,
                                'icono': variable.variable_id.url_icon,
                                "logica_muestreo": variable.variable_id.logica_muestreo.expresion or '',
                                "logica_muestreo_message": variable.variable_id.logica_muestreo.error_description or '',
                                "xN1": variable.variable_id.xN1,
                                "xN2": variable.variable_id.xN2,
                                "valor_x_defecto": variable.variable_id.valor_x_defecto or '',
                            }
                            variables.append(vals_val)
                    clientes = request.env['res.partner'].search(
                        [('id', 'in', planning_salas.planning_id.planograma_id.partner_id.ids)])
                    clientes_name = ''
                    for client in clientes:
                        clientes_name += '%s ' % client.name

                    vals = {
                        "estudio_Id": planning_salas.planning_id.planograma_id.study_id.id,
                        "consecutivo": planning_salas.name,
                        "Sala_Planificada": planning_salas.id,
                        "Nombre_Estudio": planning_salas.planning_id.planograma_id.study_id.name,
                        "Clientes": clientes_name,
                        "Tipo_estudio": "%s- %s" % (
                            planning_salas.planning_id.planograma_id.study_id.type, Tipo_estudio),
                        "Naturaleza_Estudio": Naturaleza,
                        "Variables": variables
                    }
                    data.append(vals)
            try:
                res = {
                    "Lista de Estudios dados la selección": data,  # Cantidad de salas para hoy
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
        '/api/get_variables_de_salas',
        type='http', auth='user', methods=['GET'], csrf=False)
    def get_variables_de_salas(self, **params):
        try:
            id_sala_planificada = params["id_sala_planificada"]
            data = []

            sala_planificada = request.env['planning.salas'].search([('id', '=', id_sala_planificada)])

            for variable_estudios in sala_planificada.planning_id.planograma_id.variables_estudios_ids:
                tipo_dato = self.get_tipo_dato(variable_estudios.variable_id.tipo_dato)
                vals = {
                    "id_variable": variable_estudios.variable_id.id,
                    "id_sala_planificada": int(id_sala_planificada),
                    "name_variable": variable_estudios.variable_id.name,
                    "label_visual": variable_estudios.variable_id.label_visual,
                    "Tipo_Dato": tipo_dato,
                    "valores_combo": variable_estudios.variable_id.valores_combobox.split(
                        ',') if variable_estudios.variable_id.valores_combobox else [],
                    'icono': variable_estudios.variable_id.url_icon,
                    "xN1": variable_estudios.variable_id.xN1,
                    "xN2": variable_estudios.variable_id.xN2,
                    "logica_muestreo": variable_estudios.variable_id.logica_muestreo.expresion or '',
                    "logica_muestreo_message": variable_estudios.variable_id.logica_muestreo.error_description or '',
                    "Valor_x_Defecto_target": variable_estudios.variable_id.valor_x_defecto or '',
                    "Porc_Validación": "",
                    "Disponibilidad": "",
                    "order": variable_estudios.no_order,
                    "Respuesta": "",
                    "Comentario": "",
                    "is_audited": False,
                    "Momento_medición": ""
                }
                data.append(vals)

            try:
                res = {
                    "variables_de_la_sala": data,
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
        '/api/producto_escaneado',
        type='http', auth='user', methods=['GET'], csrf=False)
    def producto_escaneado(self, **params):
        try:
            sala_planificada = params["sala_planificada"]
            ean = params["ean"]

            data = []
            product = request.env['product.product'].search([('default_code', '=', ean)], limit=1)
            if product:
                planning_sala = request.env['planning.salas'].search([('id', '=', int(sala_planificada))], limit=1)

                variables = []
                for variable in planning_sala.planning_id.planograma_id.variables_estudios_ids:
                    variables.append(variable.variable_id)
                for var_product in variables:
                    medicion = request.env['planning.product'].search(
                        [('product_id', '=', product.id), ('variable_id', '=', var_product.id),
                         ('planning_salas_id', '=', int(sala_planificada))])
                    if medicion:
                        pass
                    else:
                        vals = {
                            "product_id": product.id,
                            "variable_id": var_product.id,
                            "planning_salas_id": int(sala_planificada),
                            "planogramado": False,
                            "name": planning_sala.name,
                        }
                        request.env['planning.product'].create(vals)
                planning_products_variables = request.env['planning.product'].search(
                    [('product_id', '=', product.id), ('planning_salas_id', '=', int(sala_planificada))]).mapped(
                    'variable_id')
                variables_data = []
                for planning_products_variable in planning_products_variables:
                    tipo_dato = self.get_tipo_dato(planning_products_variable.tipo_dato)
                    var_vals = {
                        "id_variable": planning_products_variable.id,
                        "name_variable": planning_products_variable.name,
                        "label_visual": planning_products_variable.label_visual,
                        "Tipo_Dato": tipo_dato,
                        "valores_combo": planning_products_variable.valores_combobox,
                        "logica_muestreo": planning_products_variable.logica_muestreo.expresion or '',
                        "logica_muestreo_message": planning_products_variable.logica_muestreo.error_description or '',
                        "ícono": planning_products_variable.url_icon,
                        "xN1": planning_products_variable.xN1,
                        "xN2": planning_products_variable.xN2,
                        "Valor_x_Defecto_target": planning_products_variable.valor_x_defecto or '',
                        "Porc_Validación": "",
                        "Disponibilidad": "",
                        "Respuesta": "",
                        "Comentario": "",
                        "Momento_medición": "",
                        "Id_Producto_Planificado_Padre": "",
                        "Posicion_X_del_producto": "",
                        "Posicion_Y_del_producto": ""
                    }
                    variables_data.append(var_vals)
                vals_product = {
                    "id_producto": product.id,
                    "EAN": product.default_code,
                    "name_prod": product.name,
                    "user_id": planning_sala.auditor_id.id,
                    "planning_place": planning_sala.id,
                    "Categoria": product.categ_id.name,
                    "es_mueble": product.can_be_mueble,
                    "ícono": product.url_icon,
                    "is_audited": False,
                    "planogramado": False,
                    "Variables": variables_data,
                    "Fotos medidas": []

                }
            else:
                product = request.env['product.product'].sudo().create({
                    "name": "Producto creado con ean %s" % ean,
                    "default_code": ean
                })

                planning_sala = request.env['planning.salas'].search([('id', '=', int(sala_planificada))], limit=1)

                variables = []
                for variable in planning_sala.planning_id.planograma_id.variables_estudios_ids:
                    variables.append(variable.variable_id)
                for var_product in variables:
                    vals = {
                        "product_id": product.id,
                        "variable_id": var_product.id,
                        "planning_salas_id": int(sala_planificada),
                        "planogramado": False,
                        "name": planning_sala.name,
                    }
                    request.env['planning.product'].create(vals)
                planning_products_variables = request.env['planning.product'].search(
                    [('product_id', '=', product.id), ('planning_salas_id', '=', int(sala_planificada))]).mapped(
                    'variable_id')
                variables_data = []
                for planning_products_variable in planning_products_variables:
                    tipo_dato = self.get_tipo_dato(planning_products_variable.tipo_dato)
                    var_vals = {
                        "id_variable": planning_products_variable.id,
                        "name_variable": planning_products_variable.name,
                        "label_visual": planning_products_variable.label_visual,
                        "Tipo_Dato": tipo_dato,
                        "valores_combo": planning_products_variable.valores_combobox,
                        "logica_muestreo": planning_products_variable.logica_muestreo.expresion or '',
                        "logica_muestreo_message": planning_products_variable.logica_muestreo.error_description or '',
                        "ícono": planning_products_variable.url_icon,
                        "xN1": planning_products_variable.xN1,
                        "xN2": planning_products_variable.xN2,
                        "Valor_x_Defecto_target": planning_products_variable.valor_x_defecto or '',
                        "Porc_Validación": "",
                        "Disponibilidad": "",
                        "Respuesta": "",
                        "Comentario": "",
                        "is_audited": False,
                        "Momento_medición": "",
                        "Id_Producto_Planificado_Padre": "",
                        "Posicion_X_del_producto": "",
                        "Posicion_Y_del_producto": ""
                    }
                    variables_data.append(var_vals)
                vals_product = {
                    "id_producto": product.id,
                    "EAN": product.default_code,
                    "name_prod": product.name,
                    "user_id": planning_sala.auditor_id.id,
                    "planning_place": planning_sala.id,
                    "Categoria": product.categ_id.name,
                    "es_mueble": product.can_be_mueble,
                    "ícono": product.url_icon,
                    "planogramado": False,
                    "Variables": variables_data,
                    "Fotos medidas": []
                }

            try:
                res = {
                    "Product": vals_product,
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
        '/api/get_categories_of_products_by_sala_planificada',
        type='http', auth='user', methods=['GET'], csrf=False)
    def get_categories_of_products_by_sala_planificada(self, **params):
        try:
            id_sala_planificada = params["id_sala_planificada"]
            categories = request.env['planning.salas'].search(
                [('id', '=', int(id_sala_planificada))]).mapped(
                'categories_ids')
            try:
                categories_data = []
                for cat in categories:
                    vals = {
                        'id': cat.id,
                        "name": cat.name
                    }
                    categories_data.append(vals)
                res = {
                    "Id_Sala_planificada": id_sala_planificada,
                    "categories": categories_data,  # Cantidad de salas para hoy
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
        '/api/muebles_variables',
        type='http', auth='user', methods=['GET'], csrf=False)
    def muebles_variables(self, **params):
        try:
            id_sala_planificada = params["id_sala_planificada"]
            data_variables = []

            sala_planificada = request.env['planning.salas'].search([('id', '=', id_sala_planificada)])

            for variable_estudios in sala_planificada.planning_id.planograma_id.variables_estudios_ids:
                tipo_dato = self.get_tipo_dato(variable_estudios.variable_id.tipo_dato)
                vals = {
                    "id_variable": variable_estudios.variable_id.id,
                    "name_variable": variable_estudios.variable_id.name,
                    "label_visual": variable_estudios.variable_id.label_visual,
                    "Tipo_Dato": tipo_dato,
                    "valores_combo": variable_estudios.variable_id.valores_combobox.split(
                        ',') if variable_estudios.variable_id.valores_combobox else [],
                    "logica_muestreo": variable_estudios.variable_id.logica_muestreo.expresion or '',
                    "logica_muestreo_message": variable_estudios.variable_id.logica_muestreo.error_description or '',
                    'icono': variable_estudios.variable_id.url_icon,
                    "xN1": variable_estudios.variable_id.xN1,
                    "xN2": variable_estudios.variable_id.xN2,
                    "Valor_x_Defecto_target": variable_estudios.variable_id.valor_x_defecto or '',
                    "Porc_Validación": "",
                    "Disponibilidad": "",
                    "is_audited": False,
                    "order": variable_estudios.no_order,
                    "variable_id_depende": variable_estudios.variable_id.variable_que_depende_id.id or 0,
                    "is_automatic": variable_estudios.variable_id.is_automatic,
                    "Respuesta": "",
                    "Comentario": "",
                    "Momento_medición": ""
                }
                data_variables.append(vals)

            muebles = request.env['product.product'].search([('can_be_mueble', '=', True)])

            muebles_data = []

            for mueble in muebles:
                vals = {
                    "Id_Producto": mueble.id,
                    "Nombre": mueble.name,
                    "Is_Mueble": mueble.can_be_mueble
                }
                muebles_data.append(vals)
            id_sala_planificada = params["id_sala_planificada"]
            categories = request.env['planning.salas'].search(
                [('id', '=', int(id_sala_planificada))]).mapped(
                'categories_ids')
            categories_data = []
            for cat in categories:
                vals = {
                    'id': cat.id,
                    "name": cat.name
                }
                categories_data.append(vals)

            try:
                res = {
                    "Nuevo_Mueble": {
                        "id_sala_planificada": int(id_sala_planificada),
                        "Combo_Muebles": muebles_data,
                        "Tipo_Nuevo_Mueble_escogido": "",
                        "Cant_X": "",
                        "Cant_Y": "",
                        "Result_Variables_del_nuevo_mueble": data_variables,
                        "categorias": categories_data,
                        "Fotos medidas": []
                    }
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
        '/api/muebles_variables',
        type='json', auth='user', methods=['POST'], csrf=False)
    def post_muebles_variables(self, **params):
        try:

            data = params.get("Nuevo_Mueble")
            id_sala_planificada = data.get("id_sala_planificada")
            product_id = data.get("Tipo_Nuevo_Mueble_escogido")
            cantx = data.get("Cant_X")
            canty = data.get("Cant_Y")
            variables = data.get("Result_Variables_del_nuevo_mueble")
            planning_product = False
            today = datetime.utcnow()
            today = self.get_date_by_tz(today)

            images = data.get('Fotos medidas')

            for variable in variables:
                medicion = request.env['planning.product'].search(
                    [('product_id', '=', int(product_id)), ('variable_id', '=', variable.get("id_variable")),
                     ('planning_salas_id', '=', int(id_sala_planificada))])
                if medicion:

                    vals = {
                        'product_id': int(product_id),
                        "variable_id": variable.get("id_variable"),
                        "planning_salas_id": int(id_sala_planificada),
                        "respuesta": variable.get("Respuesta"),
                        "comment": variable.get("Comentario"),
                        "disponibilidad": variable.get("Disponibilidad"),
                        "date_start": today,
                        "posicion_x": cantx,
                        "is_audited": variable.get("is_audited"),
                        "xN1": variable.get("xN1"),
                        "xN2": variable.get("xN2"),
                        "posicion_y": canty,
                    }
                    medicion.write(vals)
                    planning_product = medicion.id
                    for image in images:
                        vals = {
                            'planning_product_id': medicion.id,
                            "image": b'%s' % image.encode()
                        }
                        request.env['photo.planning.product'].create(vals)
                else:
                    vals = {
                        'product_id': int(product_id),
                        "variable_id": variable.get("id_variable"),
                        "planning_salas_id": int(id_sala_planificada),
                        "respuesta": variable.get("Respuesta"),
                        "comment": variable.get("Comentario"),
                        "disponibilidad": variable.get("Disponibilidad"),
                        "date_start": today,
                        "posicion_x": cantx,
                        "is_audited": variable.get("is_audited"),
                        "xN1": variable.get("xN1"),
                        "xN2": variable.get("xN2"),
                        "posicion_y": canty,
                    }
                    planning_product = request.env['planning.product'].create(vals).id
                    for image in images:
                        vals = {
                            'planning_product_id': planning_product,
                            "image": b'%s' % image.encode()
                        }
                        request.env['photo.planning.product'].create(vals)

            try:
                planning_products = request.env['planning.product'].search(
                    [('planning_salas_id', '=', int(id_sala_planificada)),
                     ('product_id', '=', int(product_id))])

                muebles = []
                for product in planning_products:
                    products_hijos = []
                    products_hijos_medidos = request.env['planning.product'].search(
                        [('planning_salas_id', '=', int(id_sala_planificada)),
                         ('product_padre_id', '=', product.product_id.id)])

                    for product_hijo in products_hijos_medidos:
                        tipo_dato = self.get_tipo_dato(product_hijo.variable_id.tipo_dato)
                        vals_product_hijo = {
                            "id_medicion": product_hijo.id,
                            'name': product_hijo.product_id.name,
                            "x": product_hijo.posicion_x,
                            "y": product_hijo.posicion_y,
                            "url_product_icon": product_hijo.product_id.url_icon,
                            "id_variable": product_hijo.variable_id.id,
                            "name_variable": product_hijo.variable_id.name,
                            "label_visual": product_hijo.variable_id.label_visual,
                            "Tipo_Dato": tipo_dato,
                            'valores_combo': product_hijo.variable_id.valores_combobox.split(
                                ',') if product_hijo.variable_id.valores_combobox else [],
                            "ícono": product_hijo.variable_id.url_icon,
                            "logica_muestreo": product_hijo.variable_id.logica_muestreo.expresion or '',
                            "logica_muestreo_message": product_hijo.variable_id.logica_muestreo.error_description or '',
                            "xN1": product_hijo.xN1,
                            "xN2": product_hijo.xN2,
                            "Valor_x_Defecto_target": product_hijo.valor_por_defecto or '',
                            # "Porc_Validación": product_hijo.validation_perc.expresion or "",
                            "Disponibilidad": product_hijo.disponibilidad or "",
                            "Respuesta": product_hijo.respuesta,
                            "Comentario": product_hijo.comment,
                            "Momento_medición": "",
                            "Id_Producto_Planificado_Padre": product_hijo.product_padre_id.id,
                            "Posicion_X_del_producto": product_hijo.posicion_x,
                            "Posicion_Y_del_producto": product_hijo.posicion_y,
                        }
                        products_hijos.append(vals_product_hijo)
                    valores_x_cuadrado = []
                    x = y = 1
                    while x <= int(product.posicion_x):
                        y = 1
                        while y <= int(product.posicion_y):
                            # print('%s,%s' % (x, y))
                            products_hijos_medidos_posicion = request.env['planning.product'].search(
                                [('planning_salas_id', '=', int(id_sala_planificada)),
                                 ('product_padre_id', '=', product.product_id.id), ("posicion_x", '=', str(x)),
                                 ("posicion_y", '=', str(y))])

                            if products_hijos_medidos_posicion:
                                val = {
                                    "x": x,
                                    "y": y,
                                    "cant": len(products_hijos_medidos_posicion)
                                }
                            else:
                                val = {
                                    "x": x,
                                    "y": y,
                                    "cant": 0
                                }
                            valores_x_cuadrado.append(val)
                            y += 1
                        x += 1
                    print(valores_x_cuadrado)
                    image = request.env['photo.planning.product'].search(
                        [('planning_product_id', '=', product.id)], limit=1)
                    vals = {
                        "id_medicion": product.id,
                        "product_id": product.product_id.id,
                        'name': product.product_id.name,
                        "x": product.posicion_x,
                        "y": product.posicion_y,
                        "url_imagen": image.url_image,
                        "url_icon": product.product_id.url_icon,
                        "productos": products_hijos,
                        "valores_por_cuadrado": valores_x_cuadrado
                    }
                    muebles.append(vals)

                res = {
                    "Productos": muebles
                }

                return res
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
        '/api/set_medicion_variables_salas',
        type='json', auth='user', methods=['POST'], csrf=False)
    def set_medicion_variables_salas(self, **params):
        try:
            data = params.get("variables_de_la_sala")

            for variable in data:
                product = request.env['product.product'].search(
                    [('default_code', '=', 'SALA')], limit=1).id

                medicion = request.env['planning.product'].search(
                    [('product_id', '=', product), ('variable_id', '=', variable.get('id_variable')),
                     ('planning_salas_id', '=', variable.get('id_sala_planificada'))])
                today = datetime.utcnow()
                today = self.get_date_by_tz(today)
                if medicion:
                    vals = {
                        'product_id': product,
                        "variable_id": variable.get('id_variable'),
                        "planning_salas_id": variable.get('id_sala_planificada'),
                        "respuesta": variable.get("Respuesta"),
                        "comment": variable.get("Comentario"),
                        "disponibilidad": variable.get("Disponibilidad"),
                        "validation_perc": variable.get("Porc_Validación"),
                        "xN1": variable.get("xN1"),
                        "xN2": variable.get("xN2"),
                        "is_audited": variable.get("is_audited"),
                        "date_start": today,
                    }
                    medicion.write(vals)
                else:
                    today = datetime.utcnow()
                    today = self.get_date_by_tz(today)
                    vals = {
                        'product_id': product,
                        "variable_id": variable.get('id_variable'),
                        "planning_salas_id": variable.get('id_sala_planificada'),
                        "respuesta": variable.get("Respuesta"),
                        "comment": variable.get("Comentario"),
                        "disponibilidad": variable.get("Disponibilidad"),
                        "validation_perc": variable.get("Porc_Validación"),
                        "xN1": variable.get("xN1"),
                        "xN2": variable.get("xN2"),
                        "is_audited": variable.get("is_audited"),
                        "date_start": today,
                    }
                    request.env['planning.product'].create(vals)
            return True
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

    @http.route(
        '/api/register_medicions/',
        type='json', auth="user", methods=['POST'], csrf=False)
    def register_medicions(self, **post):
        try:
            productos = post['Productos']
        except KeyError:
            msg = "`data` parameter is not found on PUT request body"
            raise exceptions.ValidationError(msg)
        try:
            for data in productos:
                product_id = data.get('id_producto')
                planning_sala = data.get('planning_place')
                is_audited = data.get('is_audited')
                auditor = data.get('user_id')
                for var in data.get('Variables'):
                    medicion = request.env['planning.product'].search(
                        [('product_id', '=', int(product_id)), ('variable_id', '=', int(var.get('id_variable'))),
                         ('planning_salas_id', '=', int(planning_sala))])
                    if medicion:
                        today = datetime.utcnow()
                        today = self.get_date_by_tz(today)
                        vals = {
                            'product_id': int(product_id),
                            "variable_id": int(var.get('id_variable')),
                            "planning_salas_id": int(planning_sala),
                            "respuesta": var.get('Respuesta'),
                            "comment": var.get('Respuesta'),
                            "disponibilidad": var.get('Disponibilidad'),
                            "validation_perc": var.get('Porc_Validación'),
                            "xN1": var.get('xN1'),
                            "xN2": var.get('xN2'),
                            "is_audited": is_audited,
                            "date_start": today,
                        }
                        medicion.write(vals)
                        images = data.get('Fotos medidas')
                        for image in images:
                            vals = {
                                'planning_product_id': medicion.id,
                                "image": b'%s' % image.encode()
                            }
                            request.env['photo.planning.product'].create(vals)

                    else:
                        today = datetime.utcnow()
                        today = self.get_date_by_tz(today)
                        vals = {
                            'product_id': int(product_id),
                            "variable_id": int(var.get('id_variable')),
                            "planning_salas_id": int(planning_sala),
                            "respuesta": var.get('Respuesta'),
                            "comment": var.get('Respuesta'),
                            "disponibilidad": var.get('Disponibilidad'),
                            "validation_perc": var.get('Porc_Validación'),
                            "xN1": var.get('xN1'),
                            "xN2": var.get('xN2'),
                            "is_audited": is_audited,
                            "date_start": today,
                        }
                        study_id = request.env['planning.product'].create(vals)

                        images = data.get('Fotos medidas')
                        for image in images:
                            vals = {
                                'planning_product_id': study_id.id,
                                "image": b'%s' % image.encode()
                            }
                            request.env['photo.planning.product'].create(vals)

            return "updated"
        except Exception as e:
            # TODO: Return error message(e.msg) on a response
            return False

    @http.route(
        '/api/update_quizs/',
        type='json', auth="user", methods=['PUT'], csrf=False)
    def update_quizs(self, **post):
        try:
            data = post
        except KeyError:
            msg = "`params` parameter is not found on PUT request body"
            raise exceptions.ValidationError(msg)
        try:
            planning_sala = request.env['planning.salas'].search([('id', '=', int(data.get('Id_SalaPlanificada')))])

            planning_sala.write({
                'answer_quiz_1': data.get('data')[0].get('respuesta_seleccionada_por_auditor'),
                'answer_quiz_2': data.get('data')[1].get('respuesta_seleccionada_por_auditor'),
                'answer_quiz_3': data.get('data')[2].get('respuesta_seleccionada_por_auditor'),
            })
            return "updated"
        except Exception as e:
            # TODO: Return error message(e.msg) on a response
            return False

    @http.route(
        '/api/reject_study/',
        type='json', auth="user", methods=['PUT'], csrf=False)
    def reject_study(self, **post):
        try:
            data = post
        except KeyError:
            msg = "`params` parameter is not found on PUT request body"
            raise exceptions.ValidationError(msg)
        try:
            planning_sala = request.env['planning.salas'].search([('id', '=', int(data.get('Id_SalaPlanificada')))])

            planning_sala.write({
                'state': data.get("state"),
                'comment': data.get("comment"),
            })
            return "updated"
        except Exception as e:
            # TODO: Return error message(e.msg) on a response
            return False

    @http.route(
        '/api/end_study/',
        type='json', auth="user", methods=['PUT'], csrf=False)
    def end_study(self, **post):
        try:
            data = post
        except KeyError:
            msg = "`params` parameter is not found on PUT request body"
            raise exceptions.ValidationError(msg)
        try:
            planning_sala = request.env['planning.salas'].search([('id', '=', int(data.get('Id_SalaPlanificada')))])

            planning_sala.write({
                'state': "done",
                'comment': data.get("comment"),
            })
            return "updated"
        except Exception as e:
            # TODO: Return error message(e.msg) on a response
            return False

    @http.route(
        '/api/get_products_by_categ_id',
        type='http', auth='user', methods=['GET'], csrf=False)
    def get_products_by_categ_id(self, **params):
        try:
            categ_id = params["categ_id"]
            id_sala_planogramada = params["id_sala_planogramada"]
            try:

                planning_products = request.env['planning.product'].search(
                    [('planning_salas_id', '=', int(id_sala_planogramada))]).filtered(
                    lambda planning: planning.product_id.categ_id.id == int(categ_id))

                products = []
                productos_anadidos = []
                for producto in planning_products:
                    variables = []
                    for planning_product in planning_products:
                        if planning_product.product_id.id == producto.product_id.id:
                            tipo_dato = self.get_tipo_dato(planning_product.variable_id.tipo_dato)
                            variables_studios = request.env['planning.salas'].search(
                                [("id", "=",
                                  int(id_sala_planogramada))]).planning_id.planograma_id.mapped(
                                'variables_estudios_ids')
                            order = 0
                            for var in variables_studios:
                                if var.variable_id.id == planning_product.variable_id.id:
                                    order = var.no_order

                            vals_var = {
                                "id_variable": planning_product.variable_id.id,
                                "name_variable": planning_product.variable_id.name,
                                "label_visual": planning_product.variable_id.label_visual,

                                "Tipo_Dato": tipo_dato,
                                'valores_combo': planning_product.variable_id.valores_combobox.split(
                                    ',') if planning_product.variable_id.valores_combobox else [],
                                "ícono": planning_product.variable_id.url_icon,
                                "xN1": planning_product.variable_id.xN1,
                                "xN2": planning_product.variable_id.xN2,
                                "logica_muestreo": planning_product.variable_id.logica_muestreo.expresion or '',
                                "logica_muestreo_message": planning_product.variable_id.logica_muestreo.error_description or '',
                                "Valor_x_Defecto_target": planning_product.variable_id.valor_x_defecto or '',
                                "Porc_Validación": "",
                                "Disponibilidad": "",
                                "Respuesta": "",
                                "order": order,
                                "variable_id_depende": planning_product.variable_id.variable_que_depende_id.id or 0,
                                "is_automatic": planning_product.variable_id.is_automatic,
                                "Comentario": "",
                                "Momento_medición": "",
                                "Id_Producto_Planificado_Padre": "",
                                "Posicion_X_del_producto": "",
                                "Posicion_Y_del_producto": "",
                            }
                            variables.append(vals_var)
                    vals_prod = {
                        "id_medicion": producto.id,
                        "id_producto": producto.product_id.id,
                        "EAN": producto.product_id.default_code,
                        "visita": producto.name,
                        "is_audited": producto.is_audited,
                        "name_prod": producto.product_id.name,
                        "user_id": producto.planning_salas_id.auditor_id.id,
                        "planning_place": producto.planning_salas_id.id,
                        "Categoria": producto.product_id.categ_id.name,
                        "es_mueble": producto.product_id.can_be_mueble,
                        "ícono": producto.product_id.url_icon,
                        "id_estudio": producto.planning_salas_id.planning_id.planograma_id.study_id.id,
                        "Variables": variables,
                        "Fotos medidas": []
                    }
                    if producto.product_id.id not in productos_anadidos:
                        productos_anadidos.append(producto.product_id.id)
                        products.append(vals_prod)

                res = {
                    "Productos": products
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
        '/api/process_data_ean',
        type='json', auth='user', methods=['POST'], csrf=False)
    def post_process_data_ean(self, **params):
        try:

            data = params.get("data")
            posicion_x = data.get("x")
            posicion_y = data.get("y")
            categ_id = data.get("categ")
            id_sala_planificada = data.get("id_sala_planificada")
            id_mueble = data.get("id_mueble")
            list_ean_detected = data.get("ean")

            sala_planificada = request.env['planning.salas'].search([('id', '=', int(id_sala_planificada))])

            vars = []

            if sala_planificada.planning_id.planograma_id.study_id.type == '5':
                # exhibitions
                vars = request.env['variables'].search([('is_automatic', '=', True), ('tipo_estudio', '=', '5')])
            if sala_planificada.planning_id.planograma_id.study_id.type == '1':
                # osa
                pass
            if sala_planificada.planning_id.planograma_id.study_id.type == '3':
                # facing
                vars = request.env['variables'].search([('is_automatic', '=', True), ('tipo_estudio', '=', '3')])

            productos_detectados = []
            for var in vars:
                for ean_detected in list_ean_detected:
                    product_id = request.env['product.product'].search([('default_code', '=', ean_detected.get("ean"))],
                                                                       limit=1)
                    if not product_id:
                        product_id = request.env['product.product'].sudo().create({
                            "name": "Producto creado con ean %s" % ean_detected,
                            "default_code": ean_detected
                        })
                    productos_detectados.append(product_id)

                    medicion = request.env['planning.product'].search(
                        [('product_id', '=', product_id.id), ('variable_id', '=', var.id),
                         ('planning_salas_id', '=', int(id_sala_planificada))])
                    if medicion:
                        today = datetime.utcnow()
                        today = self.get_date_by_tz(today)
                        vals = {
                            'product_id': int(product_id),
                            "variable_id": var.id,
                            "planning_salas_id": int(id_sala_planificada),
                            "respuesta": ean_detected.get("veces"),
                            "date_start": today,
                            "posicion_x": posicion_x,
                            "posicion_y": posicion_y,
                            "product_padre_id": id_mueble,
                        }
                        medicion.write(vals)
                    else:
                        today = datetime.utcnow()
                        today = self.get_date_by_tz(today)
                        vals = {
                            'product_id': int(product_id),
                            "variable_id": var.id,
                            "planning_salas_id": int(id_sala_planificada),
                            "respuesta": ean_detected.get("veces"),
                            "date_start": today,
                            "posicion_x": posicion_x,
                            "posicion_y": posicion_y,
                            "product_padre_id": id_mueble,
                        }
                        planning_product = request.env['planning.product'].create(vals)
            products = []
            for variable in sala_planificada.planning_id.planograma_id.variables_estudios_ids:
                variables = []
                tipo_dato = self.get_tipo_dato(variable.variable_id.tipo_dato)

                vals_var = {
                    "id_variable": variable.variable_id.id,
                    "name_variable": variable.variable_id.name,
                    "label_visual": variable.variable_id.label_visual,
                    "Tipo_Dato": tipo_dato,
                    'valores_combo': variable.variable_id.valores_combobox.split(
                        ',') if variable.variable_id.valores_combobox else [],
                    "ícono": variable.variable_id.url_icon,
                    "logica_muestreo": variable.variable_id.logica_muestreo.expresion or '',
                    "logica_muestreo_message": variable.variable_id.logica_muestreo.error_description or '',
                    "xN1": variable.variable_id.xN1,
                    "xN2": variable.variable_id.xN2,
                    "Valor_x_Defecto_target": variable.variable_id.valor_x_defecto or '',
                    "Porc_Validación": "",
                    "Disponibilidad": "",
                    "Respuesta": "",
                    "Comentario": "",
                    "Momento_medición": "",
                    "Id_Producto_Planificado_Padre": id_mueble,
                    "Posicion_X_del_producto": posicion_x,
                    "Posicion_Y_del_producto": posicion_y,
                }
                variables.append(vals_var)

                for prod in productos_detectados:
                    vals_prod = {
                        "id_producto": prod.id,
                        "EAN": prod.default_code,
                        "visita": sala_planificada.name,
                        "name_prod": prod.name,
                        "user_id": sala_planificada.auditor_id.id,
                        "planning_place": id_sala_planificada,
                        "Categoria": prod.categ_id.name,
                        "es_mueble": prod.can_be_mueble,
                        "ícono": prod.url_icon,
                        "id_estudio": sala_planificada.planning_id.planograma_id.study_id.id,
                        "Variables": variables,
                        "Fotos medidas": []
                    }
                    products.append(vals_prod)

            try:
                return {
                    "Productos": products
                }

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
        '/api/imagen_inicial',
        type='json', auth='user', methods=['POST'], csrf=False)
    def post_imagen_inicial(self, **params):
        try:

            data = params.get("data")
            id_sala_planificada = data.get("id_sala_planificada")
            data_imagen = data.get("data_imagen")

            sala_planificada = request.env['planning.salas'].search([('id', '=', id_sala_planificada)])
            sala_planificada.write({
                "image": b'%s' % data_imagen.encode()
            })

            try:
                return {
                    "message": "Imagen actualizada"
                }

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
        '/api/upload_image_sala',
        type='json', auth='user', methods=['POST'], csrf=False)
    def upload_image_sala(self, **params):
        try:

            data = params.get("data")
            id_sala_planificada = data.get("id_sala_planificada")
            data_imagen = data.get("image_64")
            today = datetime.utcnow()
            vals = {
                "planning_sala_id": int(id_sala_planificada),
                "date": today,
                "image": b'%s' % data_imagen.encode()
            }

            imagen = request.env['photo.planning.salas'].create(vals)

            try:
                return {
                    "message": "Imagen actualizada",
                    "id": imagen.id
                }

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
        '/api/muebles_de_sala',
        type='http', auth='user', methods=['GET'], csrf=False)
    def muebles_de_sala(self, **params):
        try:
            id_sala_planificada = params["id_sala_planificada"]
            try:

                planning_products = request.env['planning.product'].search(
                    [('planning_salas_id', '=', int(id_sala_planificada)),
                     ('product_id.can_be_mueble', '=', True)])

                muebles = []
                for product in planning_products:
                    products_hijos = []
                    products_hijos_medidos = request.env['planning.product'].search(
                        [('planning_salas_id', '=', int(id_sala_planificada)),
                         ('product_padre_id', '=', product.product_id.id)])

                    for product_hijo in products_hijos_medidos:
                        tipo_dato = self.get_tipo_dato(product_hijo.variable_id.tipo_dato)
                        vals_product_hijo = {
                            "id_medicion": product_hijo.id,
                            'name': product_hijo.product_id.name,
                            "x": product_hijo.posicion_x,
                            "y": product_hijo.posicion_y,
                            "url_product_icon": product_hijo.product_id.url_icon,
                            "id_variable": product_hijo.variable_id.id,
                            "name_variable": product_hijo.variable_id.name,
                            "label_visual": product_hijo.variable_id.label_visual,
                            "Tipo_Dato": tipo_dato,
                            'valores_combo': product_hijo.variable_id.valores_combobox.split(
                                ',') if product_hijo.variable_id.valores_combobox else [],
                            "ícono": product_hijo.variable_id.url_icon,
                            "logica_muestreo": product_hijo.variable_id.logica_muestreo.expresion or '',
                            "logica_muestreo_message": product_hijo.variable_id.logica_muestreo.error_description or '',
                            "xN1": product_hijo.xN1,
                            "xN2": product_hijo.xN2,
                            "Valor_x_Defecto_target": product_hijo.valor_por_defecto or '',
                            "Porc_Validación": product_hijo.validation_perc or "",
                            "Disponibilidad": product_hijo.disponibilidad or "",
                            "Respuesta": product_hijo.respuesta,
                            "Comentario": product_hijo.comment,
                            "Momento_medición": "",
                            "Id_Producto_Planificado_Padre": product_hijo.product_padre_id.id,
                            "Posicion_X_del_producto": product_hijo.posicion_x,
                            "Posicion_Y_del_producto": product_hijo.posicion_y,
                        }
                        products_hijos.append(vals_product_hijo)
                    valores_x_cuadrado = []
                    x = y = 1
                    while x <= int(product.posicion_x):
                        y = 1
                        while y <= int(product.posicion_y):
                            # print('%s,%s' % (x, y))
                            products_hijos_medidos_posicion = request.env['planning.product'].search(
                                [('planning_salas_id', '=', int(id_sala_planificada)),
                                 ('product_padre_id', '=', product.product_id.id), ("posicion_x", '=', str(x)),
                                 ("posicion_y", '=', str(y))])

                            if products_hijos_medidos_posicion:
                                val = {
                                    "x": x,
                                    "y": y,
                                    "cant": len(products_hijos_medidos_posicion)
                                }
                            else:
                                val = {
                                    "x": x,
                                    "y": y,
                                    "cant": 0
                                }
                            valores_x_cuadrado.append(val)
                            y += 1
                        x += 1
                    print(valores_x_cuadrado)
                    vals = {
                        "id_medicion": product.id,
                        "product_id": product.product_id.id,
                        'name': product.product_id.name,
                        "x": product.posicion_x,
                        "y": product.posicion_y,
                        "url_icon": product.product_id.url_icon,
                        "productos": products_hijos,
                        "valores_por_cuadrado": valores_x_cuadrado
                    }
                    muebles.append(vals)

                res = {
                    "Productos": muebles
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
        '/api/delete_mueble',
        type='json', auth='user', methods=['POST'], csrf=False)
    def delete_mueble(self, **params):
        try:

            data = params.get("data")
            medition_id = data.get("medition_id")
            mueble = request.env['planning.product'].search([('id', "=", int(medition_id))])
            products = request.env['planning.product'].search(
                [("product_padre_id", "=", mueble.product_id.id),
                 ("planning_salas_id", "=", mueble.planning_salas_id.id)])

            for product in products:
                product.unlink()
            mueble.unlink()
            return {
                "message": "Eliminación satisfactoria"
            }

        except KeyError as e:
            msg = "Wrong values"
            res = error_response(e, msg)
            return http.Response(
                json.dumps(res),
                status=200,
                mimetype='application/json'
            )
