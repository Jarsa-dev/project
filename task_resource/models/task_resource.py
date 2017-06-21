# -*- coding: utf-8 -*-
# 2015 Eficent Business and IT Consulting Services S.L.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from odoo import api, fields, models


class TaskResource(models.Model):
    _name = "task.resource"

    task_id = fields.Many2one(
        comodel_name='project.task',
        string='Task',
    )
    product_id = fields.Many2one(
        comodel_name='product.product',
        string='Product',
    )
    uom_id = fields.Many2one(
        comodel_name='product.uom',
        string='UoM',
    )
    qty = fields.Float(
        string='Quantity',
        default=1,
        digits=(14, 5),
    )
    account_id = fields.Many2one(
        'account.analytic.account',
        string='Analytic Account')
    description = fields.Char('Description')
    resource_type_id = fields.Many2one(
        'resource.type',
        string='Resource type')
    unit_price = fields.Float(
        string='Unit Price',)

    @api.onchange('product_id')
    def onchange_product(self):
        self.account_id = self.task_id.analytic_account_id

    @api.multi
    @api.onchange('product_id')
    def product_id_change(self):
        description = ''
        uom_id = False
        product = self.product_id
        if product:
            description = product.name_get()[0][1]
            uom_id = product.uom_id.id
        if product.description_purchase:
            description += ' - ' + product.description_purchase
        self.description = description
        self.uom_id = uom_id
        self.unit_price = self.product_id.list_price

    @api.model
    def default_get(self, field):
        if 'active_id' in self.env.context:
            record_id = self.env.context['active_id']
            plan = self.env['project.wbs_element'].search(
                [('id', '=', record_id)])
            res = super(TaskResource, self).default_get(field)
            res.update({'account_id': plan.analytic_account_id.id})
            res.update(domain={
                'account_id': plan.analytic_account_id.id
            })
            return res
        else:
            return super(TaskResource, self).default_get(field)
