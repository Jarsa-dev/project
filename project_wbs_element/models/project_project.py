# Copyright 2015 Eficent Business and IT Consulting Services S.L.
# Copyright 2016 Jarsa Sistemas S.A. de C.V.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import _, api, fields, models


class ProjectProject(models.Model):
    _inherit = 'project.project'

    wbs_element_ids = fields.One2many(
        comodel_name='project.wbs_element',
        inverse_name='project_id',
        copy=True
    )
    nbr_wbs_elements = fields.Integer('Number of WBS Elements',
                                      compute='_compute_count_wbs_elements')
    # TODO: move this field to the module that requires it.
    indirects_analytic_account_id = fields.Many2one(
        'account.analytic.account',
        string='Indirects Analytic Account')

    @api.depends('wbs_element_ids')
    def _compute_count_wbs_elements(self):
        for record in self:
            record.nbr_wbs_elements = len(record.wbs_element_ids)

    # TODO: move this method to the module that requires it.
    @api.model
    def create(self, vals):
        name = ('[%s] /%s' % (vals['name'], _('indirects')))
        vals['indirects_analytic_account_id'] = (
            self.indirects_analytic_account_id.create({
                'company_id': self.env.user.company_id.id,
                'name': name,
                'account_type': 'normal',
                'partner_id': vals['partner_id'],
            }).id)
        return super().create(vals)
