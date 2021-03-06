# -*- coding: utf-8 -*-
import json
import random

from odoo import models, fields, api
from odoo.exceptions import UserError


# -*- coding: utf-8 -*-


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

    comuna_id = fields.Many2one('comunas', string="Comuna")
    state_id = fields.Many2one('res.country.state', string="Region", domain=[('country_id', '=', 46)])
    lat = fields.Char(string="Latitud")
    long = fields.Char(string="Longitud")
    geo = fields.Many2one('geo', string="Geolocalization ")
    url_image = fields.Char(string="Url imagen", compute='compute_url_image')

    def name_get(self):
        result = []
        for salas in self:
            result.append((salas.id, '[%s] %s' % (
                salas.folio, salas.name)))
        return result

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

    consistencia = fields.Boolean(string="Medir consistencia", default=False)
    label_visual = fields.Char(string="Label visual")
    name = fields.Char(string="Nombre")
    id_variable = fields.Char(string="ID VARIABLE")
    valores_combobox = fields.Char(string="Valores combobox")
    scope = fields.Selection(
        [('1', 'Mueble'),
         ('0', 'Producto'),
         ('2', 'Sala')],
        string='Naturaleza')
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
         ('6', 'Price'),
         ('7', 'Radiobutton'),
         ('8', 'Date'),
         ('9', 'Mec??nica'),
         ('10', 'Estado'),
         ('11', 'Promoci??n'),
         ],
        string='Tipo de dato')
    image = fields.Binary(string="Image")
    icon = fields.Binary(string="Icono")
    study_id = fields.Many2one("study", string="Estudio")
    url_icon = fields.Char(string="Url icono", compute='compute_url_icon')
    xN1 = fields.Integer(string="xN1")
    xN2 = fields.Integer(string="xN2")
    is_automatic = fields.Boolean(default=False, string="Es automatica?")
    valor_x_defecto = fields.Char(string="Valor por defecto")
    variable_que_depende_id = fields.Many2one("variables", string="Variable de la cual depende la variable actual")
    logica_muestreo = fields.Many2one('validacion.variables', string="L??gica de validaci??n",
                                      help="Este campo se usar?? para validar una variable respecto a otra.")
    detalle1_respuesta = fields.Char("Detalle 1")
    detalle2_respuesta = fields.Char("Detalle 2")
    detalle3_respuesta = fields.Char("Detalle 3")
    detalle4_respuesta = fields.Char("Detalle 4")


    @api.depends('icon')
    def compute_url_icon(self):
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        for rec in self:
            image_url_1920 = base_url + '/web/image?' + 'model=variables&id=' + str(rec.id) + '&field=icon'
            rec.url_icon = image_url_1920

    def unlink(self):
        if self.id in [self.env.ref('supi_integration.cuantas_veces_present_facing').id,
                       self.env.ref('supi_integration.cuantas_veces_present_exhibitions').id
                       ]:
            raise UserError("La variable %s no puede ser eliminado porque es una variable del sistema" % self.name)

        return super(Variables, self).unlink()

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
    category = fields.Char(string="Categor??a")
    marca = fields.Char(string="Marca")
    puerta = fields.Integer(string="Puerta")
    division = fields.Integer(string="Divisi??n")
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
        [('2', 'Price'),
         ('3', 'Facing'),
         ('1', 'OSA'),
         ('4', 'Equipos de frio'),
         ('5', 'Exhibitions')],
        string='Tipo de estudio')
    partner_id = fields.Many2one('res.partner', string="Partner")


