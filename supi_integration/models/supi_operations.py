# -*- coding: utf-8 -*-

from odoo import models, fields, api


class QuizResult(models.Model):
    _name = 'quiz.result'

    quiz_id = fields.Many2one('quiz', string="Test")
    studie_done_id = fields.Many2one('studies.done', string="Estudios realizados")
    user_id = fields.Many2one('res.users', string="Usuario")
    name = fields.Char(related="quiz_id.correct_answer", string="Respuesta correcta")
    respuesta_seleccionada = fields.Char(string="Respuesta seleccionada")
    respuesta1 = fields.Char(string="Respuesta aleatoria")
    respuesta2 = fields.Char(string="Respuesta aleatoria")

    @api.model_create_multi
    def create(self, vals_list):
        for values in vals_list:
            quiz_result = super().create(values)
        return quiz_result
