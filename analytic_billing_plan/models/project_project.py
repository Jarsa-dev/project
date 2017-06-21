# -*- coding: utf-8 -*-
# © <2016> <Jarsa Sistemas, S.A. de C.V.>
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import _, api, exceptions, fields, models


class ProjectProject(models.Model):
    _inherit = 'project.project'

    billing_project_total = fields.Float(
        'Billing Total',
        compute='_compute_billing_project_total',)
    project_amortization = fields.Float(
        string='Project Amortization',
        digits=(14, 7),)
    advance_invoice_id = fields.Many2one(
        comodel_name='account.invoice',
        string='Advance Invoice',
        readonly=True,
        )
    project_retention = fields.Float(
        string='Project Retention',
        digits=(14, 4),)
    retention_invoice_id = fields.Many2one(
        comodel_name='account.invoice',
        string='Retention Invoice',
        readonly=True, )

    @api.multi
    @api.constrains('project_amortization')
    def _validate_amortization_percentage(self):
        for rec in self:
            if rec.project_amortization > 100 or rec.project_amortization < 0:
                raise exceptions.ValidationError(
                    _('The percentage value must be between 0 and 100.'))

    @api.multi
    @api.constrains('project_retention')
    def _validate_retention_percentage(self):
        for rec in self:
            if rec.project_retention > 100 or rec.project_retention < 0:
                raise exceptions.ValidationError(
                    _('The percentage value of the  must be'
                        'between 0 and 100.'))

    @api.multi
    def _compute_billing_project_total(self):
        for rec in self:
            wbs_elements = self.env['project.wbs_element'].search([
                ('project_id', '=', rec.id)])
            if wbs_elements:
                for wbs_element in wbs_elements:
                    rec.billing_project_total += (
                        wbs_element.billing_concept_total)
            else:
                rec.billing_project_total = 0.0
            if (rec.advance_invoice_id and
                    rec.advance_invoice_id.state == 'open'):
                    rec.billing_project_total += (
                        rec.advance_invoice_id.amount_untaxed)

    @api.multi
    def make_advance_invoice(self):
        for rec in self:
            total_invoice = 0.0
            if rec.advance_invoice_id:
                raise exceptions.ValidationError(
                    _('You can not create the invoice because '
                        'the project already has an invoice.'))
            if rec.project_amortization > 0:
                for wbs_element in rec.wbs_element_ids:
                    for task in wbs_element.task_ids:
                        if task.state != 'confirm':
                            raise exceptions.ValidationError(
                                _('All of the concepts must be confirmed to'
                                    'create the invoice.'))
                        total_invoice += task.real_subtotal
            advance_product = self.env.ref(
                'analytic_billing_plan.product_amortization')
            if len(advance_product) == 0:
                raise exceptions.ValidationError(
                    _('Amortization product not found, please contact your'
                        'system administrator.'))
            client_account = rec.partner_id.property_account_receivable_id.id
            if not client_account:
                raise exceptions.ValidationError(
                    _('You must have the receivable account for the project'
                        'client.'))
            product_account = (
                advance_product.property_account_expense_id
                if advance_product.property_account_expense_id
                else advance_product.categ_id.property_account_expense_categ_id
                if advance_product.categ_id.property_account_expense_categ_id
                else False)
            if not product_account:
                raise exceptions.ValidationError(
                    _('You must have the expense account for the advance'
                        'product.'))
            lines = []
            total = (total_invoice * (float(rec.project_amortization) / 100))
            lines.append(
                (0, 0, {
                    'product_id': advance_product.id,
                    'uom_id': self.env.ref('product.product_uom_unit').id,
                    'quantity': 1.0,
                    'price_unit': total,
                    'name': rec.name + _(' Advance Amortization'),
                    'invoice_line_tax_ids': [(6, 0, [
                        x.id for x in advance_product.taxes_id])],
                    'account_analytic_id': rec.analytic_account_id.id,
                    'account_id': product_account.id,
                }))

            invoice_id_create = self.env['account.invoice'].create({
                'project_id': rec.id,
                'partner_id': rec.partner_id.id,
                'date_invoice': fields.Date.today(),
                'fiscal_position_id': (
                    rec.partner_id.property_account_position_id.id),
                'reference': rec.name,
                'currency_id': self.env.user.company_id.currency_id.id,
                'account_id': client_account,
                'payment_term_id': rec.partner_id.property_payment_term_id.id,
                'type': 'out_invoice',
                'invoice_line_ids': [line for line in lines],
            })
            rec.advance_invoice_id = invoice_id_create.id

            return {
                'name': 'Customer Invoice',
                'view_id': self.env.ref(
                    'account.invoice_form').id,
                'view_type': 'form',
                'view_mode': 'form',
                'target': 'current',
                'res_model': 'account.invoice',
                'res_id': invoice_id_create.id,
                'type': 'ir.actions.act_window',
            }

    @api.multi
    def make_retention_invoice(self):
        for rec in self:
            total_invoice = 0.0
            if rec.retention_invoice_id:
                raise exceptions.ValidationError(
                    _('You can not create the invoice because '
                        'the project already has a retention invoice.'))
            if rec.project_retention > 0:
                for wbs_element in rec.wbs_element_ids:
                    for task in wbs_element.task_ids:
                        if task.state != 'confirm':
                            raise exceptions.ValidationError(
                                _('All of the concepts must be confirmed to'
                                    ' create the invoice.'))
                        if task.remaining_quantity > 0.0:
                            raise exceptions.ValidationError(
                                _('All the tasks must be invoiced to'
                                    ' continue with the retention invoice.'))
                        total_invoice += task.real_subtotal
            retention_product = self.env.ref(
                'analytic_billing_plan.product_retention')
            if len(retention_product) == 0:
                raise exceptions.ValidationError(
                    _('Amortization product not found, please contact your'
                        ' system administrator.'))
            client_account = rec.partner_id.property_account_receivable_id.id
            if not client_account:
                raise exceptions.ValidationError(
                    _('You must have the receivable account for the project'
                        ' client.'))
            product_account = (
                retention_product.property_account_expense_id
                if retention_product.property_account_expense_id
                else retention_product.categ_id.
                property_account_expense_categ_id
                if retention_product.categ_id.property_account_expense_categ_id
                else False)
            if not product_account:
                raise exceptions.ValidationError(
                    _('You must have the expense account for the retention'
                        'product.'))
            lines = []
            total = (total_invoice * (float(rec.project_retention) / 100))
            lines.append(
                (0, 0, {
                    'product_id': retention_product.id,
                    'uom_id': self.env.ref('product.product_uom_unit').id,
                    'quantity': 1.0,
                    'price_unit': total,
                    'name': rec.name + _(' Retention'),
                    'invoice_line_tax_ids': [(6, 0, [
                        x.id for x in retention_product.taxes_id])],
                    'account_analytic_id': rec.analytic_account_id.id,
                    'account_id': product_account.id,
                }))

            invoice_id_create = self.env['account.invoice'].create({
                'project_id': rec.id,
                'partner_id': rec.partner_id.id,
                'date_invoice': fields.Date.today(),
                'fiscal_position_id': (
                    rec.partner_id.property_account_position_id.id),
                'reference': rec.name,
                'currency_id': self.env.user.company_id.currency_id.id,
                'account_id': client_account,
                'payment_term_id': rec.partner_id.property_payment_term_id.id,
                'type': 'out_invoice',
                'invoice_line_ids': [line for line in lines],
            })
            rec.retention_invoice_id = invoice_id_create.id

            return {
                'name': 'Customer Invoice',
                'view_id': self.env.ref(
                    'account.invoice_form').id,
                'view_type': 'form',
                'view_mode': 'form',
                'target': 'current',
                'res_model': 'account.invoice',
                'res_id': invoice_id_create.id,
                'type': 'ir.actions.act_window',
            }
