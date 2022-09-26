# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'
    token = fields.Char(string='Token', config_parameter='my_operator.token')
    authorization = fields.Char(string='Authorization', config_parameter='my_operator.authorization')
    url = fields.Char(string='Url', config_parameter='my_operator.url')
    spreadsheet_link = fields.Char(string='Spreadsheet Link', config_parameter='xlsleads.spreadsheet_link')
    keys_path = fields.Char(string='Keys Path', config_parameter='xlsleads.keys_path')
    db = fields.Char(string='db', config_parameter='yimpl.db')
    username = fields.Char(string='username', config_parameter='yimpl.username')
    password = fields.Char(string='password', config_parameter='yimpl.password')
