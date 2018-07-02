# -*- coding: utf-8 -*-
# Copyright <2016> <Jarsa Sistemas, S.A. de C.V.>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class ProjectWbsElement(models.Model):
    _inherit = "project.wbs_element"

    billing_concept_total = fields.Float(
        string='Billing Total',
        compute='_compute_billing_concept_total')

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

    @api.multi
    def _compute_billing_concept_total(self):
        for rec in self:
            tasks = self.env['project.task'].search([
                ('wbs_element_id', '=', rec.id)])
            if tasks:
                for task in tasks:
                    rec.billing_concept_total += task.billing_task_total
            else:
                rec.billing_concept_total = 0.0
