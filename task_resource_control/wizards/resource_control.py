# -*- coding: utf-8 -*-0
# <2016> <Jarsa Sistemas, S.A. de C.V.>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class ResourceControl(models.TransientModel):

    _name = 'resource.control.wizard'
    _description = 'Make Product Consumes'

    item_ids = fields.One2many(
        'resource.control.line',
        'wiz_id', string='Items')

    @api.model
    def _prepare_item(self, line, model):
        if model == 'project.task':
            dic = {
                'task_id': line.id,
                'uom_id': line.uom_id.id,
                'qty': line.qty,
                'real_qty': line.real_qty,
                'unit_price': line.unit_price,
                'subtotal': line.subtotal,
                'analytic_account_id': line.analytic_account_id.id
            }
        else:
            dic = {
                'task_id': line.task_resource_id.id,
                'line_id': line.id,
                'real_qty': line.real_qty,
                'analytic_account_id': line.account_id.id,
                'product_id': line.product_id.id,
                'qty': line.qty,
                'description': line.description or line.product_id.name,
                'uom_id': line.uom_id.id
            }
        return dic

    @api.model
    def default_get(self, fields):
        res = super(ResourceControl, self).default_get(
            fields)
        active_model = self.env.context['active_model']
        active_obj = self.env[active_model]
        active_ids = self.env.context['active_ids'] or []

        if not active_ids:
            return res

        items = []
        for line in active_obj.browse(active_ids):
            items.append([0, 0, self._prepare_item(line, active_model)])
        res['item_ids'] = items
        return res

    @api.multi
    def make_control(self):
        for rec in self:
            active_model = self.env.context['active_model']
            for item in rec.item_ids:
                if active_model == 'analytic.resource.plan.line':
                    project_id = item.line_id.task_resource_id.project_id.id
                    qty_real = item.line_id.real_qty
                    requested_qty = item.line_id.requested_qty
                    analytic_account = item.line_id.account_id.id
                    if item.line_id.qty_consumed > item.new_qty:
                        raise ValidationError(
                            _("The new quantity must be greather "
                                "than the quantity consumed."))
                    resource_line = item.line_id
                else:
                    project_id = item.task_id.project_id.id
                    qty_real = item.task_id.real_qty
                    total_resource = {
                        x.product_id.name: x.requested_qty
                        for x in item.task_id.resource_line_ids}
                    for resource in item.task_id.resource_ids:
                        requested_qty = total_resource[
                            resource.product_id.name]
                        new_qty = (item.new_qty * resource.qty)
                        if new_qty < requested_qty:
                            raise ValidationError(
                                _("The new quantity can not be less than "
                                  "the requested quantity. Product: %s" %
                                  resource.product_id.name))
                    analytic_account = item.task_id.analytic_account_id.id
                    resource_line = item.task_id
                    item.task_id._update_real_qty(item.new_qty)

                if qty_real > item.new_qty:
                    item.type = 'deductive'
                elif qty_real < item.new_qty:
                    item.type = 'additive'
                elif item.new_qty < requested_qty:
                    raise ValidationError(
                        _("The new quantity can not be less than "
                          "the requested quantity."))
                else:
                    raise ValidationError(
                        _("The new quantity must be greather or "
                          "smaller than the real quantity."))

                resource_line.write({'real_qty': item.new_qty})

                change_id = self.env['resource.control'].create({
                    'project_id': project_id,
                    'insume_explotion_id': item.line_id.id,
                    'task_id': item.task_id.id,
                    'product_id': item.product_id.id,
                    'type': item.type,
                    'analytic_account_id': analytic_account,
                    'new_qty': item.new_qty,
                    'reason': item.reason,
                    })
        return {
            'name': 'Resource Control',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'resource.control',
            'res_id': change_id.id,
            'target': 'current',
            'type': 'ir.actions.act_window',
            }
