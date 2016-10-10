# -*- coding: utf-8 -*-
# © 2016 Jarsa Sistemas S.A. de C.V..
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from openerp import _, models, fields


class ProjectWbsConcept(models.Model):
    _name = 'project.wbs.concept'
    _inherit = ['mail.thread', 'ir.needaction_mixin']

    name = fields.Char(required=True)
    product_uom_id = fields.Many2one(
        'product.uom',
        string='UoM',
        required=True)
    unit_price = fields.Float(required=True)
    standard_price = fields.Float(required=True)
    active = fields.Boolean(default=True)

    _sql_constraints = [
        ('name_unique',
         'UNIQUE(name)',
         _("The concept name must be unique")),
    ]
