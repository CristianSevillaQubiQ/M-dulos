from odoo import api, fields, models

class audit(models.Model):
    _name = 'library.audit'
    _description = 'Model for auditing the library.'
    
    
    user_id = fields.Many2one(comodel_name='res.users', ondelete='restrict')
    
    operation = fields.Selection(selection=[('create', 'Create'), ('write', 'Write'), ('unlink', 'Unlink')])
    date = fields.Datetime(default=fields.Datetime.now)
    #book_id = fields.Char()
    res_id = fields.Integer()
    res_model = fields.Char()
