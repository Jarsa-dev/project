# -*- coding: utf-8 -*-
# <2015> <Jarsa sistemas S.A. de C.V>
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from odoo import api, fields, models


class ProjectProject(models.Model):
    _inherit = "project.project"

    resource_sequence_id = fields.Many2one(
        'ir.sequence',
        string='Resource Control Sequence')
    resource_control_ids = fields.One2many(
        'resource.control',
        'project_id',
        string="Resources Control")
    total_real_charge = fields.Float(
        compute='_compute_total_real_charge',
        string='Total Real',)

    @api.multi
    def _compute_total_real_charge(self):
        for rec in self:
            wbs_elements = self.env['project.wbs_element'].search([
                ('project_id', '=', rec.id)])
            if wbs_elements:
                for wbs_element in wbs_elements:
                    if not wbs_element.parent_id:
                        rec.total_real_charge += (
                            wbs_element.total_real_charge)

    @api.model
    def create(self, values):
        res = super(ProjectProject, self).create(values)
        resource_sequence = self.env['ir.sequence'].create({
            'name':  res.name + '/ [Resource control]',
            'active': True,
            'implementation': 'no_gap',
            'prefix': res.name + '-RC-',
            'number_increment': 1
            })
        res.resource_sequence_id = resource_sequence
        return res
