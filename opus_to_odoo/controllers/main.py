# -*- coding: utf-8 -*-
# Copyright <2017> <Jarsa Sistemas, S.A. de C.V.>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import base64

from openerp import http
from openerp.addons.web.controllers.main import content_disposition
from openerp.http import request


class Binary(http.Controller):

    @http.route('/web/binary/download_document', type='http', auth="public")
    def download_document(self, wizard_id, **kw):
        wizard = request.registry['download.issues.file']
        cr, uid, context = request.cr, request.uid, request.context
        res = wizard.read(
            cr, uid, [int(wizard_id)], ['issue_file'], context)[0]
        filecontent = base64.b64decode(res.get('issue_file') or '')
        if not filecontent:
            return request.not_found()
        else:
            return request.make_response(
                filecontent,
                [('Content-Type', 'application/octet-stream'),
                 ('Content-Disposition',
                  content_disposition('project_misses.txt'))])
