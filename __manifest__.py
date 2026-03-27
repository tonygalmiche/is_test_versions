{
    'name': 'InfoSaône - Module Odoo 18 pour ajouter le prénom dans le contact',
    'version': '18.0.0.0.1',
    'category': 'InfoSaône',
    'summary': 'Ajouter le prénom dans le contact',
    'description': """
InfoSaône - Module Odoo 18 pour ajouter le prénom dans le contact
===================================================
""",
    'website': 'http://www.infosaone.com',
    'depends': [
        'base',
    ],
    'data': [
        'views/res_partner_views.xml',
    ],
    'installable': True,
    'application': True,
    'author': 'Tony Galmiche / InfoSaône',
    'license': 'LGPL-3',
}
