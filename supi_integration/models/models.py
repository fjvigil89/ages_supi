# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class supi_integration(models.Model):
#     _name = 'supi_integration.supi_integration'
#     _description = 'supi_integration.supi_integration'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
