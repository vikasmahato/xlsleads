# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    speadsheet_link = fields.Char(string='Spreadsheet Link', config_parameter='xlsleads.speadsheet_link')
    keys_path = fields.Char(string='Keys Path', config_parameter='xlsleads.keys_path')
