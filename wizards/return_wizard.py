from odoo import api, fields, models
from odoo.exceptions import AccessError, UserError, ValidationError

class return_book(models.TransientModel):
    _name = 'return.book'
    _description = 'Wizard for returning books.'
    
    user_id = fields.Many2one(comodel_name='res.partner', ondelete='restrict')
    book = fields.Many2one(comodel_name='library.book', ondelete='restrict')
    
    def return_book(self):
        record = self.env['library.rent'].search([('user_id', '=', self.user_id.id), ('state', '=', 'pending'), ('book', '=', self.book.id)])
        if( len(record) == 1 ):
            values = {
                'devolution_date' : fields.Datetime.now(),
                'state' : 'returned'
            }
            record.write(values) 
        else:
            raise UserError("The user has not rented this book.") 
        

    
        
        
        
