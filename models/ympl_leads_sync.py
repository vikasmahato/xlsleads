from __future__ import print_function

import traceback
import json
import xmlrpc.client
from odoo import fields, models, api
import requests
from datetime import date
import logging
from urllib.request import urlopen
import time
import base64

_logger = logging.getLogger(__name__)


class YmplLeadsSync(models.TransientModel):
    _name = 'cron.ympl.lead.sync'

    def get_source_id_from_odoo(self, name):
        ids = self.env['utm.source'].search([('name', '=', name)], limit=1).id
        return ids

    @api.model
    def yimpl_leads_sync(self):
        _logger.info("Starting YIMPL Leads Sync")
        url = 'https://ymipl.odoo.com'
        db = self.env['ir.config_parameter'].sudo().get_param('yimpl.db')
        username = self.env['ir.config_parameter'].sudo().get_param('yimpl.username')
        password = self.env['ir.config_parameter'].sudo().get_param('yimpl.password')

        common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))

        uid = common.authenticate(db, username, password, {})
        models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))

        ids = models.execute_kw(db, uid, password, 'crm.lead', 'search',
                                [[['type', '=', 'opportunity'], ['active', '=', False], ['lost_reason', '=', 9]]],
                                {'limit': 10})
        cells = models.execute_kw(db, uid, password, 'crm.lead', 'read', [ids],
                                  {'fields': ['contact_name', 'partner_name', 'name', 'mobile', 'tag_ids']})
        id1 = models.execute_kw(db, uid, password, 'crm.tag', 'search',
                                [[['name', '=', 'Transferred to BETA']]],
                                {'limit': 20})

        leads = [{
            'contact_name': lead['contact_name'],
            'partner_name': lead['partner_name'],
            'name': lead['name'],
            'phone': lead['mobile'],
            'source_id': self.get_source_id_from_odoo('YMIPL'),
            'remote_identifier': lead["id"],
            'description': lead["description"],
            'lead_generator': "Youngman Manufacturing"

        } for lead in cells if (lead['tag_ids'] != id1)]

        _logger.info("Recieved Records Count from YIMPL: " + str(len(leads)))

        for lead in leads:
            try:
                crm_lead = self.env["crm.lead"].search([('remote_identifier', '=', lead["remote_identifier"])])

                if not crm_lead:
                    self.env['crm.lead'].create(lead)
                    id1 = models.execute_kw(db, uid, password, 'crm.tag', 'search',
                                            [[['name', '=', 'Transferred to BETA']]],
                                            {'limit': 20})
                    models.execute_kw(db, uid, password, 'crm.lead', 'write', [ids, {'tag_ids': id1}])
                else:
                    _logger.info("Lead with remote_identifier " + lead["remote_identifier"] + " exists. Skipping")
            except:
                tb = traceback.format_exc()
                _logger.error(tb)
                pass
