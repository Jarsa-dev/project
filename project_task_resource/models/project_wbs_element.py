# -*- coding: utf-8 -*-
# Copyright <2016> <Jarsa Sistemas, S.A. de C.V.>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class ProjectWbsElement(models.Model):
    _inherit = "project.wbs_element"

    total_concept_expense = fields.Float(
        string='Billing Total',
        compute='_compute_total_concept_expense')
    total_charge = fields.Float(
        compute="_compute_total_charges",
        string='Total Charge')

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
    def _compute_total_charges(self):
        for record in self:
            if not record.child_ids:
                for child in record.task_ids:
                    record.total_charge = record.total_charge + child.subtotal
        for rec in self:
            if rec.child_ids:
                for child in rec.child_ids:
                    rec.total_charge = rec.total_charge + child.total_charge
