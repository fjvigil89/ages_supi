# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ProductProduct(models.Model):
    _inherit = 'product.product'

    pack = fields.Integer(string="Paquete")


class ProductTemplate(models.Model):
    _inherit = "product.template"

    can_be_mueble = fields.Boolean(string="Puede ser mueble")
    product_id = fields.Many2one("product.template")
    product_ids = fields.One2many("product.template", 'product_id')
    partner_id = fields.Many2one("res.partner", string="Cliente")
