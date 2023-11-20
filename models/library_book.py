from odoo import fields, models

class books(models.Model):
    _name = 'library.book'
    _description = 'Model for registering books.'
    
    # Nombre del libro, caracteres
    name = fields.Char(string="Name", required=True)
    # Precio, numeros con decimales
    price = fields.Float(string="Price")
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

    
