# -*- coding: utf-8 -*-
import json

from odoo import models, fields, api

from odoo import tools
from datetime import datetime, date
import pytz
from datetime import date, timedelta


class PriceConsistence(models.Model):
    _name = 'price.consistence'
    _auto = False

    product_id = fields.Many2one('product.product')
    planning_sala_id = fields.Many2one('planning.salas')
    variable_id = fields.Many2one('variables')

    def init(self):
        tools.drop_view_if_exists(self._cr, 'price_consistence')
        self._cr.execute(""" 
           CREATE OR REPLACE VIEW price_consistence AS ( 
               SELECT            row_number() OVER () as id,
                pl.planning_salas_id as planning_sala_id,  
                pl.product_id as product_id,
                pl.variable_id as variable_id
                FROM planning_product pl             )
    """)

    def get_date_by_tz(self, val_date, format_a=None):
        utc_timestamp = pytz.utc.localize(val_date, is_dst=False)
        context_tz = pytz.timezone('Chile/Continental')
        if not format_a:
            return utc_timestamp.astimezone(context_tz).date()
        else:
            return utc_timestamp.astimezone(context_tz).strftime(format_a).date()

    @api.model
    def retrieve_dashboard(self):
        print("retrieve data")
        today = datetime.utcnow()
        today = self.get_date_by_tz(today)
        fecha_inicio_semana_actual = today - timedelta(days=today.weekday())
        fecha_fin_semana_actual = fecha_inicio_semana_actual + timedelta(days=6)

        fecha_inicio_semana_actual_1 = fecha_inicio_semana_actual - timedelta(days=7)
        fecha_fin_semana_actual_1 = fecha_inicio_semana_actual_1 + timedelta(days=6)

        fecha_inicio_semana_actual_2 = fecha_inicio_semana_actual_1 - timedelta(days=7)
        fecha_fin_semana_actual_2 = fecha_inicio_semana_actual_2 + timedelta(days=6)

        fecha_inicio_semana_actual_3 = fecha_inicio_semana_actual_2 - timedelta(days=7)
        fecha_fin_semana_actual_3 = fecha_inicio_semana_actual_3 + timedelta(days=6)

        elements_week_actual = self.env['planning'].search(
            [('date_start', '>=', fecha_inicio_semana_actual), ('date_start', '<', fecha_fin_semana_actual)])
        elements_salas_week_actual = self.env['planning'].search(
            [('date_start', '>=', fecha_inicio_semana_actual), ('date_start', '<', fecha_fin_semana_actual)]).mapped(
            'planning_salas_ids').mapped('place_id')

        elements_week_actual_1 = self.env['planning'].search(
            [('date_start', '>=', fecha_inicio_semana_actual_1), ('date_start', '<', fecha_fin_semana_actual_1)])
        elements_salas_week_actual_1 = self.env['planning'].search(
            [('date_start', '>=', fecha_inicio_semana_actual_1),
             ('date_start', '<', fecha_fin_semana_actual_1)]).mapped(
            'planning_salas_ids').mapped('place_id')

        elements_week_actual_2 = self.env['planning'].search(
            [('date_start', '>=', fecha_inicio_semana_actual_2), ('date_start', '<', fecha_fin_semana_actual_2)])
        elements_salas_week_actual_2 = self.env['planning'].search(
            [('date_start', '>=', fecha_inicio_semana_actual_2),
             ('date_start', '<', fecha_fin_semana_actual_2)]).mapped(
            'planning_salas_ids').mapped('place_id')

        elements_week_actual_3 = self.env['planning'].search(
            [('date_start', '>=', fecha_inicio_semana_actual_3), ('date_start', '<', fecha_fin_semana_actual_3)])
        elements_salas_week_actual_3 = self.env['planning'].search(
            [('date_start', '>=', fecha_inicio_semana_actual_3),
             ('date_start', '<', fecha_fin_semana_actual_3)]).mapped(
            'planning_salas_ids').mapped('place_id')
        result = {
            'count_elements_week_actual': len(elements_week_actual),
            'count_elements_week_actual_1': len(elements_week_actual_1),
            'count_elements_week_actual_2': len(elements_week_actual_2),
            'count_elements_week_actual_3': len(elements_week_actual_3),

            'count_elements_salas_week_actual': len(elements_salas_week_actual),
            'count_elements_salas_week_actual_1': len(elements_salas_week_actual_1),
            'count_elements_salas_week_actual_2': len(elements_salas_week_actual_2),
            'count_elements_salas_week_actual_3': len(elements_salas_week_actual_3),
        }

        return result
