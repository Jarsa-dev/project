# -*- coding: utf-8 -*-
# © <2016> <Jarsa Sistemas, S.A. de C.V.>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import fields, models



class AnalyticPlanVersion(models.Model):
    _name = 'analytic.plan.version'
    _inherit = ['mail.thread', 'ir.needaction_mixin']
    _description = 'Analytic Planning Version'

    name = fields.Char('Planning Version Name', required=True)
    code = fields.Char('Planning Version Code')
    active = fields.Boolean(
        help='If the active field is set to False, '
             'it will allow you to hide the analytic planning version '
             'without removing it.')
    notes = fields.Text()
    company_id = fields.Many2one(
        'res.company', string='Company', required=True)
    default_committed = fields.Boolean()
    default_plan = fields.Boolean(string='Default planning version')
