from odoo import api, fields, models
from datetime import datetime, timedelta
from odoo.exceptions import AccessError, UserError, ValidationError

class rent_book(models.TransientModel):
    _name = 'rent.book'
    _description = 'Wizard for renting books.'
    
    
    date = datetime.now()
    max_dev_time = 21 #días
    def_dev_date = date + timedelta(days=max_dev_time) 
    
    
    user_id = fields.Many2one(comodel_name='res.partner', ondelete='restrict')
    book = fields.Many2one(comodel_name='library.book', ondelete='restrict')
    rent_date = fields.Datetime(default=date)
    devolution_date = fields.Datetime(default=def_dev_date)
    

    
    def create_rent(self):            
        print(self.user_id.id)
        print(self.book.id)
        if( len(self.env['library.rent'].search([('user_id', '=', self.user_id.id), ('state', '=', 'pending')])) < 2 ):
            
            if( (len(self.env['library.rent'].search([('user_id', '=', self.user_id.id), ('state', '=', 'pending'), ('book', '=', self.book.id)]))) >= 1):
                raise UserError("This book is already rented by de user.")
                
            
            values = {
            'user_id' : self.user_id.id,
            'book' : self.book.id,
            'rent_date' : self.rent_date,
            'devolution_date' : self.devolution_date,
            'state' : 'pending'
            }
        
            return self.env['library.rent'].create(values) # Guarda en el modelo rent los datos
        else:
            raise UserError("The user already has 2 books rented.") 
        
        
        
