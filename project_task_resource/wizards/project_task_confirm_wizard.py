# -*- coding: utf-8 -*-
# <2016> <Jarsa Sistemas, S.A. de C.V.>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class ProjectTaskConfirmWizard(models.TransientModel):

    _name = 'project.task.confirm.wizard'

    @api.multi
    def confirm_tasks(self):
        active_ids = self.env['project.task'].browse(
            self._context.get('active_ids'))
        if not active_ids:
            return {}

        for task in active_ids:
            if task.state != 'confirm':
                task.state = 'confirm'
