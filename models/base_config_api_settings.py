import logging
from odoo import api, fields, models
_logger = logging.getLogger(__name__)


class ResConfigApiSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    quiz_api_username = fields.Char(string='Username')
    quiz_api_password = fields.Char(string='Password')


    def set_values(self):
        super(ResConfigApiSettings, self).set_values()
        self.env['ir.config_parameter'].sudo().set_param('quiz_api_username', self.quiz_api_username)
        self.env['ir.config_parameter'].sudo().set_param('quiz_api_password', self.quiz_api_password)

    @api.model
    def get_values(self):
        res = super(ResConfigApiSettings, self).get_values()
        quiz_api_username = self.env['ir.config_parameter'].sudo().get_param('quiz_api_username', self.quiz_api_username)
        quiz_api_password = self.env['ir.config_parameter'].sudo().get_param('quiz_api_password', self.quiz_api_password)
        res.update(quiz_api_username=quiz_api_username, quiz_api_password=quiz_api_password)
        return res
