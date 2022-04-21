# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api
from odoo.exceptions import ValidationError
from xlrd.biffh import XLRDError
import base64
import dateutil.parser
import xlrd
from datetime import datetime

IDs_COLUMNS = ['ID_VARIABLE', 'ID_ESTUDIOSALA', 'ID_PRODUCTO', 'FECHA_INICIO', 'FECHA_FIN', 'VALOR_HISTORICO',
               'PORCENTAJE_VALIDACION', 'COMENTARIO', 'AUDITOR']


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

    def convert_excel_date_to_datetime(self, excel_date):
        dt = datetime.fromordinal(datetime(1900, 1, 1).toordinal() + excel_date - 2)
        return dt

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
            index_id_variable = ''
            index_id_estudiosala = ''
            index_id_producto = ''
            index_fecha_inicio = ''
            index_fecha_fin = ''
            index_valor_historico = ''
            index_porcentaje_validacion = ''
            index_comentario = ''
            index_audirtor = ''
            ws = wb.sheet_by_index(0)

            for col_index in range(ws.ncols):
                # Obtenniendo los id columna de los encabezados
                if ws.cell(0, col_index).value == 'ID_VARIABLE':
                    index_id_variable = col_index
                if ws.cell(0, col_index).value == 'ID_ESTUDIOSALA':
                    index_id_estudiosala = col_index
                if ws.cell(0, col_index).value == 'ID_PRODUCTO':
                    index_id_producto = col_index
                if ws.cell(0, col_index).value == 'FECHA_INICIO':
                    index_fecha_inicio = col_index
                if ws.cell(0, col_index).value == 'FECHA_FIN':
                    index_fecha_fin = col_index
                if ws.cell(0, col_index).value == 'VALOR_HISTORICO':
                    index_valor_historico = col_index
                if ws.cell(0, col_index).value == 'PORCENTAJE_VALIDACION':
                    index_porcentaje_validacion = col_index
                if ws.cell(0, col_index).value == 'COMENTARIO':
                    index_comentario = col_index
                if ws.cell(0, col_index).value == 'AUDITOR':
                    index_audirtor = col_index

            # RECORRER LOS ROW PARA CREAR PLANOGRAMA!
            for row_index in range(ws.nrows):
                print(row_index)
                if row_index > 0:
                    variable_id = self.env['variables'].search(
                        [('name', '=', str(int(ws.cell(row_index, index_id_variable).value)))])
                    product_id = self.env['product.product'].search(
                        [('default_code', '=', str(int(ws.cell(row_index, index_id_producto).value)))])
                    study_id = self.env['study'].search(
                        [('name', '=', str(int(ws.cell(row_index, index_id_estudiosala).value))),
                         ('variable_id.name', '=', variable_id.name)])
                    date_start = self.convert_excel_date_to_datetime(int(ws.cell(row_index, index_fecha_inicio).value))
                    date_end = self.convert_excel_date_to_datetime(int(ws.cell(row_index, index_fecha_fin).value))
                    valor_historico = ws.cell(row_index, index_valor_historico).value
                    porcentaje_validacion = ws.cell(row_index, index_porcentaje_validacion).value
                    comment = ws.cell(row_index, index_comentario).value
                    user_id = self.env['res.users'].search(
                        [('login', '=', ws.cell(row_index, index_audirtor).value)])

                    if not study_id:
                        self.observations = u"Oops!  Por favor, verifique exista el estudio a importar en el fichero"
                        return
                    self.env['planograma'].create({
                        'date_start': date_start,
                        'date_end': date_end,
                        'product_id': product_id.id,
                        'study_id': study_id.id,
                        'historic_value': valor_historico,
                        'perc_validation': porcentaje_validacion,
                        'user_id': user_id.id,
                        'comment': comment
                    })
            self.write({'state': 'imported'})
            if self.observations != '':
                self.observations = 'Los datos se han importado correctamente. Navegue por el menú Datos Secundarios/Planogramas para consultarlos'
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

        except XLRDError:
            self.observations = u"Oops!  Existen problemas de incompatibilidad en los datos del documento"

    def close(self):
        return {'type': 'ir.actions.act_window_close'}
