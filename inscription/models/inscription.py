# -*- coding: utf-8 -*-

from odoo import fields, models


class Inscription(models.Model):
    _name = "inscription"

    name = fields.Char(
        string='Name'
    )

    email = fields.Char(
        string='Email'
    )

    phone = fields.Char(
        string="Phone Number"
    )

    address = fields.Text(
        string='Address'
    )

    password = fields.Char(
        string='Password'
    )

    state = fields.Selection([
        ('draft', 'Draft'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected')],
        default='draft',
        string='State'
    )


    user_id = fields.Many2one(
        'res.users',
        readonly=True
    )

    employee_id = fields.Many2one(
        'hr.employee',
        string='Employee',
    )

    def button_draft(self):
        return self.write({'state': 'draft'})

    def button_approved(self):
        for record in self:
            user = self.env['res.users'].create({
                'name': record.name,
                'login': record.email,
                'email': record.email,
                'password': record.password,
            })
            employee = self.env['hr.employee'].create({
                'name': record.name,
                'user_id': user.id,
                'address_home_id': self.env['res.partner'].create({
                    'name':record.name,
                    'street':record.address,
                }).id,
                'phone': record.phone,
                'private_email': record.email,
            })
            record.user_id = user.id
            record.employee_id = employee.id
            # record.user_id.action_reset_password()

            self.write({'state': 'approved'})
        return True

    def button_rejected(self):
        return self.write({'state': 'rejected'})
