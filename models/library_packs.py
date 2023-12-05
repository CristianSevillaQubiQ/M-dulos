from odoo import api, fields, models

    
class book_pack(models.Model):
    _name = "library.book.pack"
    _description = "Model for creating packs of books"
    
    name = fields.Char()
    lines_ids = fields.One2many(comodel_name='library.book.component.line', inverse_name='pack_id')
    
    
class book_pack_line(models.Model):
    _name = 'library.book.component.line'
    _description = 'Model for creating a line for a pack'
    
    
    # Which model is related to this line
    pack_id = fields.Many2one(comodel_name='library.book.pack')
    
    quantity = fields.Integer()    
    component_id = fields.Many2one(comodel_name='library.book')
    