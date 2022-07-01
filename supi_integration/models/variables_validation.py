# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-

from odoo import models, fields


class ValidacionVariables(models.Model):
    _name = 'validacion.variables'

    name = fields.Char(string="Label")
    expresion = fields.Char(string="Expresión")
    error_description = fields.Char(string="Descripción del error")
