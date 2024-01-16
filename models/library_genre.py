from odoo import api, fields, models

class genre(models.Model):
    _name = 'library.genre'
    _description = 'Model for registering genres.'
    _inherit = ['library.audit.mixing']
    
    # Nombre del género literario, caracteres
    name = fields.Char(required=True)
    # Descripción del genero, caracteres
    description = fields.Char()
    