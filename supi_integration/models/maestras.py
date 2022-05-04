# -*- coding: utf-8 -*-

from odoo import models, fields, api


# https://maps.googleapis.com/maps/api/geocode/json?latlng=44.4647452,7.3553838&key=YOUR_API_KEY
class Geo(models.Model):
    _name = 'geo'

    name = fields.Char(string="Name")
    lat = fields.Char(string="Latitude")
    long = fields.Char(string="Longitude")


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


class Comunas(models.Model):
    _name = 'comunas'
    name = fields.Char(string="Name")
    state_id = fields.Many2one('res.country.state', string="Region", domain=[('country_id', '=', 46)])


class Salas(models.Model):
    _name = 'salas'

    name = fields.Char(string="Name")
    address = fields.Char(string="Address")
    folio = fields.Char(string="Folio")
    comuna_id = fields.Many2one('comunas', string="Comuna")
    state_id = fields.Many2one('res.country.state', string="Region", domain=[('country_id', '=', 46)])
    geo = fields.Many2one('geo', string="Geolocalization ")


class PhotoSupi(models.Model):
    _name = 'photos.supi'

    name = fields.Char(string="Name")
    image = fields.Binary(string="Image")
    category = fields.Char(string="Category")


class Variables(models.Model):
    _name = 'variables'

    name = fields.Char(string="Name")
    id_variable = fields.Char(string="ID VARIABLE")
    type = fields.Selection(
        [('price', 'Price'), ('pop', 'Pop'), ('cold_equipment', 'Cold Equipment'), ('facing', 'Facing'),
         ('sovi', 'Sovi'), ('osa', 'OSA'),
         ('exhibitions', 'Exhibitions')],
        string='Tipo de estudio', default='price')
    image = fields.Binary(string="Image")


class Study(models.Model):
    _name = "study"

    name = fields.Char(string="Name")
    variable_id = fields.Many2one('variables', string="Variable")


class Quiz(models.Model):
    _name = "quiz"

    name = fields.Char(string="Name")
    study_id = fields.Many2one('study', string="Study")
    question = fields.Char(string="Question")
    correct_answer = fields.Char(string="Correct answer")
    answer1 = fields.Char(string="Answer 1")
    answer2 = fields.Char(string="Answer 2")
    study_type = fields.Selection(
        [('price', 'Price'), ('pop', 'Pop'), ('cold_equipment', 'Cold Equipment'), ('facing', 'Facing'),
         ('sovi', 'Sovi'), ('osa', 'OSA'),
         ('exhibitions', 'Exhibitions')],
        string='Tipo de estudio', default='price')
    partner_id = fields.Many2one('res.partner', string="Partner")


class Planning(models.Model):
    _name = "planning"

    place_id = fields.Many2one('salas', string="Place")
    coordinator_id = fields.Many2one('res.users', string="Coordinator")
    state_id = fields.Many2one('res.country.state', string="Commune")
    region = fields.Char(string="Region")
    address = fields.Char(string="Address")
    channel = fields.Char(string="Channel")
    name = fields.Char(string="Chain")
    geo = fields.Many2one('geo', string="Geolocalization ")


class PlanningStudies(models.Model):
    _name = "planning.studies"

    study_id = fields.Many2one('study', string="Study")
    planning_id = fields.Many2one('planning', string="Planning")
    product_id = fields.Many2one('product.product', string="Product")
    auditor = fields.Many2one('res.users', string="Auditor")


class Planograma(models.Model):
    _name = "planograma"

    name = fields.Char(related='product_id.name')
    state = fields.Selection([
        ('ready', 'Listo'),
        ('in_process', 'En proceso'),
        ('done', 'Hecho'),
    ], string='Estado', default='ready')
    date_start = fields.Date('Date start')
    date_end = fields.Date('Date end')
    place_id = fields.Many2one('salas', string="Place")
    study_id = fields.Many2one('study', string="Study")
    product_id = fields.Many2one('product.product', string="Product")
    section_id = fields.Many2one('section', string="Section")
    area_id = fields.Many2one('area', string="Area")
    target = fields.Char(size=100, string="Target")
    base = fields.Char(size=100, string="Base")
    comment = fields.Char(size=100, string="Comment")
    perc_validation = fields.Float(string="Validation %")
    historic_value = fields.Float(string="Historic value")
    user_id = fields.Many2one('res.users', string='Auditor', default=lambda self: self.env.user)
    quebrado = fields.Boolean(string="Quebrado", default=False)
    cautivo = fields.Boolean(string="Cautivo", default=False)
    c_erroneo = fields.Boolean(string="Código erróneo", default=False)
    cartel = fields.Boolean(string="Cartel", default=False)
    image = fields.Image("Imagen")
