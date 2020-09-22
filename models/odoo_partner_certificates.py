# -*- coding: utf-8 -*-
from odoo import SUPERUSER_ID
from datetime import datetime, timedelta
from odoo import api, fields, models, exceptions, _
from odoo.http import request
import requests
import random
import string


class Odoo_partner_certificates(models.Model):
    _name = 'odoo_partner.certificates'
    _description = "Odoo partner certificates"

    name = fields.Char(string='Nome', required=True)
    template_id = fields.Many2one('odoo_partner.certificates.template', string='Tipo', required=True)
    issuer = fields.Many2one('res.partner', string='Emesso da')
    expiry_date = fields.Date(string='Scadenza')
    attachments = fields.Many2many(comodel_name='ir.attachment', relation='class_ir_attachments_rel_certificate', column1='class_id', column2='attachment_id', string='Documenti	')
    reminder = fields.Boolean(string="Notificato", default=False)
    partner_id = fields.Many2one('res.partner', ondelete='cascade', string="Partner")

    def get_password():
        password_chars = string.ascii_letters + string.digits
        result = ''.join((random.choice(password_chars) for i in range(9)))
        return result
    
    def send_password(self, password):
        template_id = self.env['ir.model.data'].get_object_reference('odoo_partner_certificates', 'email_template_edi_send_password')[1]
        email_template_obj = self.env['mail.template'].browse(template_id)
        if template_id:
            if parent_id.email:
                values = email_template_obj.generate_email(partner_id.id, fields=None)
                values['email_from'] = su_id.email
                values['email_to'] = parent_id.email
                values['res_id'] = False
                values['author_id'] = self.env['res.users'].browse(request.env.uid).partner_id.id
                mail_mail_obj = self.env['mail.mail']
                msg_id = mail_mail_obj.sudo().create(values)
                if msg_id:
                    mail_mail_obj.sudo().send([msg_id])
        return True
    
    def get_username(self, firstname, lastname):
        username = firstname +'.'+ lastname +'.'
        code = ''.join(random.choice(string.digits) for i in range(4))
        result = username + str(code)
        return result

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
        parent_id = self.env.user.company_id.partner_id.quiz_api_id
        # Generate Username
        #quiz_username = self.get_username(partner.firstname, partner.lastname)
        # Generate Password
        #quiz_password = self.get_password()
        quiz_password = 'admin'
        if certificate.expiry_date == False and partner.quiz_api_id == 0:
            token = self.get_quiz_token()
            if token != False :
                url = "https://api.editricetoni.it/user/"
                payload = '{ \"email\": \"'+partner.email+'\",\"password\":\"'+quiz_password+'\",\"first_name\":\"'+partner.firstname+'\",\"last_name\":\"'+partner.lastname+'\",\"username\":\"'+partner.email+'\", \"odoo_id\": '+str(partner.id)+', \"parent\": '+str(parent_id)+', \"quiz_type\": 2}'
                headers = {
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer ' + token
                }
                response = requests.request("POST", url, headers=headers, data=payload)
                quiz = response.json()
                if 'id' in quiz.keys(): 
                    partner.write({'quiz_api_id': quiz['id']})
                # Send login detail via email
                #self.send_password(quiz_password)
        return certificate

    def write(self, vals):
        # if certificate is updated and the expiry_date field is removed or added.
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

    @api.multi
    def unlink(self):
        for record in self:
            quiz_id = record.quiz_api_id
            if quiz_id != 0:
                token = record.get_quiz_token()
                if token != False :
                    url = "https://api.editricetoni.it/user/deactivate/"+str(quiz_id)+"/"
                    payload = "{\"email\":\"school1@yopmail.com\",\"password\":\"school1\"}"
                    headers = {
                        'Content-Type': 'application/json',
                        'Authorization': 'Bearer ' + token
                    }
                    response = requests.request("POST", url, headers=headers, data=payload)
        partner = super(Odoo_inherit_partner, self).unlink()
        return partner

    def write(self, vals):
        # if partner is updated and the quiz_api_id field is defined.
        partner = super(Odoo_inherit_partner, self).write(vals)
        return partner
