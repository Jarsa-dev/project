# -*- coding: utf-8 -*-
# 2015 Eficent Business and IT Consulting Services S.L.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from openerp import _, api, exceptions, fields, models


class ProjectTask(models.Model):
    _inherit = "project.task"

    resource_ids = fields.One2many(
        comodel_name='task.resource',
        inverse_name='task_id',
        string='Task Resource',
        copy=True,
        store=True)
    state = fields.Selection(
        [('draft', 'Draft'),
         ('confirm', 'Confirmed')],
        string='Status',
        readonly=True,
        default='draft')
    resource_line_ids = fields.One2many(
        comodel_name='analytic.resource.plan.line',
        inverse_name='task_resource_id',
        store=True,
        compute='_compute_resources_line_ids')
    project_id = fields.Many2one(
        'project.project')
    analytic_account_id = fields.Many2one(
        'account.analytic.account',
        string='Analytic account')
    uom_id = fields.Many2one(
        comodel_name='product.uom',
        string='UoM',
    )
    qty = fields.Float(
        string='Quantity',
        default=1,
    )
    subtotal = fields.Float(compute='_compute_value_subtotal')
    unit_price = fields.Float()
    total_expense = fields.Float(
        'Total Expenses', compute="_compute_total_expense")
    partner_id = fields.Many2one(
        comodel_name='res.partner',
        string='Customer',
        compute='_compute_partner_id',
        store=True,
        readonly=True, )

    @api.depends('project_id')
    def _compute_partner_id(self):
        for rec in self:
            if rec.project_id:
                rec.partner_id = rec.project_id.partner_id.id

    @api.multi
    @api.constrains('project_id')
    def _check_project_state(self):
        for rec in self:
            if rec.project_id.state == 'open' and rec.project_id.order_change:
                raise exceptions.ValidationError(
                    _('A task can not be created when the '
                      'project is in open state. For create it'
                      ' you must go to the project and make an order change.'))

    @api.multi
    def _compute_total_expense(self):
        for rec in self:
            invoice_lines = self.env['account.invoice.line'].search([
                ('invoice_id.state', 'in', ['open', 'paid']),
                ('product_id', 'in', [
                    x.product_id.id for x in rec.resource_line_ids]),
                ('account_analytic_id', '=', rec.analytic_account_id.id)])
            if invoice_lines:
                for line in invoice_lines:
                        rec.total_expense += line.price_subtotal
            else:
                rec.total_expense = 0.0

    @api.multi
    @api.depends('qty', 'unit_price')
    def _compute_value_subtotal(self):
        for rec2 in self:
            rec2.subtotal = rec2.qty * rec2.unit_price

    @api.multi
    def write(self, values):
        for rec in self:
            res = super(ProjectTask, self).write(values)
            resources = self.env['analytic.resource.plan.line'].search([
                ('task_resource_id', '=', rec.id)])
            if not resources:
                for resource in rec.resource_ids:
                    rec.resource_line_ids.create({
                        'task_resource_id': rec.id,
                        'project_id': rec.project_id.id,
                        'account_id': resource.account_id.id,
                        'product_id': resource.product_id.id,
                        'description': resource.description,
                        'resource_type_id': resource.resource_type_id.id,
                        'uom_id': resource.uom_id.id,
                        'qty': rec.qty * resource.qty,
                        'real_qty': rec.qty * resource.qty,
                        'subtotal': (
                            rec.qty * resource.qty * (
                                resource.unit_price))
                    })
            else:
                list_item = []
                for item in resources:
                    if not item.purchase_request_ids and rec.state == 'draft':
                        item.unlink()
                    else:
                        list_item.append(item.product_id.id)
                for resource in rec.resource_ids:
                    if resource.product_id.id not in list_item:
                        rec.resource_line_ids.create({
                            'task_resource_id': rec.id,
                            'project_id': rec.project_id.id,
                            'account_id': resource.account_id.id,
                            'product_id': resource.product_id.id,
                            'description': resource.description,
                            'resource_type_id': resource.resource_type_id.id,
                            'uom_id': resource.uom_id.id,
                            'qty': rec.qty * resource.qty,
                            'real_qty': rec.qty * resource.qty,
                            'subtotal': (
                                rec.qty * resource.qty * (
                                    resource.product_id.lst_price))
                        })
        return res

    @api.multi
    @api.depends('resource_line_ids')
    def _compute_resources_line_ids(self):
        for rec in self:
            resources = rec.resource_line_ids.search(
                [('task_resource_id', '=', rec.id)])
            for resource in resources:
                rec.update({'resource_line_ids': resource})

    @api.multi
    def insume_explotion(self):
        return {
            'name': 'Insume Explotion',
            'view_type': 'form',
            'view_mode': 'tree',
            'res_model': 'analytic.resource.plan.line',
            'domain': [('account_id', '=', self.analytic_account_id.id)],
            'type': 'ir.actions.act_window'}

    @api.multi
    def action_button_confirm(self):
        for rec in self:
            rec.state = 'confirm'

    @api.multi
    def action_button_draft(self):
        for rec in self:
            if rec.resource_line_ids:
                raise exceptions.ValidationError(
                    _("You can't reset the concept because it already"
                        " has resources"))
            rec.state = 'draft'
