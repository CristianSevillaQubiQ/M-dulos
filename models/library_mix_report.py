from odoo import api, fields, models, tools


class LibraryMixReport(models.Model):
    _name = "library.mix.report"
    _description = 'Model for mix report, between books, times the book has been rented and the total each book has sold.'
    _auto = False
    
    
    book_id = fields.Many2one('library.book') # Nombre del libro (library.book)
    times_rented = fields.Integer() # numero de veces alquilado (count(library.rent))
    total_sold = fields.Float() # total en ventas (sum(purchase_order))
    
    
    def init(self):
        tools.drop_view_if_exists(self.env.cr, 'library_mix_report')
        self.env.cr.execute("""
            CREATE OR REPLACE VIEW library_mix_report AS (
                SELECT
                    min(lb.id) AS id,
                    lb.id AS book_id,
                    COUNT(lr.*) AS times_rented,
                    COALESCE(SUM(sol.price_total), 0) AS total_sold
                FROM
                    library_book lb
                LEFT JOIN
                    sale_order_line sol ON lb.product_tmpl_id=sol.product_id
                LEFT JOIN
                    library_rent lr ON lb.id=lr.book
                GROUP BY
                    lb.id			
            )
        """.format(self._table))

    
    
    