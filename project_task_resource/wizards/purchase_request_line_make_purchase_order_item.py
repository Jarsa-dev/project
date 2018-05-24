# -*- coding: utf-8 -*-
# <2016> <Jarsa Sistemas, S.A. de C.V.>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models
from odoo.exceptions import ValidationError
from odoo.tools.translate import _


class PurchaseRequestLineMakePurchaseOrderItem(models.TransientModel):
    _inherit = "purchase.request.line.make.purchase.order.item"

    product_qty = fields.Float(string='Quantity to purchase',
                               digits=(14, 4),)
    is_project_insume = fields.Boolean()
    product_id = fields.Many2one(
        comodel_name='product.product',
        string='Product',
        )
    product_uom_id = fields.Many2one(
        comodel_name='product.uom',
        string='UoM',)
    subtotal = fields.Float(
        digits=(14, 4),)


class PurchaseRequestLineMakePurchaseOrder(models.TransientModel):
    _inherit = "purchase.request.line.make.purchase.order"

    @api.model
    def _prepare_item(self, line):
        res = super(
            PurchaseRequestLineMakePurchaseOrder, self)._prepare_item(line)
        res['is_project_insume'] = True
        res['product_qty'] = line.remaining_qty
        return res

    @api.model
    def _check_valid_request_line(self, request_line_ids):
        for line in self.env['purchase.request.line'].browse(request_line_ids):
            if line.request_id.state != 'approved':
                raise ValidationError(
                    _('Purchase Request %s is not approved') %
                    line.request_id.name)
            if (line.purchase_state in ['purchase', 'done'] and
                    line.remaining_qty == line.product_qty):
                raise ValidationError(
                    _('The purchase has already been completed \n \n'
                      'Line: %s \n Product: %s.') %
                    (line.request_id.name, line.product_id.name))
        return (
            super(PurchaseRequestLineMakePurchaseOrder, self).
            _check_valid_request_line(request_line_ids))

    @api.model
    def _prepare_purchase_order_line(self, po, item):
        res = (
            super(PurchaseRequestLineMakePurchaseOrder, self).
            _prepare_purchase_order_line(po, item))
        if item.product_qty > item.line_id.product_qty:
            raise ValidationError(
                _('The quantity must be lower than the quantity of'
                    ' the purchase request line. \n\n'
                    'Product: %s') % item.product_id.name)
        if item.product_qty > item.line_id.remaining_qty:
            raise ValidationError(
                _('The quantity must be lower than the product'
                    ' remaining quantity. \n \n'
                  'Line: %s \n Product: %s.') %
                (item.request_id.name, item.product_id.name))
        res['is_project_insume'] = item.is_project_insume
        res['taxes_id'] = [(6, 0, item.product_id.supplier_taxes_id.ids)]
        res['specifications'] = item.line_id.specifications
        return res
