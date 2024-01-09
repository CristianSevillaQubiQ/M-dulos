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
    
    
    @api.model
    def create(self, vals):
        print("1")
        if vals.get('library_member') == True:
            print("2")
            if vals.get('member_ID', 'New') == 'New':
                print("3")
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
    