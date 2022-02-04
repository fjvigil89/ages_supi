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
    ], string='Type', help='Variables of study in system')
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
    lat = fields.Char(string="Latitude")
    long = fields.Char(string="Longitude")


class PlanningStudies(models.Model):
    _name = "planning.studies"

    study_id = fields.Many2one('study', string="Study")
    planning_id = fields.Many2one('planning', string="Planning")
    product_id = fields.Many2one('product.product', string="Product")
    auditor_id = fields.Char(string="Auditor")
