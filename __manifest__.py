# -*- coding: utf-8 -*-

{
    'name' : 'Lead Sources',
    'version' : '4.0.1',
    'category': 'Sales/CRM',
    'summary': 'Leads From Ops/Inbound/YMIPL',
    'description': """Generate Leads from different sources""",
    'author': "Ajay",
    'website': "https://www.youngman.co.in/",
    'sequence': -100,

    'depends': ['base', 'crm'],

    'data': [
        'data/cron.xml',
        'data/cron_op.xml',
        'views/views.xml',
        'views/crm_lead.xml'
    ],

    'application': True,
    'installable': True,
    'auto_install': False,
}
