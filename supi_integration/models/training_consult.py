# -*- coding: utf-8 -*-

from odoo import models, fields, api


class TrainingConsult(models.Model):
    _name = "photo.param.upload"

    image_id = fields.Many2one('photos.supi', string="Photo")
    user_id = fields.Many2one('res.users', string="User")
    param_id = fields.Many2one('parameters', string="Parameters")
    result = fields.Text(string="Result")
    date_send = fields.Datetime('Date send')


