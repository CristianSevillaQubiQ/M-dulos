from odoo import api, fields, models
from odoo.exceptions import AccessError, UserError, ValidationError

class books(models.Model):
    _name = 'library.book'
    _inherits = {'product.template': 'product_tmpl_id'}
    _description = 'Model for registering books.'
    
    # delegation inheritance
    product_tmpl_id = fields.Many2one('product.template', string='Product Template', delegate=True, required=True, ondelete='cascade') #, ondelete='cascade'
    barcode = fields.Char()
    
    
    # Estos hay que dejarlos comentados dado que ya existen en el modelo que importamos (product.template)
    # Nombre del libro, caracteres
    # name = fields.Char(related='product_tmpl_id.name', string="Name", required=True, store=False)
    # Precio, numeros con decimales
    #list_price = fields.Float(string="Price")
    
    
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
    pack_type = fields.Selection(selection=[('colection', 'Colection'), ('series', 'Series')], default='colection') # COlecciones o sagas
    
    # sinopsis
    synopsis = fields.Html(string="Synopsis")
    line_ids = fields.One2many(comodel_name='library.book.component.line', inverse_name='component_id')
    
    
    
    @api.onchange("authors_ids")
    def change_genres(self):
        return {'domain': {'genres_ids': [('genres_ids','in',self.env['res.partner'].search([('name','=',self.authors_ids.name)]))]}}
    
    @api.onchange('authors_ids')
    def _onchange_genres_ids(self):
        self.genres_ids += self.authors_ids.genres_ids # Se añadirán los géneros del autor a los que ya tenga el libro
    
    @api.onchange('is_in_pack')
    def _onchange_is_in_pack(self):
        if self.is_in_pack == False:
            self.pack_type = "" # SI desmarco el check de que esta en un pack, el tipo de pack se vacia
            
    @api.constrains('list_price')
    def check_price(self):
        if self.list_price < 0:
            raise UserError("The price cannot be lower than 0.") 
    
    @api.model
    def create(self, values):
        res = super().create(values)
        vals_audit = {
            'user_id': self.env.user.id, # Modelo 'res.users' en el campo, se le introduce una ID de usuario.
            'operation': 'create',
            'date': fields.Datetime.now(),
            'book_id': res.name
            }
        
        self.env['library.audit'].create(vals_audit) 
        return res


    def unlink(self):
        for record in self:
            vals_audit = {
                'user_id': self.env.uid,
                'operation': 'unlink',
                'date': fields.Datetime.now(),
                'book_id': record.name
                }
            
            res = super(books, record).unlink() # solo devuelve true si puede eliminar, error si no
            self.env['library.audit'].create(vals_audit)
        return res
    
    def write(self, values):
        res = super().write(values)
        vals_audit = {
            'user_id': self.env.uid,
            'operation': 'write',
            'date': fields.Datetime.now(),
            'book_id': self.name
            }
        
        self.env['library.audit'].create(vals_audit)
        return res

    def name_get(self):
        res = []
        for book in self:
            res.append((book.id, '[%s] %s' % (book.barcode,book.name)))
        return res
    
    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
        args = args or []
        
        if name:
            records = self.search(['|',('name', operator, name), ('barcode', operator, name)])
            return records.name_get()
        
        return self.env['library.book'].search([('name', operator, name)]+args, limit=limit).name_get()
    