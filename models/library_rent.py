from odoo import api, fields, models

class rent(models.Model):
    _name = 'library.rent'
    _description = 'Model for renting books.'
    
    
    user_id = fields.Many2one(comodel_name='res.partner', ondelete='restrict')
    book = fields.Many2one(comodel_name='library.book', ondelete='restrict')
    rent_date = fields.Datetime(default=fields.Datetime.now)
    devolution_date = fields.Datetime(default=fields.Datetime.now)
    state = fields.Selection(string="state",selection=[('pending','Pending'), ('returned','Returned')])
    
    