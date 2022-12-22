# -*- coding: utf-8 -*-

from odoo import fields, models, _

import logging

from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class CrmLead(models.Model):
    _inherit = 'crm.lead'

    lead_generator = fields.Char(string="Lead Generator")
    lead_qualifier = fields.Many2one('res.users', string='Lead Qualifier', help="Select a user who will qualify this lead")
    lead_generator_number = fields.Char(string="Lead Generator Contact")
    audio_link = fields.Many2many('ir.attachment', string="Audio Link")
    remote_identifier = fields.Char(string="Remote Identifier")
