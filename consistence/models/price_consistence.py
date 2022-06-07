# -*- coding: utf-8 -*-
import json

from odoo import models, fields, api

from odoo import tools


class PriceConsistence(models.Model):
    _name = 'price.consistence'

    name = fields.Char(string="Nombre")
    #
    # def _query(self, with_clause='', fields={}, groupby='', from_clause=''):
    #     with_ = ("WITH %s" % with_clause) if with_clause else ""
    #
    #     select_ = """study_id"""
    #     from_ = """ planograma """
    #     return '%s (SELECT %s FROM %s)' % (with_, select_, from_)
    #
    # def init(self):
    #     # self._table = sale_report
    #     tools.drop_view_if_exists(self.env.cr, self._table)
    #     self.env.cr.execute("""CREATE or REPLACE VIEW %s as (%s)""" % (self._table, self._query()))

    @api.model
    def retrieve_dashboard(self):
        print("retrieve data")
        # """ This function returns the values to populate the custom dashboard in
        #     the purchase order views.
        # """
        # self.check_access_rights('read')
        elements = self.env['price.consistence'].search([])
        result = {
            'count_elements': len(elements), }
        #     'all_waiting': 0,
        #     'all_late': 0,
        #     'my_to_send': 0,
        #     'my_waiting': 0,
        #     'my_late': 0,
        #     'all_avg_order_value': 0,
        #     'all_avg_days_to_purchase': 0,
        #     'all_total_last_7_days': 0,
        #     'all_sent_rfqs': 0,
        #     'company_currency_symbol': self.env.company.currency_id.symbol
        # }
        #
        # one_week_ago = fields.Datetime.to_string(fields.Datetime.now() - relativedelta(days=7))
        # # This query is brittle since it depends on the label values of a selection field
        # # not changing, but we don't have a direct time tracker of when a state changes
        # query = """SELECT COUNT(1)
        #             FROM mail_tracking_value v
        #             LEFT JOIN mail_message m ON (v.mail_message_id = m.id)
        #             JOIN purchase_order po ON (po.id = m.res_id)
        #             WHERE m.create_date >= %s
        #               AND m.model = 'purchase.order'
        #               AND m.message_type = 'notification'
        #               AND v.old_value_char = 'RFQ'
        #               AND v.new_value_char = 'RFQ Sent'
        #               AND po.company_id = %s;
        #          """
        #
        # self.env.cr.execute(query, (one_week_ago, self.env.company.id))
        # res = self.env.cr.fetchone()
        # result['all_sent_rfqs'] = res[0] or 0
        #
        # # easy counts
        # po = self.env['purchase.order']
        # result['all_to_send'] = po.search_count([('state', '=', 'draft')])
        # result['my_to_send'] = po.search_count([('state', '=', 'draft'), ('user_id', '=', self.env.uid)])
        # result['all_waiting'] = po.search_count([('state', '=', 'sent'), ('date_order', '>=', fields.Datetime.now())])
        # result['my_waiting'] = po.search_count(
        #     [('state', '=', 'sent'), ('date_order', '>=', fields.Datetime.now()), ('user_id', '=', self.env.uid)])
        # result['all_late'] = po.search_count(
        #     [('state', 'in', ['draft', 'sent', 'to approve']), ('date_order', '<', fields.Datetime.now())])
        # result['my_late'] = po.search_count(
        #     [('state', 'in', ['draft', 'sent', 'to approve']), ('date_order', '<', fields.Datetime.now()),
        #      ('user_id', '=', self.env.uid)])
        #
        # # Calculated values ('avg order value', 'avg days to purchase', and 'total last 7 days') note that 'avg order value' and
        # # 'total last 7 days' takes into account exchange rate and current company's currency's precision. Min of currency precision
        # # is taken to easily extract it from query.
        # # This is done via SQL for scalability reasons
        # query = """SELECT AVG(COALESCE(po.amount_total / NULLIF(po.currency_rate, 0), po.amount_total)),
        #                    AVG(extract(epoch from age(po.date_approve,po.create_date)/(24*60*60)::decimal(16,2))),
        #                    SUM(CASE WHEN po.date_approve >= %s THEN COALESCE(po.amount_total / NULLIF(po.currency_rate, 0), po.amount_total) ELSE 0 END),
        #                    MIN(curr.decimal_places)
        #             FROM purchase_order po
        #             JOIN res_company comp ON (po.company_id = comp.id)
        #             JOIN res_currency curr ON (comp.currency_id = curr.id)
        #             WHERE po.state in ('purchase', 'done')
        #               AND po.company_id = %s
        #          """
        # self._cr.execute(query, (one_week_ago, self.env.company.id))
        # res = self.env.cr.fetchone()
        # result['all_avg_order_value'] = round(res[0] or 0, res[3])
        # result['all_avg_days_to_purchase'] = round(res[1] or 0, 2)
        # result['all_total_last_7_days'] = round(res[2] or 0, res[3])

        return result
