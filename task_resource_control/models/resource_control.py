# -*- coding: utf-8 -*-
# <2015> <Jarsa sistemas S.A. de C.V>
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from odoo import api, fields, models


class ResourceControl(models.Model):
    _name = "resource.control"
    _description = "Control the quantity of insumes used in a task"

    name = fields.Char(string="Resource Control Name")
    project_id = fields.Many2one(
        'project.project',
        string="Project")
    insume_explotion_id = fields.Many2one(
        'analytic.resource.plan.line',
        string="Insume")
    task_id = fields.Many2one(
        'project.task',
        string="Task")
    product_id = fields.Many2one(
        'product.product',
        string='Product',)
    analytic_account_id = fields.Many2one(
        'account.analytic.account',
        string='Analytic account')
    type = fields.Selection([
        ('deductive', "Deductive"),
        ('additive', "Additive")])
    reason = fields.Text()
    new_qty = fields.Float(
        string="New quantity changed",
        digits=(14, 5),)

    @api.model
    def create(self, values):
        res_con = super(ResourceControl, self).create(values)
        sequence = res_con.project_id.resource_sequence_id
        res_con.name = sequence.next_by_id()
        return res_con

    @api.multi
    def action_approve(self):
        for rec in self:
            rec.state = 'approved'

    @api.multi
    def action_reject(self):
        for rec in self:
            rec.state = 'reject'

    @api.multi
    def action_pending(self):
        for rec in self:
            rec.state = 'pending'