class Planning(models.Model):
    _name = "planning"
    _description = "Planificacion"

    name = fields.Char(string="Consecutivo")
    channel = fields.Char(string="Canal")
    planograma_id = fields.Many2one("planograma", string="Planograma")
    date_start = fields.Date('Date start')
    date_end = fields.Date('Date end')
    description = fields.Char(size=100, string="Descripci??n")
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
    _description = "Salas planificadas"

    planning_id = fields.Many2one('planning', string="Planning")
    place_id = fields.Many2one('salas', string="Sala")
    name = fields.Char("Consecutivo")
    auditor_id = fields.Many2one('res.users', string="Auditor")
    coordinator_id = fields.Many2one('res.users', string="Coordinador")
    specifications = fields.Char(size=100, string="Especificaciones")
    comment = fields.Char(size=100, string="Comentario")
    planning_products_ids = fields.One2many('planning.product', 'planning_salas_id', string="Productos")
    image = fields.Binary(string="Foto inicial")
    id_quiz_1 = fields.Many2one('quiz', string="Id Quiz 1")
    answer_quiz_1 = fields.Char("Respuesta 1")
    id_quiz_2 = fields.Many2one('quiz', string="Id Quiz 2")
    answer_quiz_2 = fields.Char("Respuesta 2")
    id_quiz_3 = fields.Many2one('quiz', string="Id Quiz 3")
    answer_quiz_3 = fields.Char("Respuesta 3")
    mediciones_ids = fields.One2many('planning.product', 'planning_salas_id', string="Mediciones")
    categories_ids = fields.Many2many('product.category')
    state = fields.Selection([
        ('prepared', 'Preparado'),
        ('done', 'Realizado'),
        ('no_done', 'No realizado'),
    ], string='Estado', help='Estado', default='prepared')
    images_ids = fields.One2many('photo.planning.salas', 'planning_sala_id')

    @api.model
    def create(self, vals):
        if not vals.get('name'):
            vals['name'] = self.env['ir.sequence'].next_by_code('planning.salas')
        return super(PlanningSalas, self).create(vals)

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

    @api.depends("planning_salas_id")
    def _compute_studio(self):
        for medition in self:
            if medition:
                if medition.planning_salas_id is not None:
                    if medition.planning_salas_id.planning_id is not None:
                        if medition.planning_salas_id.planning_id.planograma_id is not None:
                            if medition.planning_salas_id.planning_id.planograma_id.study_id is not None:
                                medition.tipo_estudio = medition.planning_salas_id.planning_id.planograma_id.study_id.name or ''

    tipo_estudio = fields.Char(compute='_compute_studio', string="Tipo de estudio")
    name = fields.Char("Visita", related='planning_salas_id.name')
    auditor = fields.Many2one('res.users', string="Auditor")
    planning_salas_id = fields.Many2one('planning.salas', string="Sala planificada")
    product_id = fields.Many2one('product.product', string="Producto")
    product_ids = fields.Many2many('product.product')
    variable_id = fields.Many2one('variables', string="Variable")
    variable_ids = fields.Many2many('variables', string="Variables")
    valor_por_defecto = fields.Char("Valor por defecto")
    validation_perc = fields.Many2one('validacion.variables', string="Regla de validaci??n",
                                      help="Este campo se usar?? para validar una variable respecto a otra.")
    disponibilidad = fields.Char("Disponibilidad")
    respuesta = fields.Char("Respuesta")
    comment = fields.Char("Comentario")
    posicion_x = fields.Char("Posicion X del producto")
    posicion_y = fields.Char("Posicion Y del producto")
    date_start = fields.Date(string='Momento de medicion')
    planogramado = fields.Boolean(string="Planogramado ?? a??adido", default=True)
    xN1 = fields.Integer(string="xN1")
    xN2 = fields.Integer(string="xN2")
    is_audited = fields.Boolean(string="Auditada?", default=False)
    estado = fields.Selection(
        [('quebrado', 'Quebrado'),
         ('cautivo', 'Cautivo'),
         ('erroneo', 'Err??neo'),
         ('present', 'Presente'),
         ('por_evaluar', 'Por evaluar'),
         ('no_aplica', 'No Aplica')],
        string='Estado', default='por_evaluar')
    product_padre_id = fields.Many2one('product.product', string="Producto padre")
    images_ids = fields.One2many('photo.planning.product', 'planning_product_id')

    detalle1_respuesta = fields.Char("Detalle 1")
    detalle2_respuesta = fields.Char("Detalle 2")
    detalle3_respuesta = fields.Char("Detalle 3")
    detalle4_respuesta = fields.Char("Detalle 4")

    def name_get(self):
        result = []
        for product_planning in self:
            result.append((product_planning.id,
                           '%s - %s' % (product_planning.product_id.name, product_planning.variable_id.name)))
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
    planning_id = fields.Many2one('planning.salas', string="Planning")
    product_id = fields.Many2one('product.product', string="Product")
    variable_id = fields.Many2one('variables', string="Variable")
    auditor = fields.Many2one('res.users', string="Auditor")
    valor_por_defecto = fields.Char("Valor por defecto")
    validation_perc = fields.Char("% Validaci??n")
    disponibilidad = fields.Char("Disponibilidad")
    respuesta = fields.Char("Respuesta")
    comment = fields.Char("Comentario")
    posicion_x = fields.Char("Posicion X del producto")
    posicion_y = fields.Char("Posicion Y del producto")
    date_start = fields.Date(string='Momento de medicion')
    product_padre_id = fields.Many2one('product.product', string="Producto padre")

    # images_ids = fields.One2many('photo.medition', 'planning_study_id')

    def name_get(self):
        result = []
        for studies in self:
            result.append((studies.id,
                           '%s - %s' % (studies.study_id.name, studies.product_id.name)))
        return result


