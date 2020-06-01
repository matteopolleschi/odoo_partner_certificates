# -*- coding: utf-8 -*-
{
    'name': "Odoo partner certificates",

    'summary': """Odoo Partner Certificates Module""",

    'description': """
        This module upgrade the partner module by adding:
            - create an certificates
            - one partner have multiple certificates
    """,

    'author': "Mounir lahsini",
    'website': "https://github.com/matteopolleschi/odoo_partner_certificates",

    'category': 'Hidden',
    'version': '1.0',
    'sequence': 2,

    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/odoo_partner_certificates_view.xml',
        'views/expiry_date_reminder_cron.xml',
        'data/expiry_date_reminder_action_data.xml'
    ],
    'demo': [],
    'installable': True,
    'auto_install': False,
}