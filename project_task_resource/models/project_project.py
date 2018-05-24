# -*- coding: utf-8 -*-
# <2016> <Jarsa Sistemas, S.A. de C.V.>
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import _, api, fields, models


class ProjectProject(models.Model):
    _inherit = 'project.project'

    total_project_expenses = fields.Float(
        'Billing Total', compute='_compute_total_project_expenses',)
    state = fields.Selection(
        [('draft', 'Draft'),
         ('open', 'In Progress'),
         ('closed', 'Closed'),
         ('cancel', 'Canceled')],
        string='Status',
        readonly=True,
        default='draft',)
    order_change = fields.Boolean()

    @api.multi
    def _compute_total_project_expenses(self):
        for rec in self:
            wbs_elements = self.env['project.wbs_element'].search([
                ('project_id', '=', rec.id)])
            if wbs_elements:
                for wbs_element in wbs_elements:
                    if not wbs_element.parent_id:
                        rec.total_project_expenses += (
                            wbs_element.total_concept_expense)
            else:
                rec.total_project_expenses = 0.0

    @api.multi
    def action_open(self):
        for rec in self:
            rec.state = 'open'
            rec.order_change = False

    @api.multi
    def action_close(self):
        for rec in self:
            rec.state = 'closed'

    @api.multi
    def action_open_draft(self):
        for rec in self:
            rec.state = 'draft'

    @api.multi
    def action_cancel_draft(self):
        for rec in self:
            rec.state = 'draft'

    @api.multi
    def action_cancel(self):
        for rec in self:
            rec.state = 'cancel'

    @api.multi
    def make_order_change(self):
        for rec in self:
            rec.state = 'draft'

            return {
                'name': _('WBS Element'),
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'project.wbs_element',
                'context': {
                    'default_project_id': rec.id,
                },
                'target': 'current',
                'type': 'ir.actions.act_window',
            }
