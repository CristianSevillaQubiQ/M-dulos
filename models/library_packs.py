from odoo import api, fields, models

    
class book_pack_line(models.Model):
    _name = 'library.book.component.line'
    _description = 'Model for creating a line for a pack'
    
    
    quantity = fields.Integer()    
    component_ids = fields.Many2one(comodel_name='library.book')
    