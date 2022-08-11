# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    drive_link = fields.Char(string='drive_link', config_parameter='xls_leads.drive_link')
    keys_path = fields.Char(string='keys_path', config_parameter='xls_leads.keys_path')
