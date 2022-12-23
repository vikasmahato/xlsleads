# -*- coding: utf-8 -*-

from odoo import api, fields, models, _

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
    user_id = fields.Many2one(comodel_name='res.users', string='Salesperson', store=True)
    partner_id = fields.Many2one(comodel_name='res.partner', string='Customer', domain=[('is_company','=', True), ('is_customer_branch', '=', False)], store=True)

    @api.onchange('partner_id')
    def onchange_partner_id(self):
        if self.partner_id and self.partner_id.user_id:
            return {'domain': {'user_id': [('id', '=', self.partner_id.user_id.id)]}}
        else:
            acc_m_team_id = self.env['crm.team'].search([('name', 'ilike', 'INSIDE SALES')]).id
            domain = self.env['crm.team.member'].search([('crm_team_id', '=', acc_m_team_id)]).user_id.ids
            return {'domain': {'user_id': [('id', 'in', domain)]}}


