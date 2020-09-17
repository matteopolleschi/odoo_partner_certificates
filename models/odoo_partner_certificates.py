# -*- coding: utf-8 -*-
from odoo import SUPERUSER_ID
from datetime import datetime, timedelta
from odoo import api, fields, models, exceptions, _
from odoo.http import request
import requests


class Odoo_partner_certificates(models.Model):
    _name = 'odoo_partner.certificates'
    _description = "Odoo partner certificates"

    name = fields.Char(string='Nome', required=True)
    template_id = fields.Many2one('odoo_partner.certificates.template', string='Tipo', required=True)
    issuer = fields.Many2one('res.partner', string='Emesso da')
    expiry_date = fields.Date(string='Scadenza')
    attachments = fields.Many2many(comodel_name='ir.attachment', relation='class_ir_attachments_rel', column1='class_id', column2='attachment_id', string='Documenti	')
    reminder = fields.Boolean(string="Notificato", default=False)
    partner_id = fields.Many2one('res.partner', ondelete='cascade', string="Partner")

    def get_quiz_token(self):
        url = "https://api.editricetoni.it/api/token/"
        payload = "{\"email\":\"school1@yopmail.com\",\"password\":\"school1\"}"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Token'
            }
        response = requests.request("POST", url, headers=headers, data=payload)
        token = response.json()
        if 'access' in token.keys():
            result = token['access']
        else : result = False
        return result

    @api.model
    def create(self, vals):
        certificate = super(Odoo_partner_certificates, self).create(vals)
        partner = self.env['res.partner'].search([('id', '=', certificate.partner_id.id )])
        if certificate.expiry_date == False and partner.quiz_api_id == 0:
            token = self.get_quiz_token()
            if token != False :
                url = "https://api.editricetoni.it/user/"
                #payload = '{ \"email\": \"'+partner.email+'\",\"password\":\"admin\",\"first_name\":\"'+partner.firstname+'\",\"last_name\":\"'+partner.lastname+'\",\"username\":\"'+partner.email+'\", \"odoo_id\": '+str(partner.id)+', \"parent\": 2, \"quiz_type\": 2}'
                payload = '{ \"email\": \"'+partner.email+'\",\"password\":\"admin\",\"first_name\":\"'+partner.firstname+'\",\"last_name\":\"'+partner.lastname+'\",\"username\":\"'+partner.email+'\", \"parent\": 2, \"quiz_type\": 2}'
                headers = {
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer ' + token
                }
                response = requests.request("POST", url, headers=headers, data=payload)
                quiz = response.json()
                if 'id' in quiz.keys(): 
                    partner.write({'quiz_api_id': quiz['id']})
                # For Testing
                self.env['res.partner'].create({'name': 'Create user 123', 'comment': response.json()})
        return certificate

    def write(self, vals):
        certificate = super(Odoo_partner_certificates, self).write(vals)
        return certificate

    @api.onchange('template_id')
    def onchange_template_id(self):
        if self.template_id:
            self.name = self.template_id.name


class Odoo_partner_certificates_template(models.Model):
    _name = "odoo_partner.certificates.template"
    _description = "Odoo partner certificates Template"

    name = fields.Char(string='Nome', required=True)
    description = fields.Text(string="Description")


class Odoo_inherit_partner(models.Model):
    _inherit = 'res.partner'

    certificate_ids = fields.One2many('odoo_partner.certificates', 'partner_id', string='Scadenze')
    quiz_api_id = fields.Integer(string='Quiz api id')

    @api.model
    def _cron_expiry_date_reminder(self):
        su_id =self.env['res.partner'].browse(SUPERUSER_ID)
        today_date = datetime.now().date()
        for partner in self.search([]):
            if partner.certificate_ids:
                for certificate in partner.certificate_ids:
                    if certificate.expiry_date == today_date and certificate.reminder == False:
                        template_id = self.env['ir.model.data'].get_object_reference('odoo_partner_certificates', 'email_template_edi_expiry_date_reminder')[1]
                        email_template_obj = self.env['mail.template'].browse(template_id)
                        if template_id:
                            if partner.parent_id.email:
                                recepient_email = partner.parent_id.email
                            else : recepient_email = partner.email
                            values = email_template_obj.generate_email(partner.id, fields=None)
                            values['email_from'] = su_id.email
                            values['email_to'] = recepient_email 
                            values['res_id'] = False
                            values['author_id'] = self.env['res.users'].browse(request.env.uid).partner_id.id
                            mail_mail_obj = self.env['mail.mail']
                            msg_id = mail_mail_obj.sudo().create(values)
                            if msg_id:
                                mail_mail_obj.sudo().send([msg_id])
                        certificate.reminder = True

        return True

    #def get_quiz_token(self):
    #    url = "https://api.editricetoni.it/api/token/"
    #    payload = "{\"email\":\"school1@yopmail.com\",\"password\":\"school1\"}"
    #    headers = {
    #        'Content-Type': 'application/json',
    #        'Authorization': 'Token'
    #        }
    #    response = requests.request("POST", url, headers=headers, data=payload)
    #    token = response.json()
    #    if 'access' in token.keys():
    #        result = token['access']
    #    else : result = False
    #    return result

    #@api.multi
    #def unlink(self):
    #    partner = super(Odoo_inherit_partner, self).unlink()
    #    token = self.get_quiz_token()
    #    if token != False :
    #       url = "https://api.editricetoni.it/user/deactivate/"+id+"/"
    #       payload = "{\"email\":\"school1@yopmail.com\",\"password\":\"school1\"}"
    #       headers= {}
    #       response = requests.request("POST", url, headers=headers, data = payload)
    #       print(response.text.encode('utf8'))
    #    return partner