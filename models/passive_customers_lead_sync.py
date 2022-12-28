from __future__ import print_function

import traceback
from odoo import models, api
import requests
import logging

_logger = logging.getLogger(__name__)


class PassiveLeadSync(models.TransientModel):
    _name = 'cron.passive.lead.sync'

    def get_source_id_from_odoo(self):
        ids = self.env['utm.source'].search([('name', '=', 'PASSIVE CUSTOMER LEAD')], limit=1)
        return ids.id if ids else False

    def get_lead_qualifier_ids(self):
        team_id = self.env['crm.team'].search([('name', '=', 'LQ')]).id
        return self.env['crm.team.member'].search([('crm_team_id', '=', team_id)]).user_id.ids

    @api.model
    def passive_lead_sync(self):
        passive_customer_endpoint = self.env['ir.config_parameter'].sudo().get_param('passive.passive_customer_endpoint')

        if not passive_customer_endpoint:
            return

        response = requests.get(passive_customer_endpoint, verify=False)

        if response.ok:
            lead_qualifiers = self.get_lead_qualifier_ids()
            source_id = self.get_source_id_from_odoo()
            leads = []

            count_lq = len(lead_qualifiers)

            records = response.json()

            for i in range(len(records)):
                existing_lead = self.env['crm.lead'].search([('remote_identifier', '=', records[i]['customer_masters_id']), ('source_id', '=', source_id), ('active', '=', True)], limit=1)
                if not existing_lead:
                    leads.append({
                        'name': 'PCL: ' + records[i]['company'],
                        'contact_name': records[i]['contact_name'],
                        'partner_name': records[i]['company'],
                        'phone': records[i]['phone_number'],
                        'lead_qualifier': lead_qualifiers[i % count_lq],
                        'source_id': source_id,
                        'description': "Last challn Recieving Date: " + records[i]['last_challan_recieving_date'] + " Contact person email is" + records[i]['email'],
                        'remote_identifier': records[i]['customer_masters_id']
                    })

            self.env['crm.lead'].create(leads)



