# -*- coding: utf-8 -*-
# Copyright <2017> <Jarsa Sistemas, S.A. de C.V.>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import _, api, fields, models
import base64


class ImportData(models.TransientModel):
    _name = 'import.data'

    file = fields.Binary(required=True,)
    new_file = fields.Binary()
    new_file_name = fields.Char()
    nbr_issues = fields.Integer()

    @api.model
    def _check_data(self, file):
        document = base64.b64decode(file)
        lines = document.split('\n')

        misses = []
        for row in lines:
            if len(row) > 0:
                if row[1] == 'C':
                    data = row.split(',"s#')
                    row_type = data[0].replace('"', '')
                    code = data[1].replace('"', '')
                    name = data[2].replace('"', '')
                    uom_name = data[3].replace('"', '')
                else:
                    data = row.split(',')
                    row_type = data[0].replace('"', '')
                    code = data[1]
                    name = data[2]
                    uom_name = data[3]

                project = data[6]
                if ('"') in project:
                    project = project.replace('"', '')
                uom_id = self.env['product.uom'].search(
                    [('name', '=ilike', uom_name)])
                project_id = self.env['project.project'].search(
                    [('name', '=', project)])
                if len(project_id) == 0:
                    if not ("Proyecto no encontrado en el sistema.") in misses:
                        misses.append("Proyecto no encontrado en el sistema.")

                if row_type == unicode('Subcapitulo', encoding='latin-1'):
                    wbs_element = self.env['project.wbs_element'].search(
                        [('code', '=', code)])
                    if len(wbs_element) > 0:
                        if not (
                            "Ya existe un elemento EDT con el codigo: " +
                                str(code)) in misses:
                            misses.append(
                                "Ya existe un elemento EDT con el codigo: " +
                                str(code))
                        continue

                elif row_type == 'EDT_Hijo':
                    wbs_element = self.env['project.wbs_element'].search(
                        [('code', '=', code)])
                    if len(wbs_element) > 0:
                        if not (
                            "Ya existe un elemento EDT con el codigo: " +
                                str(code)) in misses:
                            misses.append(
                                "Ya existe un elemento EDT con el codigo: " +
                                str(code))
                        continue

                elif row_type == 'Concepto':
                    if len(uom_id) == 0:
                        if not(
                            "No existe la unidad de medida: " +
                                str(uom_name)) in misses:
                            misses.append(
                                "No existe la unidad de medida: " +
                                str(uom_name))
                        continue

                elif row_type == 'Insumo':
                    product_id = self.env['product.product'].search(
                        [('default_code', '=', code)])
                    if len(product_id) == 0:
                        if not(
                            "No se econtro el producto con el codigo: " +
                                code + " de nombre: " + name) in misses:
                            misses.append(
                                "No se econtro el producto con el codigo: " +
                                code + " de nombre: " + name)
                    if len(uom_id) == 0:
                        if not(
                            "No existe la unidad de medida: " +
                                str(uom_name)) in misses:
                            misses.append(
                                "No existe la unidad de medida: " +
                                str(uom_name))
                        continue

                elif row_type == 'Insumo_Servicio':
                    product_service = self.env.ref(
                        '__export__.product_product_3812')
                    if len(product_service) == 0:
                        if not (
                            "No se encuentra el producto para"
                                "los servicios") in misses:
                            misses.append(
                                "No se encuentra el producto"
                                "para subcontratos")
                    if len(uom_id) == 0:
                        if not(
                            "No existe la unidad de medida: " +
                                str(uom_name)) in misses:
                            misses.append(
                                "No existe la unidad de medida: " +
                                str(uom_name))
                        continue

        if len(misses) > 0:
            content = ''
            for miss in misses:
                content += miss + '\n'
            self.new_file = base64.encodestring(content)
            self.nbr_issues = len(misses)
            return False
        else:
            return True

    @api.multi
    def import_data(self):
        if not self._check_data(self.file):
            return {
                'name': _('Data Issues'),
                'view_type': 'form',
                'view_mode': 'form',
                'view_id': self.env.ref(
                    'opus_to_odoo.view_download_issues_file').id,
                'res_model': 'download.issues.file',
                'target': 'new',
                'type': 'ir.actions.act_window',
                'context': {
                    'default_issue_qty': self.nbr_issues,
                    'default_issue_file': self.new_file,
                }
            }
