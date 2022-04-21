# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api
from odoo.exceptions import ValidationError
from xlrd.biffh import XLRDError
import base64
import dateutil.parser
import xlrd

IDs_COLUMNS = ['ID_VARIABLE', 'ID_ESTUDIOSALA', 'ID_PRODUCTO', 'FECHA_INICIO', 'FECHA_FIN', 'VALOR_HISTORICO',
               'PORCENTAJE_VALIDACION', 'COMENTARIO', 'AUDIRTOR']


class ImportPlanograma(models.TransientModel):
    _name = 'import.planograma'

    name = fields.Char(string="Nombre", default='Planificación')

    state = fields.Selection([
        ('draft', 'Borrador'),
        ('checked', 'Validado'),
        ('imported', 'Importado')], default='draft', track_visibility='onchange',
        string='Estado', required=True, readonly=True, index=True)
    filename = fields.Char(string="Nombre", default='')
    data_file = fields.Binary('File data',
                              help='File(xls)', attachment=True)
    observations = fields.Char(string="Observaciones")

    @api.onchange('data_file')
    def onchange_data_file(self):
        self.observations = ''

    def check(self):
        if not self.data_file:
            raise ValidationError('Por favor, debe seleccionar un fichero')
        message = ''
        try:
            wb = xlrd.open_workbook(file_contents=base64.decodebytes(self.data_file))
            ws = wb.sheet_by_index(0)

            if ws.ncols != 9:
                message += 'Por favor, revise el documento, se detectó un error en la cantidad de columnas del documento'

            for col_index in range(ws.ncols):

                if ws.cell(0, col_index).value not in IDs_COLUMNS:
                    message += '%s %s' % (
                        'Por favor, verifique que los nombres de las columnas estén entre los siguientes',
                        str(IDs_COLUMNS))

            # id_variable, id_estudiosala, \
            # id_producto, fecha_inicio, fecha_fin, \
            # valor_historico, porcentaje_historico, comentario, auditor = ''
            if message != '':
                self.observations = message
            else:
                self.observations = 'Todo parece correcto.'
                self.write({'state': 'checked'})
            if wb:
                pass


        except XLRDError:
            self.observations = u"Oops!  Existen problemas de incompatibilidad o de formato de estructura de la plantilla..."
        ctx = dict(self._context)
        mod_obj = self.env['ir.model.data']
        model_data_ids = mod_obj.search([('model', '=', 'ir.ui.view'),
                                         ('name', '=', 'form_to_import_planograma')])
        resource_id = model_data_ids.read(fields=['res_id'])[0]['res_id']

        return {'name': ('Planograma'),
                'context': ctx,
                'view_mode': 'form',
                'res_model': 'import.planograma',
                'views': [(resource_id, 'form')],
                'res_id': self.id,
                'type': 'ir.actions.act_window',
                'target': 'new',
                }

    def go_back(self):
        self.write({'state': 'draft'})
        ctx = dict(self._context)
        mod_obj = self.env['ir.model.data']
        model_data_ids = mod_obj.search([('model', '=', 'ir.ui.view'),
                                         ('name', '=', 'form_to_import_planograma')])
        resource_id = model_data_ids.read(fields=['res_id'])[0]['res_id']

        return {'name': ('Planograma'),
                'context': ctx,
                'view_mode': 'form',
                'res_model': 'import.planograma',
                'views': [(resource_id, 'form')],
                'res_id': self.id,
                'type': 'ir.actions.act_window',
                'target': 'new',
                }

    def import_data(self):
        try:
            wb = xlrd.open_workbook(file_contents=base64.decodebytes(self.data_file))


        except XLRDError:
            self.observations = u"Oops!  Existen problemas de incompatibilidad en los datos del documento"
