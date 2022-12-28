# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'
    token = fields.Char(string='Token', config_parameter='my_operator.token')
    authorization = fields.Char(string='Authorization', config_parameter='my_operator.authorization')
    youngman_india_myoperator_departments = fields.Char(string='My Operator Departments', config_parameter='my_operator.youngman_india_myoperator_departments')
    url = fields.Char(string='Url', config_parameter='my_operator.url')
    spreadsheet_link = fields.Char(string='Spreadsheet Link', config_parameter='xlsleads.spreadsheet_link')
    ops_lead_qualifier = fields.Char(string='Ops Lead Qualifier', config_parameter='xlsleads.ops_lead_qualifier')
    keys_path = fields.Char(string='Keys Path', config_parameter='xlsleads.keys_path')
    db = fields.Char(string='db', config_parameter='yimpl.db')
    username = fields.Char(string='username', config_parameter='yimpl.username')
    password = fields.Char(string='password', config_parameter='yimpl.password')
    passive_customer_endpoint = fields.Char(string='Passive customers Endpoint', config_parameter='passive.passive_customer_endpoint')

