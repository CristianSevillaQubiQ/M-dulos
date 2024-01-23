# Copyright <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Library",
    "summary": "Librería en odoo",
    "version": "16.0.1.0.0",
    "category": "Library",
    "website": "https://www.qubiq.es",
    "author": "QubiQ",
    "license": "AGPL-3",
    "application": True,
    "installable": True,
    "depends": ['base', 'product', 'sale'],
    "data": [
        'wizards/finish_subscription.xml',
        'wizards/rent_book.xml',
        'wizards/return_wizard.xml',
        
        'data/mail_template.xml',
        #'data/ir_cron.xml',
        
        
        'views/book_library.xml',
        'views/audit_library.xml',
        'views/res_config_settings_views.xml',
        'views/rent_library.xml',
        'views/genres_library.xml',
        'views/res_partner.xml',
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/reports.xml',
        'views/report_library_book.xml',
        'views/report_sale.xml'],
}
