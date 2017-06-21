# -*- coding: utf-8 -*-
# © 2016 Jarsa Sistemas, S.A. de C.V.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models, _


class AccountChartOfAnalyticsWizard(models.TransientModel):
    _inherit = "account.analytic.chart"

    date_from = fields.Date(string='From')
    date_to = fields.Date(string='To')

    @api.multi
    def account_chart_open_window(self):
        mod_obj = self.env['ir.model.data']
        act_obj = self.env['ir.actions.act_window']

        result = mod_obj.get_object_reference(
            'account_analytic_report', 'action_analytic_tree')
        id = result and result[1] or False
        result = act_obj.search_read([('id', '=', id)])[0]
        res = {}
        title = ''
        if self.date_from and self.date_to:
            res['date_from'] = self.date_from
            res['date_to'] = self.date_to
            title += _('From: ') + self.date_from + _(' To ') + self.date_to

        result['context'] = str(res)
        result['display_name'] += title
        return result
