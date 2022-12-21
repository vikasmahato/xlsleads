from __future__ import print_function

import traceback
from odoo import models, api
import pygsheets
import logging

_logger = logging.getLogger(__name__)


class OpsLeadSync(models.TransientModel):
    _name = 'cron.ops.lead.sync'

    def get_source_id_from_odoo(self, name):
        ids = self.env['utm.source'].search([('name', '=', name)], limit=1).id
        return ids

    @api.model
    def ops_lead_sync(self):
        keys_path = self.env['ir.config_parameter'].sudo().get_param('xlsleads.keys_path')
        spreadsheet_link = self.env['ir.config_parameter'].sudo().get_param('xlsleads.spreadsheet_link')
        default_ops_lead_qualifier = self.env['ir.config_parameter'].sudo().get_param('xlsleads.ops_lead_qualifier')
        client = pygsheets.authorize(service_account_file=keys_path)
        sheet1 = client.open_by_url(spreadsheet_link)
        worksheet = sheet1.sheet1
        cells = worksheet.get_all_records(empty_value='', head=1, majdim='ROWS')

        lead_qualifier = self.env["res.users"].search([('login', '=', default_ops_lead_qualifier)])

        end_row = len(cells)
        leads = [{
            'contact_name': lead['customer_name'],
            'partner_name': lead['customer_company'],
            'name': lead['customer_requirement'],
            'phone': lead['customer_number'],
            'lead_generator': lead['your_name'],
            'lead_qualifier': lead_qualifier.id if lead_qualifier else False,
            'lead_generator_number': lead['your_number'],
            'source_id': self.get_source_id_from_odoo('OPS')
        } for lead in cells]

        for lead in leads:
            try:
                self.env['crm.lead'].create(lead)
                worksheet.delete_rows(2, number=end_row)
            except:
                tb = traceback.format_exc()
                _logger.error(tb)
                pass


