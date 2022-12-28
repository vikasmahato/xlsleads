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

    def _get_default_country(self):
        country = self.env['res.country'].search([('code', '=', 'IN')], limit=1)
        return country.id

    def get_lead_qualifier_ids(self, passive_customer_lq_emails):
        team_id = self.env['crm.team'].search([('name', '=', 'LQ')]).id
        all_lqs =  self.env['crm.team.member'].search([('crm_team_id', '=', team_id)]).user_id.ids

        if passive_customer_lq_emails:
            emails = [email.strip() for email in passive_customer_lq_emails.split(",")]
            configured_users = self.env['res.users'].search([('login', 'in', emails)]).ids
            return list(set(all_lqs) & set(configured_users)) # take intersection of two lists
        else:
            return all_lqs


    @api.model
    def passive_lead_sync(self):
        passive_customer_endpoint = self.env['ir.config_parameter'].sudo().get_param('passive.passive_customer_endpoint')
        passive_customer_lq_emails= self.env['ir.config_parameter'].sudo().get_param('passive.passive_customer_lq_emails')

        if not passive_customer_endpoint:
            return

        response = requests.get(passive_customer_endpoint, verify=False)

        if response.ok:
            lead_qualifiers = self.get_lead_qualifier_ids(passive_customer_lq_emails)
            source_id = self.get_source_id_from_odoo()
            count_lq = len(lead_qualifiers)

            country_id = self._get_default_country()

            records = response.json()

            state_ids = {}

            for i in range(len(records)):
                existing_lead = self.env['crm.lead'].search([('remote_identifier', '=', records[i]['customer_masters_id']), ('source_id', '=', source_id), ('active', '=', True)], limit=1)

                state_id = None
                if records[i]['state_code'] in state_ids:
                    state_id = state_ids[records[i]['state_code']]
                else:
                    state = self.env['res.country.state'].search([('code', '=', records[i]['state_code']), ('country_id', '=', country_id)], limit=1)
                    state_ids[records[i]['state_code']] = state.id if state else False

                if not existing_lead:
                    lead = {
                        'name': 'PCL: ' + records[i]['company'],
                        'contact_name': records[i]['contact_name'],
                        'partner_name': records[i]['company'],
                        'phone': records[i]['phone_number'],
                        'lead_qualifier': lead_qualifiers[i % count_lq],
                        'source_id': source_id,
                        'email_from': records[i]['email'],
                        'description': "Last challn Recieving Date: " + records[i]['last_challan_recieving_date'],
                        'remote_identifier': records[i]['customer_masters_id'],
                        'state_id': state_id
                    }
                    self.env['crm.lead'].create([lead])
                    _logger.info("Create lead with remote_identifier {}, source_id {}.".format( records[i]['customer_masters_id'], source_id))





