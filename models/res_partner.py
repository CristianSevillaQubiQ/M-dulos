from odoo import api, fields, models
from odoo.exceptions import AccessError, UserError, ValidationError

class ResPartner(models.Model):
    #_name = 'res.partner'
    _inherit = 'res.partner'
    author_name = fields.Char()
    author_surname = fields.Char()
    book_author = fields.Boolean()
    library_member = fields.Boolean() 
    member_ID = fields.Char(copy=False, default='New', readonly=True)
    genres_ids = fields.Many2many(comodel_name='library.genre')
    
    rented_books_count = fields.Integer(compute='_compute_rented_books')
    sold_books_count = fields.Char(compute='_compute_sold_books', compute_sudo=True)
    not_rented_books = fields.Many2one(comodel_name='library.book', compute='_compute_author_not_rented_books')
    
    name = fields.Char(compute='_compute_name', inverse='_compute_first_second', store=True)
    first_name = fields.Char()
    second_name = fields.Char()
    
    def view_member_books(self):
        return {
            'type':'ir.actions.act_window',
            'name':'Member books',
            'res_model':'library.rent',
            'view_mode':'list',
            'view_type':'list',
            'domain':[('user_id', '=', self.id)],
        }
        
    def _compute_author_not_rented_books(self):
        for record in self:
            authors_total_book_list = self.env['library.book'].search([('authors_ids','=',record.id)]).mapped('id') # todos los libros del autor
            print(authors_total_book_list)
            
            rented_book_list = self.env['library.rent'].search([]).mapped('id') # todos los libros alquilados de todos los autores
            print(rented_book_list)
            
            not_rented = []
            for book in authors_total_book_list:
                if book not in rented_book_list:
                    not_rented.append(book)
            print(not_rented)
            
        self.not_rented_books = not_rented
        
        
        
    @api.onchange('first_name', 'second_name')
    def _compute_name(self):
        if (self.first_name) and (self.second_name):
            self.name = self.first_name + " " + self.second_name
        elif (self.first_name) and (not self.second_name):
            self.name = self.first_name
        elif (not self.first_name) and (self.second_name):
            self.name = self.second_name
        elif (not self.first_name) and (not self.second_name):
            self.name = ""
    
    @api.onchange('name')
    def _compute_first_second(self):
        if ((self.name != False)):
            arr = self.name.split(' ')
            if (len(arr)>1):
                self.first_name = arr[0]
                self.second_name = arr[1]
        
    def _compute_rented_books(self):
        for record in self:
            record.rented_books_count = self.env['library.rent'].search_count([('user_id','=',record.id)])
            
            
    def _compute_sold_books(self):
        for record in self:
            record.sold_books_count = "0 €" # todos los autores a cero o tendremos un error de valor no asignado
        authors = self.env['res.partner'].search([('book_author','=',True)])
        for author in authors:
            total_sold = 0
            books_ids = self.env['library.book'].search([('authors_ids','=',author.id)])
            for book in books_ids:
                sale_lines = self.env['sale.order.line'].search([('name', '=', book.name)])
                #total_sold += sum(line.price_total for line in sale_lines)
                total_sold += sum(sale_lines.mapped('price_total'))
            author.sold_books_count = str(total_sold) + " €"
        
    
            
    
    @api.model
    def create(self, vals):
        if vals.get('library_member') == True:
            if vals.get('member_ID', 'New') == 'New':
                vals['member_ID'] = self.env['ir.sequence'].next_by_code('member.lfpv') or 'New'

        res = super().create(vals)
        return res
    
    @api.onchange('author_name', 'author_surname')
    def _onchange_compute_fullname(self):
        if (self.author_name) and (self.author_surname):
            self.name = self.author_name + " " + self.author_surname
        elif (self.author_name) and (not self.author_surname):
            self.name = self.author_name
        elif (not self.author_name) and (self.author_surname):
            self.name = self.author_surname
        elif (not self.author_name) and (not self.author_surname):
            self.name = ""
            
    def launch_wizard(self):
        return {
            'type':'ir.actions.act_window',
            'name':'Member wizard',
            'res_model':'finish.subscription',
            'view_mode':'form',
            'view_type':'form',
            'target':'new',
        }
        
    def name_get(self):
        res = []
        for record in self:
            res.append((record.id, '[%s] %s' % (record.member_ID, record.name)))
        return res
  
    
    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
        args = args or []
        
        if name:
            records = self.search(['|',('name', operator, name), ('member_ID', operator, name)])
            return records.name_get()
        
        return self.env['res.partner'].search([('name', operator, name)]+args, limit=limit).name_get()
    

    


class SaleOrder(models.Model):
    _inherit = 'sale.order'
    
    def action_confirm(self):       
        if self.partner_id.library_member == True:
            res = super(SaleOrder, self).action_confirm()
            return res
        else:
            raise UserError("The user is not a library member") 
    