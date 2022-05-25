# -*- coding: utf-8 -*-

from odoo import models, fields, api


# https://maps.googleapis.com/maps/api/geocode/json?latlng=44.4647452,7.3553838&key=YOUR_API_KEY
class Geo(models.Model):
    _name = 'geo'
    _description = "Geolocalizacion"

    name = fields.Char(string="Name")
    lat = fields.Char(string="Latitude")
    long = fields.Char(string="Longitude")


class Section(models.Model):
    _name = 'section'
    _description = "Seccion"

    name = fields.Char(string="Section")


class Area(models.Model):
    _name = 'area'
    _description = "Area"

    name = fields.Char(string="Area")


class Parameters(models.Model):
    _name = 'parameters'
    _description = "Parametros"

    name = fields.Char(string="Parameters")
    detail = fields.Char(string="Details")


class Comunas(models.Model):
    _name = 'comunas'
    _description = "Comunas"
    name = fields.Char(string="Name")
    state_id = fields.Many2one('res.country.state', string="Region", domain=[('country_id', '=', 46)])


class Salas(models.Model):
    _name = 'salas'
    _description = "Salas"

    name = fields.Char(string="Name")
    address = fields.Char(string="Address")
    folio = fields.Char(string="Folio")
    image = fields.Binary(string="Imagen")
    url_image = fields.Char(string="Url imagen", compute='compute_url_image')
    comuna_id = fields.Many2one('comunas', string="Comuna")
    state_id = fields.Many2one('res.country.state', string="Region", domain=[('country_id', '=', 46)])
    lat = fields.Char(string="Latitud")
    long = fields.Char(string="Longitud")
    geo = fields.Many2one('geo', string="Geolocalization ")

    @api.depends('image')
    def compute_url_image(self):
        print("url")
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        for rec in self:
            image_url_1920 = base_url + '/web/image?' + 'model=salas&id=' + str(rec.id) + '&field=image'
            rec.url_image = image_url_1920


class PhotoSupi(models.Model):
    _name = 'photos.supi'
    _description = "Photo Supi"

    name = fields.Char(string="Name")
    image = fields.Binary(string="Image")
    category = fields.Char(string="Category")


class Variables(models.Model):
    _name = 'variables'
    _description = "Variables"

    name = fields.Char(string="Name")
    id_variable = fields.Char(string="ID VARIABLE")
    valores_combobox = fields.Char(string="Valores combobox")
    tipo_dato = fields.Selection(
        [('2', 'Price'),
         ('4', 'Carteleria'),
         ('3', 'Facing'),
         ('1', 'OSA'),
         ('5', 'Exhibitions')],
        string='Tipo de estudio')
    image = fields.Binary(string="Image")
    icon = fields.Binary(string="Icono")
    study_id = fields.Many2one("study", string="Estudio")


class Muebles(models.Model):
    _name = "muebles"
    _description = "Muebles"

    name = fields.Char(string="Nombre")
    category = fields.Char(string="Categoría")
    marca = fields.Char(string="Marca")
    puerta = fields.Integer(string="Puerta")
    division = fields.Integer(string="División")
    bandeja = fields.Integer(string="Bandeja")
    product_id = fields.Many2one('product.product', string="Producto")


class StudyType(models.Model):
    _name = "study.type"
    _description = "Tipo estudios"

    name = fields.Char(string="Name")


class StudyFrecuency(models.Model):
    _name = "study.frecuency"
    _description = "Frecuencia del estudio"

    name = fields.Char(string="Name")


class Study(models.Model):
    _name = "study"
    _description = "Estudios"

    name = fields.Char(string="Name")
    # variable_id = fields.Many2one('variables', string="Variable")
    tipo_estudio = fields.Many2one('study.type')
    naturaleza = fields.Selection(
        [('0', 'Productos'),
         ('1', 'Muebles sin productos'),
         ('2', 'Muebles con productos'),
         ('3', 'Salas')],
        string='Naturaleza del estudio')
    frecuency = fields.Many2one('study.frecuency')


