# -*- coding: utf-8 -*-
# Copyright <2017> <Jarsa Sistemas, S.A. de C.V.>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, fields, models


class DownloadIssusesFile(models.Model):
    _name = 'download.issues.file'

    issue_file = fields.Binary(string="Issues File",)
    issue_qty = fields.Integer(string="Issues Quantity",)

    @api.multi
    def download_file(self):
        for rec in self:
            return {
                'type': 'ir.actions.act_url',
                'url': '/web/binary/download_document?wizard_id=%s' % rec.id,
                'target': 'self',
            }
