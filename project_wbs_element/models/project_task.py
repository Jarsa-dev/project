# Copyright 2016 Jarsa Sistemas S.A. de C.V.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class ProjectTask(models.Model):
    _inherit = 'project.task'

    wbs_element_id = fields.Many2one(
        comodel_name='project.wbs_element',
        string='WBS Element',
        copy=True
    )
    analytic_tag_id = fields.Many2one(
        'account.analytic.tag',
        string='Analytic account')
    description = fields.Text()
    state = fields.Selection(
        [('draft', 'Draft'),
         ('confirm', 'Confirmed')],
        string='Status',
        readonly=True,
        default='draft')

    @api.onchange('wbs_element_id')
    def _onchange_wbs_element_id(self):
        if self.wbs_element_id:
            self.project_id = self.wbs_element_id.project_id

    @api.multi
    @api.constrains('wbs_element_id')
    def _check_wbs_element_assigned(self):
        for record in self:
            if record.wbs_element_id and record.wbs_element_id.child_ids:
                raise ValidationError(
                    _('A WBS Element that is parent'
                        ' of others cannot have'
                        ' concepts assigned.'))

    @api.model
    def create(self, values):
        rec = super().create(values)
        if not rec.wbs_element_id:
            name = rec.name
        else:
            name = '[%s] %s - %s' % (
                rec.project_id.name, rec.wbs_element_id.code, rec.name)
        rec.analytic_tag_id = (
            rec.analytic_tag_id.create({
                'name': name,
            }))
        return rec

    @api.multi
    def unlink(self):
        for rec in self:
            if rec.analytic_tag_id:
                rec.analytic_tag_id.unlink()
            return super().unlink()
