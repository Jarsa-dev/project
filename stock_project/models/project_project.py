# -*- coding: utf-8 -*-
# Jarsa Sistemas S.A. de C.V.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from openerp import _, api, fields, models


class ProjectProject(models.Model):
    _inherit = 'project.project'

    location_id = fields.Many2one(
        comodel_name='stock.location',
        string='Project Location'
    )
    code = fields.Char()
    picking_out_id = fields.Many2one('stock.picking.type')

    @api.model
    def create(self, vals):
        project = super(ProjectProject, self).create(vals)
        location = project.location_id.create({
            'name': project.name,
            'active': True,
            'partner_id': project.partner_id.id
        })
        project.location_id = location.id
        sequence_out_id = self.env['ir.sequence'].create({
            'name':  project.name + ' Sequence Out',
            'active': True,
            'implementation': 'no_gap',
            'prefix': vals['code'] + '/OUT/',
            'number_increment': 1
            })
        delievery_id = self.env['stock.picking.type'].create(
            {
                'name': location.name + _('/Delievery'),
                'sequence_id': sequence_out_id.id,
                'warehouse_id': 1,
                'code': 'incoming',
                'default_location_src_id': location.id,
                'default_location_dest_id': self.env.ref(
                    'stock.location_production').id
            })
        sequence_in_id = self.env['ir.sequence'].create({
            'name':  project.name + ' Sequence In',
            'active': True,
            'implementation': 'no_gap',
            'prefix': vals['code'] + '/IN/',
            'number_increment': 1
            })
        self.env['stock.picking.type'].create(
            {
                'name': location.name + _('/Receptions'),
                'sequence_id': sequence_in_id.id,
                'warehouse_id': 1,
                'code': 'incoming',
                'return_picking_type_id': delievery_id.id,
                'default_location_dest_id': location.id
            })
        project.picking_out_id = delievery_id.id
        return project
