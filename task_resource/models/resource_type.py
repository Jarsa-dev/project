# -*- coding: utf-8 -*-0
# <2016> <Jarsa Sistemas, S.A. de C.V.>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class ResourceType(models.Model):
    _name = 'resource.type'
    _description = 'Make Product Consumes'

    name = fields.Char(
        string='Resource type')
    task_resource_ids = fields.One2many(
        'task.resource',
        'resource_type_id',
        string='Task resource')
