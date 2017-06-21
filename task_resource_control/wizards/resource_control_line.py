# -*- coding: utf-8 -*-
# <2016> <Jarsa Sistemas, S.A. de C.V.>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ResourceControlLine(models.TransientModel):

    _name = 'resource.control.line'
    _description = 'Manage the lines of the Aditive/Deductive'

    wiz_id = fields.Many2one('resource.control.wizard')
    name = fields.Char(
        string='Task name',
        readonly=True)
    line_id = fields.Many2one(
        'analytic.resource.plan.line',
        string='Resource Line',
        readonly=True)
    task_id = fields.Many2one(
        'project.task', string="Project Task",
        readonly=True)
    analytic_account_id = fields.Many2one(
        'account.analytic.account',
        related='line_id.account_id',
        string='Analytic Account',
        readonly=True)
    product_id = fields.Many2one(
        'product.product',
        string='Product',
        readonly=True)
    description = fields.Char(
        string='Description',
        readonly=True)
    uom_id = fields.Many2one(
        'product.uom',
        string='UoM',
        readonly=True)
    qty = fields.Float(
        string='Quantity Planned',
        readonly=True)
    real_qty = fields.Float(
        string='Quantity Real',
        readonly=True)
    new_qty = fields.Float(
        string='New Quantity',
        required=True,)
    unit_price = fields.Float(
        string='Unit price')
    subtotal = fields.Float(string='Subtotal')
    type = fields.Char(string='Control type')
    reason = fields.Text(required=True,)
