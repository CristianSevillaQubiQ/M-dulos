from odoo import api, fields, models
from datetime import date

class rent(models.Model):
    _name = 'library.rent'
    _description = 'Model for renting books.'
    
    
    user_id = fields.Many2one(comodel_name='res.partner', ondelete='restrict')
    book = fields.Many2one(comodel_name='library.book', ondelete='restrict')
    rent_date = fields.Date(default=fields.Date.today)
    devolution_date = fields.Date(default=fields.Date.today)
    state = fields.Selection(string="state",selection=[('pending','Pending'), ('returned','Returned')])
    
    @api.model
    def renting_email(self, test):        
        for record in self.env['library.rent'].search([('state', "=", "pending"),("devolution_date", "<=", date.today())]):
            template_id = self.env.ref('doq_2.renting_email_template')
            template_id.send_mail(record.id, force_send=True)
            s
    
    
    
    