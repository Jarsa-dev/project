# -*- coding: utf-8 -*-
# Copyright <2016> <Jarsa Sistemas, S.A. de C.V.>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models
from odoo.exceptions import ValidationError
from odoo.tools.translate import _


class ProjectWbsElement(models.Model):
    _inherit = "project.wbs_element"

    total_concept_expense = fields.Float(
        string='Billing Total',
        compute='_compute_total_concept_expense')

    @api.multi
    def _compute_total_concept_expense(self):
        for rec in self:
            tasks = self.env['project.task'].search([
                ('wbs_element_id', '=', rec.id)])
            if tasks:
                for task in tasks:
                    rec.total_concept_expense += task.total_expense
            else:
                rec.total_concept_expense = 0.0
        for record in self:
            if record.child_ids:
                for child in record.child_ids:
                    record.total_concept_expense += child.total_concept_expense

    @api.multi
    @api.constrains('project_id')
    def _check_project_state(self):
        for rec in self:
            if rec.project_id.state == 'open' and rec.project_id.order_change:
                raise ValidationError(
                    _('A task can not be created when the '
                      'project is in open state. For create it'
                      ' you must go to the project and make an order change.'))
