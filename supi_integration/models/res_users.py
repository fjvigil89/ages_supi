# -*- coding: utf-8 -*-

from odoo import models, fields, api

class ResUsers(models.Model):
    _inherit = 'res.users'

    geo = fields.Many2one('geo', string="Geolocalizacion")
    user_type = fields.Selection([
        ('client', 'Client'),
        ('auditor', 'Auditor'),
        ('auditor_field', 'Field auditor'),
    ], string='User type', help='Users type in system', default='auditor')
    rut = fields.Char(string="RUT")
    phone = fields.Char(string="Telefono")

