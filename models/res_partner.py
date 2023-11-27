from odoo import api, fields, models

class ResPartner(models.Model):
    _inherit = 'res.partner'

    book_author = fields.Boolean()
    library_member = fields.Boolean()
    member_ID = fields.Integer()