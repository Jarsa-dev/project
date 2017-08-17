# -*- coding: utf-8 -*-
# Copyright 2017, Jarsa Sistemas, S.A. de C.V.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from openerp import _, api, fields, models
from openerp.exceptions import UserError
from os import getenv
import pymssql


class ImportOpusWizard(models.TransientModel):
    _name = 'import.opus.wizard'

    project_ids = fields.Selection(
        string='Projects',
        selection="get_projects",)
    log_filename = fields.Char(string="Name")
    log_binary = fields.Binary(string="Download File")

    @api.model
    def conexion(self, database=False):
        server = self.env.user.company_id.server
        username = self.env.user.company_id.username
        password = self.env.user.company_id.password
        conn = False
        if server and username and password:
            try:
                conn = pymssql.connect(
                    server=server, user=username,
                    password=password, database=database)
            except:
                raise UserError('hola')
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
            selection_data.append(('1', 'There are not results.'))
        return selection_data
