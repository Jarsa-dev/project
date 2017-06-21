# -*- coding: utf-8 -*-
# Copyright <2016> <Jarsa Sistemas, S.A. de C.V.>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class AnalyticBillingPlan(models.Model):
    _name = 'analytic.billing.plan'
    _description = "Analytic Billing Plan"
    _inherit = ['mail.thread', 'ir.needaction_mixin']

    name = fields.Char()
    customer_id = fields.Many2one(
        'res.partner', string="Customer", readonly=True)
    state = fields.Selection(
        [('draft', 'Draft'),
         ('confirm', 'Confirmed')], string='State',
        default='draft')
    date = fields.Date('Date', required=True, default=fields.Date.today)
    currency_id = fields.Many2one(
        'res.currency',
        string='Currency',
        default=lambda self: self.env.user.company_id.currency_id)
    project_id = fields.Many2one(
        'project.project',
        string='Project')
    analytic_billing_plan_line_ids = fields.One2many(
        'analytic.billing.plan.line',
        'analytic_billing_plan_id',
        string="Analytic Billing Plan Lines",
        readonly=True, )
    invoice_id = fields.Many2one(
        'account.invoice',
        string="Invoice",)

    @api.multi
    def action_button_confirm(self):
        for rec in self:
            account_move_obj = self.env['account.move']
            if not self.env.user.company_id.bridge_account_id:
                raise ValidationError(
                    _('You must have a bridge account assigned'
                        ' in the company configurations.'))
            if not self.env.user.company_id.billing_request_journal_id:
                raise ValidationError(
                    _('You must have an account journal for the moves assigned'
                        ' in the company configurations.'))
            for line in rec.analytic_billing_plan_line_ids:
                if line.amount < 0:
                    raise ValidationError(
                        _('The amount must be higher than zero.'))
                total = rec.currency_id.compute(
                    line.amount,
                    self.env.user.currency_id)
                accounts = {'credit': line.account_id.id,
                            'debit': (
                                self.env.user.company_id.bridge_account_id.id)}
                move_lines = []
                for name, account in accounts.items():
                    move_line = (0, 0, {
                        'name': line.analytic_billing_plan_id.name,
                        'account_id': account,
                        'narration': line.ref,
                        'debit': (total if name == 'debit' else 0.0),
                        'credit': (total if name == 'credit' else 0.0),
                        'journal_id': (
                            self.env.user.company_id.
                            billing_request_journal_id.id),
                        'analytic_account_id': line.account_analytic_id.id,
                        'project_id': (
                            line.analytic_billing_plan_id.project_id.id),
                        'task_id': line.task_id.id,
                        'partner_id': (
                            line.analytic_billing_plan_id.
                            project_id.partner_id.id),
                    })
                    move_lines.append(move_line)
                move = {
                    'date': fields.Date.today(),
                    'journal_id': (
                        self.env.user.company_id.
                        billing_request_journal_id.id),
                    'name': _('Billing Request Line: %s') %
                             (line.task_id.description),
                    'line_ids': [x for x in move_lines],
                }
                move_id = account_move_obj.create(move)
                line.write({
                    'move_id': move_id.id,
                    })
            rec.write({
                'state': 'confirm',
                })
            rec.message_post(
                _('<strong>Billing Request Confirmed.</strong><ul>'
                  '<li><strong>Confirmed by: </strong>%s</li>'
                  '<li><strong>Confirmed at: </strong>%s</li>'
                  '</ul>') % (self.env.user.name, fields.Datetime.now()))

    @api.multi
    def action_button_draft(self):
        for rec in self:
            if rec.state == 'paid':
                raise ValidationError(
                    _('You can not delete a billing request'
                      'with a paid invoice.'))
            for line in rec.analytic_billing_plan_line_ids:
                line.move_id.unlink()
                line.write(
                    {
                        'state': 'draft',
                    })
            rec.write({'state': 'draft'})
            rec.message_post(
                _('<strong>Billing Request Drafted.</strong><ul>'
                  '<li><strong>Confirmed by: </strong>%s</li>'
                  '<li><strong>Confirmed at: </strong>%s</li>'
                  '</ul>') % (self.env.user.name, fields.Datetime.now()))

    @api.multi
    def make_project_invoices(self):
        total = 0.0
        invoice_names = ''
        lines = []
        for rec in self:
            if rec.invoice_id:
                raise ValidationError(
                    _('The billing request already has an invoice.'))
            if not rec.state == 'confirm':
                raise ValidationError(
                    _('The billing request must be confirmed.'))

            partner = rec.customer_id.id
            project = rec.project_id
            currency = rec.currency_id
            for invoice in rec.analytic_billing_plan_line_ids:
                total += currency.compute(
                    invoice.amount, self.env.user.currency_id)
                invoice_names += ' ' + invoice.name + ', '

            if total > 0.0:
                lines.append(
                    (0, 0, {
                        'product_id': self.env.ref(
                            'analytic_billing_plan.product_concept').id,
                        'quantity': 1.0,
                        'price_unit': total,
                        'uom_id': self.env.ref(
                            'product.product_uom_unit').id,
                        'name': project[0].name + _(' Payment'),
                        'invoice_line_tax_ids': [(6, 0, [
                            x.id for x in self.env.user.
                            company_id.product_id.taxes_id])],
                        'account_id': (
                            self.env.user.company_id.bridge_account_id.id),
                    }))

            if project.project_amortization > 0:
                product_amortization = self.env.ref(
                    'analytic_billing_plan.'
                    'product_amortization')
                if len(product_amortization) == 0:
                    raise ValidationError(
                        _('You must have a product for project '
                            'amortizations.'))
                product_account = (
                    product_amortization.property_account_expense_id
                    if product_amortization.property_account_expense_id
                    else product_amortization.categ_id.
                    property_account_expense_categ_id
                    if product_amortization.categ_id.
                    property_account_expense_categ_id
                    else False)
                if not product_account:
                    raise ValidationError(
                        _('You must have an account for the product'))
                percentage_rate = float(project.project_amortization) / 100
                lines.append(
                    (0, 0, {
                        'product_id': product_amortization.id,
                        'quantity': 1.0,
                        'price_unit': (total * percentage_rate) * -1.0,
                        'name': project.name + _(' Amortization'),
                        'uom_id': (
                            self.env.ref('product.product_uom_unit').id),
                        'invoice_line_tax_ids': [(6, 0, [
                            x.id for x in product_amortization.taxes_id])],
                        'account_id': product_account.id,
                    }))

            if project.project_retention > 0:
                product_retention = self.env.ref(
                    'analytic_billing_plan.'
                    'product_retention')
                if len(product_retention) == 0:
                    raise ValidationError(
                        _('You must have a product for project '
                            'retentions.'))
                product_account = (
                    product_retention.property_account_expense_id
                    if product_retention.property_account_expense_id
                    else product_retention.categ_id.
                    property_account_expense_categ_id
                    if product_retention.categ_id.
                    property_account_expense_categ_id
                    else False)
                if not product_account:
                    raise ValidationError(
                        _('You must have an account for the product'))
                percentage_rate = float(project.project_retention) / 100
                lines.append(
                    (0, 0, {
                        'product_id': product_retention.id,
                        'quantity': 1.0,
                        'price_unit': (total * percentage_rate) * -1.0,
                        'name': project.name + _(' Retention'),
                        'uom_id': self.env.ref(
                            'product.product_uom_unit').id,
                        'invoice_line_tax_ids': [(6, 0, [
                            x.id for x in product_retention.taxes_id])],
                        'account_id': product_account.id,
                    }))

            invoice_id_create = self.env['account.invoice'].create({
                'project_id': project.id,
                'partner_id': partner,
                'date_invoice': fields.Date.today(),
                'fiscal_position_id': (
                    project.partner_id.property_account_position_id.id),
                'reference': invoice.ref,
                'name': invoice_names,
                'currency_id': invoice.analytic_billing_plan_id.currency_id.id,
                'payment_term_id': (
                    project.partner_id.property_payment_term_id.id),
                'account_id': (
                    project.partner_id.property_account_receivable_id.id),
                'type': 'out_invoice',
                'invoice_line_ids': [line for line in lines],
            })
            rec.invoice_id = invoice_id_create.id

            return {
                'name': 'Customer Invoice',
                'view_id': self.env.ref(
                    'account.invoice_form').id,
                'view_type': 'form',
                'view_mode': 'form',
                'target': 'current',
                'res_model': 'account.invoice',
                'res_id': invoice_id_create.id,
                'type': 'ir.actions.act_window'
            }

    @api.model
    def create(self, vals):
        res = super(AnalyticBillingPlan, self).create(vals)
        res.name = self.env['ir.sequence'].next_by_code('billing.request')
        count = 1
        for line in res.analytic_billing_plan_line_ids:
            line.name = self.assign_code(res, count)
            count += 1
        return res

    @api.model
    def assign_code(self, br, count):
        name = br.name + '-' + str(count)
        return name

    @api.multi
    def unlink(self):
        for rec in self:
            if rec.invoice_id:
                raise ValidationError(
                    _('The Billing Request already has an invoice.'))
            rec.analytic_billing_plan_line_ids.unlink()
            return super(AnalyticBillingPlan, self).unlink()
