# -*- coding: utf-8 -*-
import json

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

    label_visual = fields.Char(string="Label visual")
    id_variable = fields.Char(string="ID VARIABLE")
    valores_combobox = fields.Char(string="Valores combobox")
    tipo_estudio = fields.Selection(
        [('2', 'Price'),
         ('3', 'Facing'),
         ('1', 'OSA'),
         ('4', 'Equipos de frio'),
         ('5', 'Exhibitions')],
        string='Tipo de estudio')

    tipo_dato = fields.Selection(
        [('1', 'Texto'),
         ('2', 'Int'),
         ('3', 'Double'),
         ('4', 'Bool'),
         ('5', 'Select'),
         ('6', 'Price')],
        string='Tipo de dato')
    image = fields.Binary(string="Image")
    icon = fields.Binary(string="Icono")
    study_id = fields.Many2one("study", string="Estudio")

    def name_get(self):
        result = []
        for variable in self:
            result.append((variable.id, '%s - %s' % (
                variable.label_visual, dict(self._fields['tipo_estudio'].selection).get(variable.tipo_estudio))))
        return result


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
    type = fields.Selection(
        [('2', 'Price'),
         ('3', 'Facing'),
         ('1', 'OSA'),
         ('4', 'Equipos de frio'),
         ('5', 'Exhibitions')],
        string='Tipo de estudio')
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
    planning_salas_ids = fields.One2many('planning.salas', 'planning_id', string="Salas planificadas")
    state = fields.Selection([
        ('ready', 'Listo'),
        ('proceeding', 'En proceso'),
        ('cancel', 'Cancelado'),
        ('done', 'Hecho'),
    ], string='Estado', help='Estados de la planificacion', default='ready')


class PlanningSalas(models.Model):
    _name = "planning.salas"
    _rec_name = 'planning_id'
    _description = "Salas planificadas"

    planning_id = fields.Many2one('planning', string="Planning")
    place_id = fields.Many2one('salas', string="Sala")
    auditor_id = fields.Many2one('res.users', string="Auditor")
    coordinator_id = fields.Many2one('res.users', string="Coordinador")
    specifications = fields.Char(size=100, string="Especificaciones")
    comment = fields.Char(size=100, string="Comentario")
    planning_products_ids = fields.One2many('planning.product', 'planning_salas_id', string="Productos")
    image = fields.Binary(string="Foto inicial")
    quizs_ids = fields.One2many('quiz.result', 'planning_salas_id', string='Quizs', copy=True)
    state = fields.Selection([

        ('prepared', 'Preparado'),
        ('done', 'Realizado'),
        ('no_done', 'No realizado'),
    ], string='Estado', help='Estado', default='prepared')

    def name_get(self):
        result = []
        for salas in self:
            result.append((salas.id, '%s - %s- %s' % (salas.place_id.name, salas.auditor_id.name,
                                                      dict(self._fields['state'].selection).get(
                                                          salas.state))))
        return result


class PlanningProducts(models.Model):
    _name = "planning.product"
    _description = "Productos planificados"

    planning_salas_id = fields.Many2one('planning.salas', string="Sala planificada")
    product_id = fields.Many2one('product.product', string="Producto")
    product_ids = fields.Many2many('product.product')
    variable_id = fields.Many2one('variables', string="Variable")
    variable_ids = fields.Many2many('variables', string="Variables")
    valor_por_defecto = fields.Char("Valor por defecto")
    validation_perc = fields.Char("% Validación")
    disponibilidad = fields.Char("Disponibilidad")
    respuesta = fields.Char("Respuesta")
    comment = fields.Char("Comentario")
    posicion_x = fields.Char("Posicion X del producto")
    posicion_y = fields.Char("Posicion Y del producto")
    date_start = fields.Date(string='Momento de medicion')
    product_padre_id = fields.Many2one('product.product', string="Producto padre")

    def name_get(self):
        result = []
        for product in self:
            name = ''
            for prod in product.product_ids:
                name += str(prod.name)
            result.append((product.id, '%s - %s' % (name, product.variable_id.label_visual)))
        return result


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
    study_id_naturaleza = fields.Char(string="Naturaleza", default='0')
    study_id_type = fields.Char(string="Type")

    def name_get(self):
        result = []
        for planograma in self:
            result.append((planograma.id, '%s-%s' % (planograma.partner_id.name, planograma.study_id.name)))
        return result

    @api.onchange('study_id')
    def onchange_study_id(self):
        if self.study_id:
            if self.study_id.naturaleza:
                self.study_id_naturaleza = self.study_id.naturaleza
            else:
                self.study_id_naturaleza = '0'
            if self.study_id.type:
                self.write({'study_id_type': self.study_id.type})
            else:
                self.write({'study_id_type': ''})

        self.salas_planograma_ids = False

    def generate_planning(self):
        vals = {
            "date_start": self.date_start,
            "date_end": self.date_end,
            "user_id": self.env.user.id,
            "planograma_id": self.id,
            "name": self.partner_id.name,
            "description": self.description,
        }
        planning_id = self.env['planning'].create(vals)

        for line in self.salas_planograma_ids:
            vals = {
                "planning_id": planning_id.id,
                "place_id": line.place_id.id,
                "auditor_id": self.user_id.id,
                "coordinator_id": self.user_id.id,
            }
            planning_sala_id = self.env['planning.salas'].create(vals)
            vals = {
                "planning_salas_id": planning_sala_id.id,
                "product_ids": [(6, 0, line.muebles_ids.ids)],
                "variable_ids": [(6, 0, self.variables_estudios_ids.ids)],
            }
            self.env['planning.product'].create(vals)


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
    product_id_domain = fields.Char(
        compute="_compute_product_id_domain",
        readonly=True,
        store=False,
    )
    muebles_ids = fields.Many2many('product.product')

    @api.onchange('place_id', 'planograma_id')
    def _compute_product_id_domain(self):
        for rec in self:
            print(rec.planograma_id.study_id_naturaleza)
            if rec.planograma_id.study_id_naturaleza == '0':
                rec.product_id_domain = json.dumps(
                    [('can_be_mueble', '=', False)]
                )
            if rec.planograma_id.study_id_naturaleza == '1':
                rec.product_id_domain = json.dumps(
                    [('can_be_mueble', '=', True),
                     ('product_ids', '=', False)]
                )
            if rec.planograma_id.study_id_naturaleza == '2':
                rec.product_id_domain = json.dumps(
                    [('can_be_mueble', '=', True),
                     ('product_ids', '!=', False)]
                )
