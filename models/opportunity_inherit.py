# -*- coding: utf-8 -*-

from odoo import fields, models, _

import logging

from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class CrmLead(models.Model):
    _inherit = 'crm.lead'

    lead_generator = fields.Char(string="Lead Generator")
    lead_qual = fields.Char(string="Lead Qualifier")
    lead_qual_num = fields.Char(string="LQ Number")

    audio_link = fields.Many2many('ir.attachment', string="Audio Link")

    # def write(self, vals):
    #     if self.team_id.user_id.id == self._uid:
    #         return super(CrmLead, self).write(vals)
    #
    #     if self.lead_qual:
    #         if (self._uid != self.user_id.id) and self.type == 'lead':
    #             raise ValidationError(_('You cant change Salesperson unless you are assigned to it!'))
    #         elif (self.lead_qual.lower() not in self.user_id.name.lower()) and self.type == 'lead':
    #             raise ValidationError(_('You cant change Salesperson unless you are assigned as LQ to it!'))
    #     return super(CrmLead, self).write(vals)

    # def write(self, vals):
    #     if self.lead_qual:
    #         if self._uid == self.user_id and (self.lead_qual.lower() in self.user_id.name.lower()):
    #             return super(CrmLead, self).write(vals)
    #         else:
    #             raise ValidationError(_('You cant change Salesperson unless you are assigned to it!'))
    #     else:
    #         if self._uid == self.user_id:
    #             return super(CrmLead, self).write(vals)
    #         else:
    #             raise ValidationError(_('You cant change Salesperson unless you are assigned to it!'))
