# -*- coding: utf-8 -*-
# Copyright <2016> <Jarsa Sistemas, S.A. de C.V.>
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from openerp import api, fields, models, _
from openerp.exceptions import UserError


class ProjectTask(models.Model):
    _inherit = 'project.task'

    wbs_element_id = fields.Many2one(
        comodel_name='project.wbs_element',
        string='WBS Element',
        copy=True
    )
    analytic_account_id = fields.Many2one(
        'account.analytic.account',
        string='Analytic account')
    wbs_element_account = fields.Many2one(
        'account.analytic.account',
        string='Wbs Analytic Account')
    description = fields.Text(required=True,)

    @api.onchange('wbs_element_id')
    def _onchange_wbs_element_id(self):
        if self.wbs_element_id:
            self.project_id = self.wbs_element_id.project_id

    @api.multi
    @api.constrains('wbs_element_id')
    def _check_wbs_element_assigned(self):
        for record in self:
            if record.wbs_element_id and record.wbs_element_id.child_ids:
                raise UserError(
                    _('A WBS Element that is parent'
                        ' of others cannot have'
                        ' concepts assigned.'))

    @api.model
    def create(self, values):
        task = super(ProjectTask, self).create(values)
        if not task.wbs_element_id:
            name = task.name
        else:
            name = ('[' + task.project_id.name + '] /' +
                    '[' + task.wbs_element_id.code + '] / ' + task.name)
        task.analytic_account_id = (
            task.analytic_account_id.create({
                'company_id': self.env.user.company_id.id,
                'name': name,
                'parent_id': task.wbs_element_id.analytic_account_id.id,
                'partner_id': task.partner_id.id,
                'account_type': 'normal'}))
        task.wbs_element_account = (
            task.wbs_element_id.analytic_account_id)
        return task

    @api.multi
    def unlink(self):
        for rec in self:
            if rec.analytic_account_id:
                rec.analytic_account_id.unlink()
            return super(ProjectTask, self).unlink()
