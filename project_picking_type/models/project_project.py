# -*- coding: utf-8 -*-
# © <2016> <Jarsa Sistemas, S.A. de C.V.>
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import api, fields, models


class ProjectProject(models.Model):
    _inherit = 'project.project'

    location_id = fields.Many2one(
        comodel_name='stock.location',
        string='Project Location',)
    picking_out_id = fields.Many2one(
        comodel_name='stock.picking.type',
        string='Picking Out',)
    picking_in_id = fields.Many2one(
        comodel_name='stock.picking.type',
        string='Picking In',)
    operations_state = fields.Boolean(
        compute='_compute_operations_state',
        default=True)

    @api.multi
    def action_close(self):
        self.picking_in_id.active = False
        self.picking_out_id.active = False
        return super(ProjectProject, self).action_close()

    @api.multi
    def _compute_operations_state(self):
        for rec in self:
            if rec.picking_out_id and rec.picking_in_id:
                if (not rec.picking_out_id.active and not
                        rec.picking_in_id.active):
                    rec.operations_state = False
                else:
                    rec.operations_state = True
