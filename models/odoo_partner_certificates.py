# -*- coding: utf-8 -*-
from odoo import fields, models


class Odoo_partner_certificates(models.Model):
    _name = 'odoo_partner.certificates'
    _description = "Odoo partner certificates"

    name = fields.Char(string='Name Certificate')
    expiry_date = fields.Date(string='Expiry Date', default=fields.Date.today)
    issuer = fields.Many2one('res.partner', string='Issuer')
    attachments = fields.Many2many(comodel_name='ir.attachment', relation='class_ir_attachments_rel', column1='class_id', column2='attachment_id', string='Attachments')
    expiry_date_reminder = fields.Boolean("Reminder")


class Odoo_inherit_partner(models.Model):
    _inherit = 'res.partner'

    certificate_ids = fields.Many2many('odoo_partner.certificates', string='Certificates')