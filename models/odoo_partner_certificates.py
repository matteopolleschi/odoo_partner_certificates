# -*- coding: utf-8 -*-
from odoo import fields, models


class Odoo_partner_certificates(models.Model):
    _name = 'odoo_partner.certificates'
    _description = "Odoo partner certificates"

    name = fields.Char(string='Name Certificate')
    expiry_date = fields.Date(string='Expiry Date', default=fields.Date.today)
    issuer = fields.Many2one('res.partner', string='Issuer')
    attachment = fields.Binary(string='Attachments')
    #attachment_ids = fields.One2many( comodel_name='max.base.multi.attachment', inverse_name='owner_id', string='Attachments', domain=lambda self: [('owner_model', '=', self._name), ('owner_field', '=', 'attachment_ids')], copy=True)
    


class Odoo_inherit_partner(models.Model):
    _inherit = 'res.partner'

    certificate_ids = fields.Many2many('odoo_partner.certificates', string='Certificates')