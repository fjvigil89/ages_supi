# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError


class ProductProduct(models.Model):
    _inherit = 'product.product'

    pack = fields.Integer(string="Paquete")

    def unlink(self):
        if self.id in [self.env.ref('supi_integration.product_sala').id,
                       self.env.ref('supi_integration.CheckOUT').id,
                       self.env.ref('supi_integration.Isla').id,
                       self.env.ref('supi_integration.Gondola').id,
                       self.env.ref('supi_integration.EQFRIO').id,
                       ]:
            raise UserError("El producto %s no puede ser eliminado porque es una variable del sistema" % self.name)

        return super(ProductProduct, self).unlink()


class ProductTemplate(models.Model):
    _inherit = "product.template"

    can_be_mueble = fields.Boolean(string="Puede ser mueble")
    product_id = fields.Many2one("product.template")
    # planning_product = fields.Many2one("planning.product")
    product_ids = fields.One2many("product.template", 'product_id')
    categories_ids = fields.One2many("product.partner.category", 'product_id')
    partner_id = fields.Many2one("res.partner", string="Cliente")
    url_icon = fields.Char(string="Url icono", compute='compute_url_icon')

    @api.depends('image_1920')
    def compute_url_icon(self):
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        for rec in self:
            image_url_1920 = base_url + '/web/image?' + 'model=product.product&id=' + str(rec.id) + '&field=image_1920'
            rec.url_icon = image_url_1920


class ProductPartnerCategories(models.Model):
    _name = "product.partner.category"

    product_id = fields.Many2one("product.template", string="Producto")
    partner_id = fields.Many2one("res.partner", string="Cliente")
    category = fields.Char(string="Categoria")
