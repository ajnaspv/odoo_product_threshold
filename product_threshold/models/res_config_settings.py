from odoo import api, fields, models, tools

class ResConfig(models.TransientModel):
    _inherit = 'res.config.settings'

    product_threshold = fields.Float(string="Threshold")