from __future__ import print_function


import traceback


from odoo import fields, models, api
import pygsheets
import requests
from datetime import date
import logging
import json
from urllib.request import urlopen
import time
import base64

_logger = logging.getLogger(__name__)




class ReadXls(models.TransientModel):
    _name = 'cron.xls'

    def get_source_id_from_odoo(self, name):
        ids = self.env['utm.source'].search([('name', '=', name)], limit=1).id
        return ids

    @api.model
    def cron_test(self):
        print("checking")
        print("Executing")

        keys_path = self.env['ir.config_parameter'].sudo().get_param('xlsleads.keys_path')
        spreadsheet_link = self.env['ir.config_parameter'].sudo().get_param('xlsleads.spreadsheet_link')

        client = pygsheets.authorize(service_account_file=keys_path)
        sheet1 = client.open_by_url(spreadsheet_link)
        worksheet = sheet1.sheet1
        cells = worksheet.get_all_records(empty_value='', head=1, majdim='ROWS')

        end_row = len(cells)
        leads = [{
            'contact_name': lead['customer_name'],
            'partner_name': lead['customer_company'],
            'name': lead['customer_requirement'],
            'phone': lead['customer_number'],
            'lead_qual': lead['your_name'],
            'lead_qual_num': lead['your_number'],
            'source_id': self.get_source_id_from_odoo('OPS')
        } for lead in cells]

        for lead in leads:
            try:
                self.env['crm.lead'].create(lead)
            except:
                tb = traceback.format_exc()
                _logger.error(tb)
                pass
        # worksheet.delete_rows(2, number=end_row)

    def aud_link(self, file, name, id):
        if not file:
            return
        contents = urlopen(file).read()
        x = str(date.today()) + '_' + name
        attachment_id = self.env['ir.attachment'].create({
            'name': x,
            'datas': base64.b64encode(contents),
            'mimetype': 'audio/mpeg',
            'type': 'binary',
            'display_name': name,
            'id': id,
            'res_model': 'crm_lead'
        })
        return attachment_id

    def record_test(self, File):
        if (len(File) == 0):
            return
        Token = self.env['ir.config_parameter'].sudo().get_param('my_operator.token')
        authorization = self.env['ir.config_parameter'].sudo().get_param('my_operator.authorization')
        url = "https://developers.myoperator.co/recordings/link?token=" + str(Token) + "&file=" + str(File)

        payload = {}
        files = {}
        headers = {
            'Authorization': authorization,
            'Cookie': 'PHPSESSID=gpjd0bokagfusgitdec0fbjvk0; ci_session=a%3A5%3A%7Bs%3A10%3A%22session_id%22%3Bs%3A32%3A%22b6a7139f618b67a7cb93fdcd0ab6b93a%22%3Bs%3A10%3A%22ip_address%22%3Bs%3A9%3A%2210.0.1.81%22%3Bs%3A10%3A%22user_agent%22%3Bs%3A21%3A%22PostmanRuntime%2F7.29.2%22%3Bs%3A13%3A%22last_activity%22%3Bi%3A1662110545%3Bs%3A9%3A%22user_data%22%3Bs%3A0%3A%22%22%3B%7Dbc69296ae438df19d4c8f09cc437d2b1'
        }

        response = requests.request("GET", url, headers=headers, data=payload, files=files)
        json_data = json.loads(response.text)
        return json_data['url']

    @api.model
    def yml_test(self):
        print(1)
        x = int(time.time())
        url = self.env['ir.config_parameter'].sudo().get_param('my_operator.url')
        token = self.env['ir.config_parameter'].sudo().get_param('my_operator.token')
        authorization = self.env['ir.config_parameter'].sudo().get_param('my_operator.authorization')
        payload = {'token': token}
        files = [

        ]
        headers = {
            'Authorization': authorization,
            'Cookie': 'PHPSESSID=203s9hkjqhdr9tubpf0gsr6c17; ci_session=a%3A5%3A%7Bs%3A10%3A%22session_id%22%3Bs%3A32%3A%2277732330871d49b41b58bfad7085a580%22%3Bs%3A10%3A%22ip_address%22%3Bs%3A9%3A%2210.0.0.34%22%3Bs%3A10%3A%22user_agent%22%3Bs%3A21%3A%22PostmanRuntime%2F7.29.2%22%3Bs%3A13%3A%22last_activity%22%3Bi%3A1662099047%3Bs%3A9%3A%22user_data%22%3Bs%3A0%3A%22%22%3B%7D0b844e084787e76686beb44352352805'
        }

        response = requests.request("POST", url, headers=headers, data=payload, files=files)

        json_data = json.loads(response.text)
        if (len(json_data['data']['hits']) > 0):
            for lead in json_data['data']['hits']:
                if lead['_source']['department_name'] == 'Rent':
                    leads = [
                        dict(active=True, name='Inbound leads', contact_name=lead['_source']['caller_number_raw'],
                             phone=lead['_source']['caller_number'],
                             id=lead['_source']['additional_parameters'][0]['vl'],
                             lead_qual=lead['_source']['log_details'][0]['received_by'][0]['name'],
                             lead_qual_num=lead['_source']['log_details'][0]['received_by'][0][
                                 'contact_number_raw'],
                             source_id=self.get_source_id_from_odoo('INBOUND'),
                             audio_link=self.aud_link(self.record_test(lead['_source']['filename']),
                                                      lead['_source']['log_details'][0]['received_by'][0]['name'],
                                                      lead['_source']['additional_parameters'][0]['vl']))]

            for lead in leads:

                try:
                    self.env['crm.lead'].create(lead)
                except:
                    tb = traceback.format_exc()
                    _logger.error(tb)
                    pass
