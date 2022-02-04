# -*- coding: utf-8 -*-

from odoo import models, fields, api


# 51944007   9A 16500
# 53251445   53543187 huawei

class ResUsers(models.Model):
    _inherit = 'res.users'

    lat = fields.Char(string="Latitude")
    long = fields.Char(string="Longitude")
    user_type = fields.Selection([
        ('client', 'Client'),
        ('auditor', 'Auditor'),
        ('auditor_field', 'Field auditor'),
    ], string='User type', help='Users type in system', default='auditor')