class PhotosPlanningProduct(models.Model):
    _name = "photo.planning.salas"
    _order = 'date'

    planning_sala_id = fields.Many2one('planning.salas', string="Sala planificada")
    date = fields.Datetime(string="Fecha de la imagen")
    image = fields.Binary(string="Imagen")


class PhotosPlanningProduct(models.Model):
    _name = "photo.planning.product"

    planning_product_id = fields.Many2one('planning.product', string="Estudio")
    image = fields.Binary(string="Imagen")
    url_image = fields.Char(string="Url imagen", compute='compute_url_image')

    @api.depends('image')
    def compute_url_image(self):
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        for rec in self:
            image_url_1920 = base_url + '/web/image?' + 'model=photo.planning.product&id=' + str(
                rec.id) + '&field=image'
            rec.url_image = image_url_1920


class Planograma(models.Model):
    _name = "planograma"
    _description = "Planograma"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char("Consecutivo")
    date_start = fields.Date('Date start')
    date_end = fields.Date('Date end')
    partner_id = fields.Many2many('res.partner', string="Clientes")
    study_id = fields.Many2one('study', string="Study")
    user_id = fields.Many2one('res.users', string="Usuario")
    description = fields.Char(size=100, string="Descripci??n")
    salas_planograma_ids = fields.One2many('salas.planograma', 'planograma_id', string='Salas del planograma',
                                           copy=True)
    variables_estudios_ids = fields.One2many('variables.studies', 'planograma_id', string='Variables de estudio',
                                             copy=True)
    selection_vals_domain = fields.Char(
        compute="_compute_selection_vals_domain",
        readonly=True,
        store=False,
    )
    study_id_naturaleza = fields.Char(string="Naturaleza", default='0')
    study_id_type = fields.Char(string="Type")
    scope_type = fields.Char(string="Alcance", )

    # scope = fields.Selection(
    #     [('1', 'Mueble'),
    #      ('0', 'Producto'),
    #      ('2', 'Sala')],
    #     string='Naturaleza')

    # naturaleza = fields.Selection(
    #     [('0', 'Productos'),
    #      ('1', 'Muebles sin productos'),
    #      ('2', 'Muebles con productos'),
    #      ('3', 'Salas')],
    #     string='Naturaleza del estudio')

    @api.onchange('study_id')
    def onchange_study_id(self):
        self.salas_planograma_ids = False
        self.variables_estudios_ids = False

    #
    # # [('tipo_estudio', '=', parent.study_id_type), ('scope', '=', parent.scope_type)]
    # @api.onchange('study_id')
    # def _compute_selection_vals_domain(self):
    #     for rec in self:
    #         print(rec.study_id.naturaleza);
    #         if rec.study_id.naturaleza == '0':
    #             rec.selection_vals_domain = json.dumps(
    #                 [('tipo_estudio', '=', self.study_id.type), ('scope', '=', "0")]
    #             )
    #         if rec.study_id.naturaleza == '1':
    #             rec.selection_vals_domain = json.dumps(
    #                 [('tipo_estudio', '=', self.study_id.type), ('scope', '=', "1")]
    #             )
    #         if rec.study_id.naturaleza == '2':
    #             rec.selection_vals_domain = json.dumps(
    #                 [('tipo_estudio', '=', self.study_id.type), ('scope', 'in', ["1", "0"])]
    #             )
    #         if rec.study_id.naturaleza == '3':
    #             rec.selection_vals_domain = json.dumps(
    #                 [('tipo_estudio', '=', self.study_id.type), ('scope', '=', "1")]
    #             )

    @api.model
    def create(self, vals):
        if not vals.get('name'):
            vals['name'] = self.env['ir.sequence'].next_by_code('planograma')
        return super(Planograma, self).create(vals)

    def name_get(self):
        result = []
        for planograma in self:
            result.append((planograma.id, '%s-%s' % (planograma.name, planograma.study_id.name)))
        return result

    def generate_planning(self):
        if not self.variables_estudios_ids:
            raise UserError("Defina las variables a medir en el estudio")
        vals = {
            "date_start": self.date_start,
            "date_end": self.date_end,
            "user_id": self.user_id.id,
            "planograma_id": self.id,
            "name": self.name,
            "description": self.description,
        }
        planning_id = self.env['planning'].create(vals)

        for line in self.salas_planograma_ids:
            study_type = self.study_id.type
            partner_id = self.partner_id.ids

            quiz = self.env['quiz'].search(
                [('study_type', '=', int(study_type)), ('partner_id', 'in', partner_id)]).ids
            if len(quiz) < 3:
                selected = random.sample(quiz, k=len(quiz))
            else:
                selected = random.sample(quiz, k=3)

            id_quiz_1 = False
            id_quiz_2 = False
            id_quiz_3 = False
            if len(selected) >= 1:
                if len(selected) == 1:
                    id_quiz_1 = selected[0]
                if len(selected) == 2:
                    id_quiz_1 = selected[0]
                    id_quiz_2 = selected[1]
                if len(selected) == 3:
                    id_quiz_1 = selected[0]
                    id_quiz_2 = selected[1]
                    id_quiz_3 = selected[2]
            vals = {
                "planning_id": planning_id.id,
                "place_id": line.place_id.id,
                "auditor_id": self.user_id.id,
                "coordinator_id": self.user_id.id,
                "id_quiz_1": id_quiz_1,
                "id_quiz_2": id_quiz_2,
                "id_quiz_3": id_quiz_3,
                "categories_ids": [(6, 0, line.categories_ids.ids)],
            }
            planning_sala_id = self.env['planning.salas'].create(vals)

            variables_list = []
            for variable in self.variables_estudios_ids:
                for var in variable.variable_id:
                    if var.id not in variables_list:
                        variables_list.append(var.id)
            if line.muebles_ids:
                for mueble in line.muebles_ids:
                    for var in variables_list:
                        vals = {
                            "planning_salas_id": planning_sala_id.id,
                            "product_id": mueble.id,
                            "variable_id": var,
                        }
                        self.env['planning.product'].create(vals)


