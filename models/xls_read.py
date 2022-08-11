from __future__ import print_function
import traceback
from odoo import fields, models, api
import pygsheets

import logging

_logger = logging.getLogger(__name__)



class ReadXls(models.TransientModel):
    _name = 'cron.xls'

    @api.model
    def cron_test(self):
        print("checking")
        print("Executing")

        keys_path =self.env['ir.config_parameter'].sudo().get_param('xlsleads.keys_path')
        speadsheet_link = self.env['ir.config_parameter'].sudo().get_param('xlsleads.speadsheet_link')

        client = pygsheets.authorize(service_account_file=keys_path)
        sheet1 = client.open_by_url(speadsheet_link)
        worksheet = sheet1.sheet1
        cells = worksheet.get_all_records(empty_value='', head=1, majdim='ROWS')

        end_row = len(cells)
        leads = [{
            'contact_name': lead['customer_name'],
            'partner_name': lead['customer_company'],
            'name': lead['customer_requirement'],
            'phone': lead['customer_number'],
            'lead_qual': lead['your_name'],
            'lead_qual_num': lead['your_number']
        } for lead in cells]

        for lead in leads:
            try:
                self.env['crm.lead'].create(lead)
            except:
                tb =traceback.format_exc()
                _logger.error(tb)
                pass
        worksheet.delete_rows(2, number=end_row)

