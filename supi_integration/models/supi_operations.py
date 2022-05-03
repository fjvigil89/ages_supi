# -*- coding: utf-8 -*-

from odoo import models, fields, api


class QuizResult(models.Model):
    _name = 'quiz.result'

    quiz_id = fields.Many2one('quiz', string="Test")
    user_id = fields.Many2one('res.users', string="Usuario")
    name = fields.Char(related="quiz_id.correct_answer", string="Respuesta correcta")
    respuesta_seleccionada = fields.Char(string="Respuesta seleccionada")
    respuesta1 = fields.Char(string="Respuesta aleatoria")
    respuesta2 = fields.Char(string="Respuesta aleatoria")