class VariablesEstudios(models.Model):
    _name = "variables.studies"
    _description = "Variables de estudios"
    _rec_name = 'variable_id'
    _order = 'no_order'

    planograma_id = fields.Many2one("planograma", string="Planograma")
    variable_id = fields.Many2one('variables', string="Variable")
    no_order = fields.Integer(string="Orden de aparici??n")
    selection_vals_domain = fields.Char(
        compute="_compute_selection_vals_domain",
        readonly=True,
        store=False,
    )

    @api.onchange('planograma_id', 'planograma_id.study_id')
    def _compute_selection_vals_domain(self):
        for rec in self:
            print(rec.planograma_id.study_id.naturaleza);
            if rec.planograma_id.study_id:
                if rec.planograma_id.study_id.naturaleza == '0':
                    rec.selection_vals_domain = json.dumps(
                        [('tipo_estudio', '=', self.planograma_id.study_id.type), ('scope', '=', "0")]
                    )
                if rec.planograma_id.study_id.naturaleza == '1':
                    rec.selection_vals_domain = json.dumps(
                        [('tipo_estudio', '=', self.planograma_id.study_id.type), ('scope', '=', "1")]
                    )
                if rec.planograma_id.study_id.naturaleza == '2':
                    rec.selection_vals_domain = json.dumps(
                        [('tipo_estudio', '=', self.planograma_id.study_id.type), ('scope', 'in', ["1", "0"])]
                    )
                if rec.planograma_id.study_id.naturaleza == '3':
                    rec.selection_vals_domain = json.dumps(
                        [('tipo_estudio', '=', self.planograma_id.study_id.type), ('scope', '=', "1")]
                    )
            else:
                rec.selection_vals_domain = json.dumps(
                    []
                )


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
    categories_ids = fields.Many2many('product.category')

    @api.onchange('place_id', 'planograma_id', 'categories_ids')
    def _compute_product_id_domain(self):
        for rec in self:
            print(rec.planograma_id.study_id_naturaleza)
            if rec.planograma_id.study_id_naturaleza == '3':
                rec.product_id_domain = json.dumps(
                    []
                )
            if rec.planograma_id.study_id_naturaleza == '0':
                products = self.env['product.product'].search([('categ_id', 'in', self.categories_ids.ids)]).ids
                rec.product_id_domain = json.dumps(
                    [('id', 'in', products)]
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
