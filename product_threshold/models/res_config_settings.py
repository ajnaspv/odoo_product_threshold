from odoo import api, fields, models, tools

class ResConfig(models.TransientModel):
    _inherit = 'res.config.settings'

    threshold = fields.Float(string="Threshold", config_parameter='product_threshold.threshold')