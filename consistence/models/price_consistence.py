# -*- coding: utf-8 -*-
import json

from odoo import models, fields, api


class PriceConsistence(models.Model):
    _name = 'price.consistence'

    name = fields.Char(string="Nombre")
