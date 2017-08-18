# -*- coding: utf-8 -*-
# Copyright 2017, Jarsa Sistemas, S.A. de C.V.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from openerp import _, api, fields, models
from openerp.exceptions import UserError
from os import getenv
import pymssql
import base64
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


class ImportOpusWizard(models.TransientModel):
    _name = 'import.opus.wizard'

    project_ids = fields.Selection(
        string='Projects',
        selection="get_projects",)
    progress = fields.Integer(
        string='Progress',
    )
    log_filename = fields.Char(string="Name")
    log_binary = fields.Binary(string="Download File")
    state = fields.Selection(
        [('choose', 'Get'),
         ('download', 'Download')],
        default='choose',)

    @api.model
    def conexion(self, database=False):
        server = self.env.user.company_id.opus_server
        username = self.env.user.company_id.opus_username
        password = self.env.user.company_id.opus_password
        conn = False
        if server and username and password:
            try:
                conn = pymssql.connect(
                    server=server, user=username,
                    password=password, database=database)
            except:
                raise UserError(_('Opus Server Not Found'))
        return conn

    @api.model
    def get_projects(self):
        conn = self.conexion()
        selection_data = []
        if conn:
            cr = conn.cursor()
            cr.execute(
                "SELECT name FROM sys.databases WHERE database_id > 4")
            databases = cr.fetchall()
            for data in databases:
                selection_data.append((data[0], data[0]))
            conn.close()
        else:
            selection_data.append(('1', _('There are not results.')))
        return selection_data

    @api.model
    def validate_uom(self, cr):
        missing_uom = []
        cr.execute(
            str("""SELECT DISTINCT r.UnidadMedida FROM Recurso AS r
            INNER JOIN NaturalezaDeRecurso AS nr
                ON r.NaturalezaDeRecursoId = nr.NaturalezaDeRecursoId
            WHERE nr.Alias = 'Material'"""))
        uom_names = cr.fetchall()
        uom_obj = self.env['product.uom']
        length = 0
        for uom in uom_names:
            if length < len(uom[0]):
                length = len(uom[0])
        for uom in uom_names:
            if not uom_obj.search([('name', '=', uom[0])]):
                missing_uom.append(_('%s not exist' % uom[0].ljust(length+5)))
        return missing_uom

    @api.model
    def validate_products(self, cr):
        missing_products = []
        cr.execute(
            str("""SELECT Recurso.Clave FROM Recurso
            INNER JOIN NaturalezaDeRecurso
                ON Recurso.NaturalezaDeRecursoId = NaturalezaDeRecurso.NaturalezaDeRecursoId
            WHERE NaturalezaDeRecurso.Alias = 'Material'"""))
        products_codes = cr.fetchall()
        prod_obj = self.env['product.product']
        length = 0
        for code in products_codes:
            if length < len(code[0]):
                length = len(code[0])
        for code in products_codes:
            if not prod_obj.search([('default_code', '=', code[0])]):
                missing_products.append(_('%s not exist' % code[0].ljust(length+5)))
        return missing_products

    @api.model
    def validate_customers(self, cr):
        missing_customers = []
        cr.execute("SELECT ClienteId, Nombre FROM Cliente")
        customers = cr.fetchall()
        cust_obj = self.env['res.partner']
        length = 0
        for cust in customers:
            if length < len(cust[1]):
                length = len(cust[1])
        for customer in customers:
            if not cust_obj.search([('name', '=', customer[1])]):
                missing_customers.append(_('%s not exist' % customer[1].ljust(length+5)))
        return missing_customers

    @api.multi
    def validate_project(self):
        self.ensure_one()
        log_data = ""
        conn = self.conexion(self.project_ids)
        if conn:
            cr = conn.cursor()
            missing_uom = self.validate_uom(cr)
            if missing_uom:
                log_data += _("   Missing UoM \n" + ("-"*18) + "\n")
                for error in missing_uom:
                    log_data += (error + "\n")
            missing_products = self.validate_products(cr)
            if missing_products:
                log_data += _("   Missing Products \n" + ("-"*18) + "\n")
                for error in missing_products:
                    log_data += (error + "\n")
            missing_customers = self.validate_customers(cr)
            if missing_customers:
                log_data += _("   Missing Customers \n" + ("-"*18) + "\n")
                for error in missing_customers:
                    log_data += (error + "\n")
            if len(log_data) > 0:
                self.log_binary = base64.b64encode(log_data)
                self.log_filename = _("Project Errors") + '.txt'
                self.state = 'download'
                return {
                    'type': 'ir.actions.act_window',
                    'res_model': 'import.opus.wizard',
                    'view_mode': 'form',
                    'view_type': 'form',
                    'res_id': self.id,
                    'views': [(False, 'form')],
                    'target': 'new',
                }
