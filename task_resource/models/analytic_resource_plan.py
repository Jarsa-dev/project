# -*- coding: utf-8 -*-
# <2016> <Jarsa Sistemas, S.A. de C.V.>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class AnalyticResourcePlanLine(models.Model):
    _name = "analytic.resource.plan.line"
    _description = "Resource Plan"

    name = fields.Char(
        string='Name')
    task_resource_id = fields.Many2one(
        'project.task',
        string='Concept',
    )
    project_id = fields.Many2one(
        'project.project',
        string='Project',
        readonly=True,)
    product_id = fields.Many2one(
        'product.product',
        string='Product')
    account_id = fields.Many2one(
        'account.analytic.account',
        string='Analytic Account')
    date = fields.Date(default=fields.Date.today)
    qty = fields.Float(
        string="Quantity",
        digits=(14, 5),)
    subtotal = fields.Float()
    unit_price = fields.Float()
    description = fields.Char(string='Description')
    uom_id = fields.Many2one(
        comodel_name='product.uom',
        string='UoM',
    )
    purchase_request_ids = fields.Many2many(
        comodel_name='purchase.request',
        string='Purchase Requests')
    resource_type_id = fields.Many2one(
        'resource.type',
        string='Resources types')

    real_qty = fields.Float(
        string="Quantity Real",
        digits=(14, 5),)
    requested_qty = fields.Float(
        string="Requested Quantity",
        compute='_compute_requested_qty',
        digits=(14, 5),)

    @api.model
    def _get_available_qty(self):
        if self.requested_qty > 0.0:
            return self.real_qty - self.requested_qty
        else:
            return self.real_qty

    @api.onchange('product_id')
    def onchange_product(self):
        self.description = self.product_id.description
        self.uom_id = self.product_id.uom_id
        self.account_id = self.task_resource_id.analytic_account_id

    @api.model
    def create(self, values):
        res = super(AnalyticResourcePlanLine, self).create(values)
        project = res.task_resource_id.project_id.name
        product = res.product_id.name
        task = res.task_resource_id.name
        res.name = '[' + project + ' / ' + task + ']' + '[' + product + ']'
        return res

    @api.multi
    def _compute_requested_qty(self):
        for rec in self:
            requests = self.env['purchase.request'].search(
                [('state', '!=', 'rejected')])
            if requests:
                for request in requests:
                    for line in request.line_ids:
                        if (rec.product_id.id == line.product_id.id and
                                rec.account_id.id == line.
                                analytic_account_id.id):
                            product_uom_qty = (
                                self.env['product.uom']._compute_qty(
                                    line.product_uom_id.id,
                                    line.product_qty,
                                    rec.product_id.uom_id.id,
                                    round=False))
                            rec.requested_qty += product_uom_qty
            else:
                rec.requested_qty = 0.0
