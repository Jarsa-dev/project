# -*- coding: utf-8 -*-
# <2016> <Jarsa Sistemas, S.A. de C.V.>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from odoo import api, fields, models


class ResourceConsumeLine(models.TransientModel):

    _name = 'resource.consume.line'
    _description = 'Manage the lines of the Product Consumes'

    wiz_id = fields.Many2one('resource.consume')
    line_id = fields.Many2one(
        'analytic.resource.plan.line',
        string='Resource Line',
        required=True,
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
    uom_id = fields.Many2one(
        'product.uom',
        string='UoM',
        readonly=True,)
    real_qty = fields.Float(
        string="Real Quantity",
        readonly=True,
        digits=(14, 5),)
    qty_on_hand = fields.Float(
        string='Quantity On Hand',
        readonly=True,
        digits=(14, 5),)
    qty_consumed = fields.Float(
        string='Quantity Consumed',
        readonly=True,
        digits=(14, 5))
    qty_to_consume = fields.Float(
        string="Quantity To Consume",
        default="1.0",
        digits=(14, 5),)

    @api.onchange('product_id', 'uom_id')
    def onchange_product_id(self):
        if self.product_id:
            name = self.product_id.name
            if self.product_id.code:
                name = '[%s] %s' % (name, self.product_id.code)
            if self.product_id.description_purchase:
                name += '\n' + self.product_id.description_purchase
            self.uom_id = self.product_id.uom_id.id
            self.qty_to_consume = 1
            self.name = name
