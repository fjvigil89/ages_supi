# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Section(models.Model):
    _name = 'section'

    name = fields.Char(string="Section")


class Area(models.Model):
    _name = 'area'

    name = fields.Char(string="Area")


class Parameters(models.Model):
    _name = 'parameters'

    name = fields.Char(string="Parameters")
    detail = fields.Char(string="Details")


class Salas(models.Model):
    _name = 'salas'

    name = fields.Char(string="Name")
    address = fields.Char(string="Address")
    lat = fields.Char(string="Latitude")
    long = fields.Char(string="Longitude")


class PhotoSupi(models.Model):
    _name = 'photos.supi'

    name = fields.Char(string="Name")
    image = fields.Binary(string="Image")
    category = fields.Char(string="Category")


class Variables(models.Model):
    _name = 'variables'

    name = fields.Char(string="Name")
    type = fields.Selection([
        ('osa', 'OSA (Presence)'),
        ('price', 'Price'),
        ('facing_sovi', 'Facing Sovi'),
        ('posters', 'Posters'),
        ('display', 'Display'),
    ], string='User type', help='Variables of study in system')
    image = fields.Binary(string="Image")
