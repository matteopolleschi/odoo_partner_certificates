# -*- coding: utf-8 -*-
{
    'name': "Odoo partner certificates",

    'summary': """Odoo Partner Certificates Module""",

    'description': """
        This module upgrade the module res_partner by adding:
            - create a certificate (name, expiry date, issuer, reminder and attachments).
            - a partner can have multiple certificates.
            - a certificate contains multiple attachments.
            - when certificate is expired company receive a reminder mail.
            - When partner is created a user is created for it in quiz.
            - When partner is deleted the user is desactivated in quiz.
    """,

    'author': "Daphne Solutions",
    'website': "https://github.com/matteopolleschi/odoo_partner_certificates",

    'category': 'Hidden',
    'version': '3.0',
    'sequence': 2,

    'depends': ['base', 'contacts', 'partner_firstname'],
    'data': [
        'security/ir.model.access.csv',
        'views/odoo_partner_certificates_view.xml',
        'views/expiry_date_reminder_cron.xml',
        'views/base_config_api_view.xml',
        'data/expiry_date_reminder_action_data.xml',
        #'data/send_password_action_data.xml',
        'data/odoo_partner_certificates_template_data.xml'
    ],
    'demo': [],
    'installable': True,
    'auto_install': False,
}
