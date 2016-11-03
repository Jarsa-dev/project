# -*- coding: utf-8 -*-
# Copyright <2016> <Jarsa Sistemas, S.A. de C.V.>
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from openerp import api, fields, models, _
from openerp.exceptions import ValidationError


class ProjectWbsElement(models.Model):
    _name = "project.wbs_element"
    _description = "Project WBS Element"
    _inherit = ['mail.thread', 'ir.needaction_mixin']

    code = fields.Char(compute='_compute_wbs_code')
    name = fields.Char(required=True)
    description = fields.Text()
    project_id = fields.Many2one(
        'project.project',
        string='Project',
        required=True,
        copy=True
    )
    parent_id = fields.Many2one(
        'project.wbs_element',
        string='Parent WBS Element',
        required=False,
        copy=True
    )
    child_ids = fields.One2many(
        comodel_name='project.wbs_element',
        inverse_name='parent_id',
        string='Child WBS Elements',
        copy=True
    )
    task_ids = fields.One2many(
        comodel_name='project.task',
        inverse_name='wbs_element_id',
        string='Tasks',
        copy=True
    )
    nbr_tasks = fields.Integer(
        string='Number of Tasks',
        compute='_compute_count_tasks')
    nbr_childs = fields.Integer(
        string='Number of Child WBS Elements',
        compute='_compute_count_childs')
    nbr_docs = fields.Integer(
        string='Number of Documents',
        compute='_compute_count_attached_docs')
    color = fields.Integer(string='Color Index')
    analytic_account_id = fields.Many2one(
        'account.analytic.account',
        string='Analytic account')
    parent_analytic_account_id = fields.Many2one(
        'account.analytic.account',
        string='Parent nalytic account')
    total_charge = fields.Float(compute="_compute_total_charges")


    @api.depends('task_ids')
    def _compute_count_tasks(self):
        for record in self:
            record.nbr_tasks = len(record.task_ids)

    @api.depends('child_ids')
    def _compute_count_childs(self):
        for record in self:
            record.nbr_childs = len(record.child_ids)

    def _compute_count_attached_docs(self):
        attachment = self.env['ir.attachment']
        task = self.env['project.task']
        for record in self:
            project_attachments = attachment.search(
                [('res_model', '=', 'project.wbs_element'),
                 ('res_id', '=', record.id)])
            tasks = task.search([('wbs_element_id', '=', record.id)])
            task_attachments = attachment.search(
                [('res_model', '=', 'project.task'),
                 ('res_id', 'in', tasks.ids)])
            record.nbr_docs = \
                (len(project_attachments) or 0) + (len(task_attachments) or 0)

    @api.onchange('parent_id')
    def _onchange_parent_id(self):
        if self.parent_id:
            self.project_id = self.parent_id.project_id

    @api.multi
    @api.constrains('child_ids', 'task_ids')
    def _check_tasks_assigned(self):
        for record in self:
            if record.child_ids and record.task_ids:
                raise ValidationError(
                    _('A WBS Element that is parent of others cannot have '
                      'tasks assigned.'))

    @api.onchange('project_id')
    def _onchange_project_id(self):
        for record in self.child_ids:
            record.project_id = record.project_id

    @api.multi
    def attachment_tree_view(self):
        tasks = self.env['project.task'].search([
            ('project_id', 'in', self.ids)])
        domain = [
            '|',
            '&', ('res_model', '=', 'project.wbs_element'), (
                'res_id', 'in',
                self.ids),
            '&', ('res_model', '=', 'project.task'), ('res_id', 'in',
                                                      tasks.ids)
        ]
        res_id = self.ids and self.ids[0] or False
        return {
            'name': _('Attachments'),
            'domain': domain,
            'res_model': 'ir.attachment',
            'type': 'ir.actions.act_window',
            'view_id': False,
            'view_mode': 'kanban,tree,form',
            'view_type': 'form',
            'limit': 80,
            'context': "{'default_res_model': '%s','default_res_id': %d}" % (
                self._name, res_id)
        }

    @api.multi
    @api.depends('parent_id', 'child_ids', 'project_id', 'code')
    def _compute_wbs_code(self):
        for rec in self:
            if len(rec.parent_id) == 1:
                if len(rec.parent_id.child_ids) >= 1:
                    childrens = rec.parent_id.child_ids
                    childrens_ids = rec.parent_id.child_ids.ids
                    if rec.id not in childrens_ids:
                        rec.code = ''
                        break
                    else:
                        rec_position = childrens_ids.index(rec.id)
                    if rec_position == 0:
                        rec.code = rec.parent_id.code + '.' + "1"
                    else:
                        element_before = childrens[rec_position - 1]
                        if not element_before.code:
                            last_code = int(element_before.code) + 1
                            rec.code = (rec.parent_id.code +
                                        '.' + str(last_code))
                            rec.parent_analytic_account_id = (
                                rec.parent_id.analytic_account_id)
                        else:
                            codes = element_before.code.split('.')
                            increment_code = int(codes[-1]) + 1
                            rec.code = ''
                            for i, code in enumerate(codes):
                                if i != len(codes) - 1:
                                    if rec.code == '':
                                        rec.code = code
                                    else:
                                        rec.code = rec.code + '.' + code
                                else:
                                    rec.code = (
                                        rec.code + '.' + str(increment_code))
            else:
                all_elements = self.env['project.wbs_element'].search(
                    [('project_id', '=', rec.project_id.id),
                     ('parent_id', '=', False)])
                all_elements_ids = all_elements.ids
                if rec.id not in all_elements_ids:
                    rec.code = ''
                    break
                else:
                    rec_position = all_elements_ids.index(rec.id)
                if rec_position == 0:
                    rec.code = "1"
                else:
                    element_before = all_elements[rec_position - 1]
                    last_code = int(element_before.code) + 1
                    rec.code = str(last_code)

    @api.model
    def create(self, values):
        wbs_element = super(ProjectWbsElement, self).create(values)
        if not wbs_element.parent_id:
            name = ('['+str(wbs_element.code)+'] ' +
                    str(wbs_element.project_id.name.encode("utf-8")) +
                    ' / '+str(wbs_element.name))
        else:
            name = ('['+str(wbs_element.parent_id.code) +
                    ' / '+str(wbs_element.code)+'] ' +
                    str(wbs_element.project_id.name.encode("utf-8")) +
                    ' ' +
                    str(wbs_element.parent_id.name.encode("utf-8")) +
                    ' / '+str(wbs_element.name.encode("utf-8")))
        wbs_element.analytic_account_id = (
            wbs_element.analytic_account_id.create({
                'company_id': self.env.user.company_id.id,
                'name': name,
                'account_type': 'normal'}))
        return wbs_element

    @api.multi
    def unlink(self):
        for rec in self:
            if len(rec.child_ids) > 0:
                raise ValidationError(
                    _("Oops! This WBS element actually have"
                      "Childs elements. \nYou must delete his childs "
                      "before continue"))
            else:
                return super(ProjectWbsElement, self).unlink()

    @api.multi
    def write(self, values):
        for rec in self:
            res = super(ProjectWbsElement, self).write(values)
            if not rec.parent_id:
                name = ('['+str(rec.code)+'] ' +
                        str(rec.project_id.name.encode("utf-8")) +
                        ' / '+str(rec.name.encode("utf-8")))
            else:
                name = ('['+str(rec.parent_id.code) +
                        ' / '+str(rec.code)+'] ' +
                        str(rec.project_id.name.encode("utf-8")) +
                        ' ' +
                        str(rec.parent_id.name.encode("utf-8")) +
                        ' / '+str(rec.name.encode("utf-8")))
                rec.analytic_account_id.name = name
            return res

    @api.depends('child_ids')
    def _compute_total_charges(self):
        for rec in self:
            for child in rec.task_ids:
                rec.total_charge = rec.total_charge + child.subtotal
