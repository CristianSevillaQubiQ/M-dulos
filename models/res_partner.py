from odoo import api, fields, models
from odoo.exceptions import AccessError, UserError, ValidationError

class ResPartner(models.Model):
    #_name = 'res.partner'
    _inherit = 'res.partner'

    author_name = fields.Char()
    author_surname = fields.Char()

    book_author = fields.Boolean()
    library_member = fields.Boolean() 
    member_ID = fields.Integer()
    
    genres_ids = fields.Many2many(comodel_name='library.genre')
    
    
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


class SaleOrder(models.Model):
    _inherit = 'sale.order'
    
    def action_confirm(self):       
        if self.partner_id.library_member == True:
            res = super(SaleOrder, self).action_confirm()
            return res
        else:
            raise UserError("The user is not a library member") 
    