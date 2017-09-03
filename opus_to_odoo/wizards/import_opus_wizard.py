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
    log_filename = fields.Char(string="Name")
    log_binary = fields.Binary(string="Download File")
    state = fields.Selection(
        [('choose', 'Get'),
         ('error', 'Error'),
         ('import', 'Import')],
        default='choose',)
    partner_id = fields.Many2one(
        'res.partner',
    )
    parent_location_id = fields.Many2one(
        comodel_name='stock.location',
        string='Parent Location',
        domain=[('usage', '=', 'view')],)
    code = fields.Char()

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
        try:
            cr.execute(
                str("""SELECT DISTINCT r.UnidadMedida FROM Recurso AS r
                INNER JOIN NaturalezaDeRecurso AS nr
                    ON r.NaturalezaDeRecursoId = nr.NaturalezaDeRecursoId
                WHERE nr.Alias = 'Material'"""))
            uom_names = cr.fetchall()
            uom_obj = self.env['product.uom']
            for uom in uom_names:
                if not uom_obj.search([('name', '=', uom[0])]):
                    missing_uom.append(_('%s not exist' % uom[0].ljust(8)))
                    uom_obj.create({
                        'name': uom[0],
                        'category_id':
                        self.env.ref('product.uom_categ_wtime').id,
                        'factor': 20.0,
                        'factor_inv': 10.0,
                        'rounding': .01,
                        'uom_type': 'bigger', })
            return missing_uom
        except:
            raise UserError(
                _('There are a problem in the query, Please check your data.'))

    @api.model
    def validate_products(self, cr):
        missing_products = []
        cr.execute(
            str("""SELECT Recurso.Clave, Recurso.Descripcion FROM Recurso
            INNER JOIN NaturalezaDeRecurso
                ON Recurso.NaturalezaDeRecursoId =
                    NaturalezaDeRecurso.NaturalezaDeRecursoId
            WHERE NaturalezaDeRecurso.Alias = 'Material'"""))
        products_codes = cr.fetchall()
        prod_obj = self.env['product.product']
        length = 0
        for code in products_codes:
            if length < len(code[0]):
                length = len(code[0])
        for code in products_codes:
            if not prod_obj.search([('default_code', '=', code[0])]):
                prod_obj.create({'name': code[1]})
                missing_products.append(
                    _('%s not exist' % code[0].ljust(length + 5)))
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
            self.partner_id = cust_obj.search([('name', '=', customer[1])])
            if not self.partner_id:
                missing_customers.append(
                    _('%s not exist' % customer[1].ljust(length + 5)))
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
            self.state = 'import'
            conn.close()
            return {
                'type': 'ir.actions.act_window',
                'res_model': 'import.opus.wizard',
                'view_mode': 'form',
                'view_type': 'form',
                'res_id': self.id,
                'views': [(False, 'form')],
                'target': 'new',
            }
        else:
            self.state = 'import'

    @api.multi
    def create_project(self):
        project_obj = self.env['project.project']
        project_id = project_obj.create({
            'name': self.project_ids,
            'partner_id': self.env.ref('base.main_partner').id,
            'parent_location_id': self.parent_location_id.id,
            'code': self.code,
            # tener el parnet arriba
            # 'partner_id': self.partner_id.id,
            })
        return project_id

    @api.multi
    def create_edt(self, project_id, cr):
        cr.execute(
            "SELECT MAX(nivel) FROM RenglonDePresupuesto")
        level = cr.fetchall()
        cr.execute(str(
            """SELECT RenglonDePresupuestoId,RenglonPadreId,
            Descripcion,Nivel,PrecioUnitario,
            Cantidad,UnidadMedida,ClaveDeRenglon FROM
            RenglonDePresupuesto WHERE nivel != -1"""))
        edt_elements = cr.fetchall()
        obj_wbs_element = self.env['project.wbs_element']
        obj_wbs_concepts = self.env['project.task']
        obj_uom = self.env['product.uom']
        wbs_elements = {}
        parent = False
        count = 0
        for index in range(0, (level[0][0] + 1)):
            wbs_element_level = []
            for edt in edt_elements:
                if edt[3] == index:
                    wbs_element_level.append(edt)
            for element in wbs_element_level:
                if len(wbs_elements) > 0:
                    parent = wbs_elements[element[1]]
                if index == level[0][0]:
                    obj_wbs_concepts.create({
                        'name': element[7],
                        'description': element[2],
                        'project_id': project_id.id,
                        'wbs_element_id': wbs_elements[element[1]],
                        'unit_price': element[4],
                        'qty': element[5],
                        # Tener las unidades de medida arriba
                        # 'uom_id': obj_uom.search(
                        # [('name', '=', element[6])]).id,}
                        'uom_id': self.env.ref('product.product_uom_cm').id,
                        })
                else:
                    wbs_elements[element[0]] = obj_wbs_element.create({
                        'name': element[2],
                        'project_id': project_id.id,
                        'parent_id': parent,
                        'code': element[0],
                    }).id

    @api.multi
    def set_resources(self, project_id, cr):
        cr.execute(str(
            """SELECT ConceptoClave, ComponenteDescripcion,
            ComponenteUnidad, ComponenteCantidad, ComponenteCostoUnitario
            FROM View_Matrices vm
            INNER JOIN RenglonDePresupuesto rp
            ON vm.RenglonDePresupuestoId = rp.RenglonDePresupuestoId
            WHERE vm.ComponenteTipo = 'Material'"""))
        resources = cr.fetchall()
        obj_product = self.env['product.product']
        obj_uom = self.env['product.uom']
        for resource in resources:
            task = project_id.task_ids.search([('name', '=', resource[0])])
            product = obj_product.search(
                 ['|', ('default_code', '=', resource[0]),
                  ('name', '=ilike', resource[1])], limit=1).id
            task.resource_ids.create({
                'account_id': project_id.analytic_account_id.id,
                'product_id': product,
                'resource_type_id': self.env.ref(
                    'task_resource.insume_material').id,
                'uom_id': obj_uom.search([('name', '=', resource[2])]).id,
                # 'uom_id': self.env.ref('product.product_uom_cm').id,
                'qty': resource[3],
                'unit_price': resource[4],
                'task_id': task.id,
                })

    @api.multi
    def import_project(self):
        self.ensure_one()
        conn = self.conexion(self.project_ids)
        if conn:
            cr = conn.cursor()
            project_id = self.create_project()
            self.create_edt(project_id, cr)
            self.set_resources(project_id, cr)
        conn.close()