class Quiz(models.Model):
    _name = "quiz"
    _description = "Quiz"

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
    _description = "Planificacion"

    name = fields.Char(string="Cadena")
    channel = fields.Char(string="Canal")
    planograma_id = fields.Many2one("planograma", string="Planograma")
    date_start = fields.Date('Date start')
    date_end = fields.Date('Date end')
    description = fields.Char(size=100, string="Descripción")
    user_id = fields.Many2one('res.users', string="Usuario")
    state = fields.Selection([
        ('ready', 'Listo'),
        ('proceeding', 'En proceso'),
        ('cancel', 'Cancelado'),
        ('done', 'Hecho'),
    ], string='Estado', help='Estados de la planificacion', default='ready')

    # study_id = fields.Many2one("study", string="Estudio")
    # product_id = fields.Many2one("product.product", string="Producto")
    # place_id = fields.Many2one("salas", string="Sala")
    # variable_id = fields.Many2one("variable", string="Variable")
    # comuna_id = fields.Many2one('comunas', string="Comuna")
    # state_id = fields.Many2one('res.country.state', string="Region", domain=[('country_id', '=', 46)])
    # tiene_cartel = fields.Boolean(string="Tiene cartel?")
    # mecanica = fields.Boolean(string="Mecánica")
    # result = fields.Integer(string="Resultado")


class PlanningSalas(models.Model):
    _name = "planning.salas"
    _rec_name = 'planning_id'
    _description = "Salas planificadas"

    planning_id = fields.Many2one('planning', string="Planning")
    place_id = fields.Many2one('salas', string="Sala")
    auditor_id = fields.Many2one('res.users', string="Auditor")
    coordinator_id = fields.Many2one('res.users', string="Coordinador")
    state = fields.Selection([
        ('ready', 'Listo'),
        ('proceeding', 'En proceso'),
        ('cancel', 'Cancelado'),
        ('done', 'Hecho'),
    ], string='Estado', help='Estado', default='ready')


class PlanningProducts(models.Model):
    _name = "planning.product"
    _description = "Productos planificados"

    planning_salas_id = fields.Many2one('planning.salas', string="Sala planificada")
    product_id = fields.Many2one('product.product', string="Producto")
    variable_id = fields.Many2one('variable', string="Variable")
    valor_por_defecto = fields.Char("Valor por defecto")


class StudiesDone(models.Model):
    _name = "studies.done"
    _description = "Estudios realizados"

    planning_salas_id = fields.Many2one('planning.salas', string="Sala planificada")
    quizs_ids = fields.One2many('quiz.result', 'studie_done_id', string='Quizs', copy=True)
    image = fields.Binary(string="Foto inicial")


class PlanningStudies(models.Model):
    _name = "planning.studies"
    _description = "Estudios planificados"

    study_id = fields.Many2one('study', string="Study")
    planning_id = fields.Many2one('planning', string="Planning")
    product_id = fields.Many2one('product.product', string="Product")
    auditor = fields.Many2one('res.users', string="Auditor")


class Planograma(models.Model):
    _name = "planograma"
    _description = "Planograma"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(related='partner_id.name')
    date_start = fields.Date('Date start')
    date_end = fields.Date('Date end')
    partner_id = fields.Many2one("res.partner", string="Cliente")
    study_id = fields.Many2one('study', string="Study")
    user_id = fields.Many2one('res.users', string="Usuario")
    description = fields.Char(size=100, string="Descripción")
    salas_planograma_ids = fields.One2many('salas.planograma', 'planograma_id', string='Salas del planograma',
                                           copy=True)
    variables_estudios_ids = fields.One2many('variables.studies', 'planograma_id', string='Variables de estudio',
                                             copy=True)


class VariablesEstudios(models.Model):
    _name = "variables.studies"
    _description = "Variables de estudios"
    _rec_name = 'variable_id'

    planograma_id = fields.Many2one("planograma", string="Planograma")
    variable_id = fields.Many2one('variables', string="Variable")


class SalasPlanograma(models.Model):
    _name = "salas.planograma"
    _description = "Salas del planograma"

    planograma_id = fields.Many2one("planograma", string="Planograma")
    place_id = fields.Many2one('salas', string="Sala")
    muebles_ids = fields.Many2many('muebles')
