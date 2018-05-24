# Copyright 2018, Jarsa Sistemas, S.A. de C.V.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    @api.multi
    def product_sequence(self):
        for rec in self:
            default_code = '%05d' % (1)
            if rec.sale_ok and rec.purchase_ok and rec.type == 'product':
                product = self.env['product.template'].search([
                    ('sale_ok', '=', True),
                    ('purchase_ok', '=', True),
                    ('default_code', '!=', False),
                    ('type', '=', 'product')],
                    limit=1, order='default_code desc')
                if product:
                    default_code = '%05d' % (
                        int(product.default_code.split('PR-')[1]) + 1)
                rec.default_code = 'PR-' + default_code
            elif rec.purchase_ok and rec.type == 'service':
                product = self.env['product.template'].search([
                    ('purchase_ok', '=', True),
                    ('default_code', '!=', False),
                    ('type', '=', 'service')],
                    limit=1, order='default_code desc')
                if product:
                    default_code = '%05d' % (
                        int(product.default_code.split('GA-')[1]) + 1)
                rec.default_code = 'GA-' + default_code
