from odoo import api, fields, models

class books(models.Model):
    _name = 'library.book'
    _inherits = {'product.template': 'product_tmpl_id'}
    _description = 'Model for registering books.'
    
    # delegation inheritance
    product_tmpl_id = fields.Many2one('product.template', string='Product Template', required=True, ondelete='cascade') #, ondelete='cascade'
    
    
    # Estos hay que dejarlos comentados dado que ya existen en el modelo que importamos (product.template)
    # Nombre del libro, caracteres
    #name = fields.Char(related='product_tmpl_id.name', string="Name", required=True, store=False)
    # Precio, numeros con decimales
    # price = fields.Float(string="Price")
    
    
    # Edición, numeros enteros
    edition = fields.Integer(string="Edition")
    # Impreso o digital, selector
    book_type = fields.Selection(string="Book type",selection=[('printed','Printed'), ('digital','Digital')])
    # Enlace web de compra, caracteres
    buy_link = fields.Char(string="Purchase link")
    # Se ha comprado, booleano
    sold = fields.Boolean(string="Sold")
    # Fecha de compra, Fecha y hora
    date = fields.Datetime(string="Date")


    # author/s
    authors_ids = fields.Many2one(comodel_name='res.partner')
    # genres
    genres_ids = fields.Many2many(comodel_name='library.genre')
    # pack
    is_in_pack = fields.Boolean()
    
    line_ids = fields.One2many(comodel_name='library.book.component.line', inverse_name='component_id')
    
    

    
    
