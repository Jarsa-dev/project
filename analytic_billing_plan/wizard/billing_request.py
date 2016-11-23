# -*- coding: utf-8 -*-
# Copyright <2012> <Israel Cruz Argil, Argil Consulting>
# Copyright <2016> <Jarsa Sistemas, S.A. de C.V.>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from openerp import _, api, exceptions, fields, models


class WizardBillingPlan(models.TransientModel):
    _name = 'wizard.billing.plan'

    project_task = fields.Many2one('project.task')
    remaining_quantity = fields.Float(compute="_compute_remaining_quantity")
    total_invoice = fields.Float(compute='_compute_total_invoice')
    quantity_invoice = fields.Float()
    currency_id = fields.Many2one(
        'res.currency',
        string='Currency',
        default=lambda self: self.env.user.company_id.currency_id)
    unit_price = fields.Float()
    qty = fields.Float()

    @api.depends('quantity_invoice', 'unit_price')
    def _compute_total_invoice(self):
        for rec in self:
            rec.total_invoice = rec.quantity_invoice * rec.unit_price

    @api.depends('qty', 'quantity_invoice')
    def _compute_remaining_quantity(self):
        for rec in self:
            rec.remaining_quantity = rec.qty - rec.quantity_invoice

    @api.multi
    def create_billing(self):
        for rec in self:
            if rec.remaining_quantity < 0.0:
                raise exceptions.ValidationError(
                    _('The quantity to invoice must be less than'
                        'the remaining quantity'))
            billing = self.env['analytic.billing.plan']
            if rec.qty == rec.quantity_invoice:
                ref = _(
                    "Total Billing of: %s %s" % (
                        rec.quantity_invoice,
                        rec.project_task.uom_id.name))
                active_order = False
            if rec.quantity_invoice < rec.qty:
                ref = _(
                    "Partial Billing of: %s %s" % (
                        rec.quantity_invoice,
                        rec.project_task.uom_id.name))
                active_order = True
            rec.project_task.write(
                {'remaining_quantity': rec.remaining_quantity})
            billing.create({
                "account_id": (
                    rec.project_task.product_id.
                    property_account_income_id.id),
                "customer_id": rec.project_task.project_id.partner_id.id,
                "date": fields.Date.today(),
                "name": rec.project_task.name,
                "price_unit": rec.unit_price,
                "amount_currency": -(
                    rec.unit_price * rec.quantity_invoice),
                "product_uom_id": rec.project_task.uom_id.id,
                "currency_id": self.env.user.company_id.currency_id.id,
                "quantity": rec.quantity_invoice,
                "task_id": rec.project_task.id,
                "amount": (
                    rec.unit_price * rec.quantity_invoice),
                "company_id": self.env.user.company_id.id,
                "ref": ref,
                "account_analytic_id": rec.project_task.analytic_account_id.id,
                "has_active_order": active_order,
                "project_id": rec.project_task.project_id.id
            })

    @api.model
    def default_get(self, field):
        if 'active_id' in self.env.context:
            record_id = self.env.context['active_id']
            plan = self.env['project.task'].search(
                [('id', '=', record_id)])
            lines = plan.line_billing_ids.search(
                [('task_id', '=', plan.id)])
            res = super(WizardBillingPlan, self).default_get(field)
            res.update({
                'unit_price': plan.unit_price,
                'remaining_quantity': plan.remaining_quantity,
                'project_task': plan.id,
            })
            if len(lines) == 0:
                quantity = plan.qty
                res.update({'qty': quantity})
            else:
                for billing in lines:
                    if billing.has_active_order:
                        if plan.remaining_quantity > 0:
                            quantity = plan.remaining_quantity
                        else:
                            quantity = plan.qty
                        res.update({'qty': quantity})
                    else:
                        raise exceptions.ValidationError(
                            _('The quantity to invoice is zero.'))
            return res
        else:
            return super(WizardBillingPlan, self).default_get(field)
