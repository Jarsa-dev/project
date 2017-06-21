# -*- coding: utf-8 -*-
# Copyright <2012> <Israel Cruz Argil, Argil Consulting>
# Copyright <2016> <Jarsa Sistemas, S.A. de C.V.>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from odoo import _, api, exceptions, fields, models


class WizardBillingPlan(models.TransientModel):
    _name = 'wizard.billing.plan'

    item_ids = fields.One2many(
        'wizard.billing.plan.line',
        'billing_request_id', string='Items')

    @api.model
    def _prepare_item(self, line):
        return {
            'project_task': line.id,
            'remaining_quantity': line.remaining_quantity,
            'unit_price': line.unit_price,
            'qty': line.qty,
            'quantity_invoice': line.remaining_quantity,
            'total_invoice': line.remaining_quantity * line.unit_price,
        }

    @api.model
    def default_get(self, fields):
        res = super(WizardBillingPlan, self).default_get(
            fields)
        project_task_obj = self.env['project.task']
        billing_line_ids = self.env.context['active_ids'] or []
        active_model = self.env.context['active_model']
        if not billing_line_ids:
            return res
        assert active_model == 'project.task', \
            'Bad context propagation'

        items = []
        control = 0
        for line in project_task_obj.browse(billing_line_ids):
            if control == 0:
                old_project = line.project_id.id
                current_project = line.project_id.id
                control = 1
            else:
                current_project = line.project_id.id
            if old_project != current_project:
                raise exceptions.ValidationError(
                    _('The concepts must be for the same project.'
                        'Concept: %s.') % (line.name))
            elif line.state != 'confirm':
                raise exceptions.ValidationError(
                    _('The concept must be confirmed \n \n'
                        'Concept: %s.') %
                    (line.name))
            elif line.remaining_quantity <= 0:
                raise exceptions.ValidationError(
                    _('The concept billing is complete.\n \n'
                        'Concept: %s.') %
                    (line.name))
            else:
                old_project = line.project_id.id
                items.append([0, 0, self._prepare_item(line)])
        res['item_ids'] = items
        return res

    @api.multi
    def create_billing(self):
        for rec in self:
            lines = []
            customers = []
            projects = []
            for item in rec.item_ids:
                if item.remaining_quantity < 0.0:
                    raise exceptions.ValidationError(
                        _('The quantity to invoice must be less than'
                            ' the remaining quantity'))
                if item.project_task.state != 'confirm':
                    raise exceptions.ValidationError(
                        _('The concept must be confirmed.'))
                billing = self.env['analytic.billing.plan']
                ref = False
                active_order = False
                if item.qty == item.quantity_invoice:
                    ref = _(
                        "Total Billing of: Concept: %s - Quantity: %s" % (
                            item.project_task.description,
                            item.quantity_invoice,))
                    active_order = False
                elif item.quantity_invoice < item.qty:
                    ref = _(
                        "Partial Billing of: Concept: %s - Quantity: %s" % (
                            item.project_task.description,
                            item.quantity_invoice,))
                    active_order = True
                lines.append(
                    (0, 0,
                        {
                            "account_id": (
                                self.env.user.company_id.product_id.
                                property_account_income_id.id
                                if self.env.user.company_id.product_id.
                                property_account_income_id.id
                                else
                                self.env.user.company_id.product_id.
                                categ_id.property_account_income_categ_id.id),
                            "ref": ref,
                            "price_unit": item.unit_price,
                            "product_uom_id": item.project_task.uom_id.id,
                            "quantity": item.quantity_invoice,
                            "task_id": item.project_task.id,
                            "amount": (
                                item.unit_price * item.quantity_invoice),
                            "account_analytic_id": (
                                item.project_task.analytic_account_id.id),
                            "has_active_order": active_order,
                        })
                    )
                customers.append(
                    item.project_task.project_id.partner_id.id)
                projects.append(
                    item.project_task.project_id.id)
            billing_request = {
                'customer_id': customers[0],
                'date': fields.Date.today(),
                'project_id': projects[0],
                "currency_id": self.env.user.company_id.currency_id.id,
                'analytic_billing_plan_line_ids': [line for line in lines],
            }
            billing_request_doc = billing.create(billing_request)
            return {
                'name': _('Billing Request'),
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'analytic.billing.plan',
                'res_id': billing_request_doc.id,
                'target': 'current',
                'type': 'ir.actions.act_window',
            }
