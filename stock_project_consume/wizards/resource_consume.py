# -*- coding: utf-8 -*-0
# <2016> <Jarsa Sistemas, S.A. de C.V.>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from openerp import _, api, exceptions, fields, models


class ResourceConsume(models.TransientModel):

    _name = 'resource.consume'
    _description = 'Make Product Consumes'

    item_ids = fields.One2many(
        'resource.consume.line',
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
            'real_qty': line.real_qty,
            'qty_on_hand': line.qty_on_hand,
            'qty_to_consume': line.remaining_qty,
            'qty_consumed': line.qty_consumed,
        }

    @api.model
    def default_get(self, fields):
        res = super(ResourceConsume, self).default_get(
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
                items.append([0, 0, self._prepare_item(line)])

        if project_validator:
            raise exceptions.ValidationError(
                _('The resources must be for the same project.'))
        elif state_validator:
            raise exceptions.ValidationError(
                _('The concept must be confirmed \n \n'
                    'Resource: %s \n Concept: %s.') %
                (line.product_id.name, line.task_resource_id.name))
        res['item_ids'] = items
        res['project_id'] = old_project
        res['location_id'] = self.env['project.project'].search(
            [('id', '=', old_project)]).location_id.id
        return res

    @api.multi
    def make_consume(self):
        stock_picking_obj = self.env['stock.picking']
        moves = []
        for item in self.item_ids:
            total_qty = item.line_id.qty_consumed + item.qty_to_consume
            if item.qty_to_consume <= 0:
                raise exceptions.ValidationError(
                    _('The quantity to consume must be higher than zero'
                        'Please check your data.\n'
                        '\n Resource: %s \n Concept: %s')
                    %
                    (item.product_id.name, item.line_id.task_resource_id.name))
            elif item.qty_to_consume > item.qty_on_hand:
                raise exceptions.ValidationError(
                    _('The quantity to consume must be lower or equal '
                        'than the quantity on hand. Please check your data.\n'
                        '\n Resource: %s \n Concept: %s')
                    %
                    (item.product_id.name, item.line_id.task_resource_id.name))
            elif not item.line_id.task_resource_id.project_id.picking_out_id:
                raise exceptions.ValidationError(
                    _('The project must have a picking type for the consume.'))
            elif item.qty_to_consume > item.real_qty:
                raise exceptions.ValidationError(
                    _('The quantity to consume must be lower or equal'
                        ' than the quantity planned. Please check your data.\n'
                        '\n Resource: %s \n Concept: %s') %
                    (item.product_id.name, item.line_id.task_resource_id.name))
            elif total_qty > item.real_qty:
                raise exceptions.ValidationError(
                    _('You cannot consume this quantity because the sumatory'
                        ' of the quantity exceeds the quantity planned.'
                        ' Please check your data. \n \n Resource: %s \n'
                        'Concept: %s') %
                    (item.product_id.name, item.line_id.task_resource_id.name))
            today = fields.Datetime.now()
            move = (0, 0, {
                'company_id': self.env.user.company_id.id,
                'date': today,
                'location_dest_id': (
                    item.line_id.task_resource_id.project_id.
                    picking_out_id.default_location_dest_id.id),
                'location_id': (
                    item.line_id.task_resource_id.project_id.
                    picking_out_id.default_location_src_id.id),
                'name': (item.product_id.name),
                'product_id': item.product_id.id,
                'product_uom': item.uom_id.id,
                'product_uom_qty': item.qty_to_consume,
                'account_analytic_id': item.analytic_account_id.id,
                'project_id': item.line_id.task_resource_id.project_id.id,
                'task_id': item.line_id.task_resource_id.id,
                })
            moves.append(move)
        picking_dict = {
            'company_id': self.env.user.company_id.id,
            'move_lines': moves,
            'picking_type_id': self.project_id.picking_out_id.id,
            'location_dest_id': (
                self.project_id.picking_out_id.default_location_dest_id.id),
            'location_id': self.location_id.id,
        }
        picking = stock_picking_obj.create(picking_dict)
        return {
            'name': 'Picking',
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'current',
            'res_model': 'stock.picking',
            'res_id': picking.id,
            'type': 'ir.actions.act_window'
            }
