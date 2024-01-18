from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = ['res.config.settings']

    renting_days = fields.Integer(string='Renting days')
