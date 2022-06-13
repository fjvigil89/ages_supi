import time

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class ShowPlanningStudiesGallery(models.TransientModel):
    _name = 'show.planning.studies'

    @api.model
    def _default_vendor(self):
        context = self._context or {}
        payment = self.env['planning.studies'].browse(context.get('active_ids', []))
        if payment:
            return payment.auditor.id

    @api.model
    def _default_image(self):
        context = self._context or {}
        planning = self.env['planning.studies'].browse(context.get('active_ids', []))
        if planning:
            return planning.images_ids.ids

    images_ids = fields.Many2many('photo.medition', default=_default_image)
    auditor = fields.Many2one('res.users', string='Vendor', required=False, default=_default_vendor)

    @api.model
    def default_get(self, fields_list):
        # OVERRIDE
        res = super().default_get(fields_list)

        planning = self.env['planning.studies'].browse(self._context.get('active_ids', []))
        res['images_ids'] = [(6, 0, planning.images_ids.ids)]
        return res
        # planning = self.env['planning.studies'].browse(self.env.context['active_ids'])
        # print(planning)
        #
        # self.write({
        #     'images_ids': [(6, 0, planning.images_ids.ids)]
        # })

        # values = super(ReSequenceWizard, self).default_get(fields_list)
        # active_move_ids = self.env['account.move']
        # if self.env.context['active_model'] == 'account.move' and 'active_ids' in self.env.context:
        #     active_move_ids = self.env['account.move'].browse(self.env.context['active_ids'])
        # if len(active_move_ids.journal_id) > 1:
        #     raise UserError(_('You can only resequence items from the same journal'))
        # move_types = set(active_move_ids.mapped('move_type'))
        # if (
        #         active_move_ids.journal_id.refund_sequence
        #         and ('in_refund' in move_types or 'out_refund' in move_types)
        #         and len(move_types) > 1
        # ):
        #     raise UserError(
        #         _('The sequences of this journal are different for Invoices and Refunds but you selected some of both types.'))
        # values['move_ids'] = [(6, 0, active_move_ids.ids)]
        # return values
