# -*- coding: utf-8 -*-
# <2016> <Jarsa Sistemas, S.A. de C.V.>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from datetime import datetime
from odoo import api, fields, models
from odoo.exceptions import ValidationError
from odoo.tools.translate import _


class PurchaseRequest(models.TransientModel):

    _name = 'purchase.request.wizard'
    _description = 'Request for quotation wizard'

    item_ids = fields.One2many(
        'purchase.request.line.wizard',
        'wiz_id', string='Items')
    project_id = fields.Many2one(
        'project.project')
    location_id = fields.Many2one(
        'stock.location')

    @api.model
    def _prepare_item(self, line):
        return {
            'line_id': line.id,
            'analytic_account_id': line.account_id.id,
            'product_id': line.product_id.id,
            'uom_id': line.uom_id.id,
            'qty': line.qty,
            'real_qty': line.real_qty,
            'requested_qty': line.requested_qty,
            'qty_to_request': line._get_available_qty()
        }

    @api.model
    def default_get(self, fields):
        res = super(PurchaseRequest, self).default_get(
            fields)
        resource_line_obj = self.env['analytic.resource.plan.line']
        resource_line_ids = self.env.context['active_ids'] or []
        active_model = self.env.context['active_model']

        if not resource_line_ids:
            return res
        assert active_model == 'analytic.resource.plan.line', \
            'Bad context propagation'

        items = []
        control = 0
        project_validator = False
        state_validator = False
        for line in resource_line_obj.browse(resource_line_ids):
            if control == 0:
                old_project = line.task_resource_id.project_id.id
                current_project = line.task_resource_id.project_id.id
                control = 1
            else:
                current_project = line.task_resource_id.project_id.id
            if old_project != current_project:
                project_validator = True
            elif line.task_resource_id.state != 'confirm':
                state_validator = True
            else:
                old_project = line.task_resource_id.project_id.id
                items.append((0, 0, self._prepare_item(line)))

        if project_validator:
            raise ValidationError(
                _('The resources of the tasks must be in the same project.'))
        elif state_validator:
            raise ValidationError(
                _('The concept must be confirmed \n \n'
                    'Resource: %s \n Concept: %s.') %
                (line.product_id.name, line.task_resource_id.name))
        res['item_ids'] = items
        res['project_id'] = old_project
        res['location_id'] = self.env['project.project'].search(
            [('id', '=', old_project)]).location_id.id
        return res

    @api.multi
    def make_request(self):
        lines = []
        for rec in self:
            for item in rec.item_ids:
                value = item.requested_qty + item.qty_to_request
                if value > item.real_qty or item.qty_to_request <= 0:
                    raise ValidationError(
                        _(
                            'You cannot request more products than you planned'
                            '.or null quantities.'
                            '\n \n Resource: %s'
                            '\n Concept: %s') % (
                            item.product_id.name,
                            item.line_id.task_resource_id.name))
        today = datetime.strptime(fields.Datetime.now(), "%Y-%m-%d %H:%M:%S")
        for item in self.item_ids:
            product_uom_id = item.product_id.uom_po_id.id
            if item.uom_id.id != item.product_id.uom_po_id.id:
                product_uom_qty = self.env['product.uom']._compute_qty(
                    item.uom_id.id,
                    item.qty_to_request,
                    item.product_id.uom_po_id.id,
                    round=False)
            else:
                product_uom_qty = item.qty_to_request
            line = (0, 0, {
                'product_id': item.product_id.id,
                'name': item.line_id.description,
                'product_uom_id': product_uom_id,
                'product_qty': product_uom_qty,
                'date_required': today,
                'analytic_account_id': item.analytic_account_id.id,
                'is_project_insume': True,
                })
            lines.append(line)
        order = ({
            'company_id': self.env.user.company_id.id,
            'picking_type_id': self.project_id.picking_in_id.id,
            'requested_by': self.env.user.id,
            'project_id': self.project_id.id,
            'name': self.env['purchase.request']._get_default_name(),
            'line_ids': lines,
            })
        purchase = self.env['purchase.request'].create(order)
        for item in self.item_ids:
            item.line_id.write({'purchase_request_ids': [(4, purchase.id)]})
        return {
            'name': 'Purchase Request',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'purchase.request',
            'res_id': purchase.id,
            'target': 'current',
            'type': 'ir.actions.act_window',
            }
