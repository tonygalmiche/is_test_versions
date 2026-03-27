{
    'name': 'InfoSaône - Module Odoo 16 pour ajouter le prénom dans le contact',
    'version': '16.0.0.0.1',
    'category': 'InfoSaône',
    'summary': 'Ajouter le prénom dans le contact',
    'description': """
InfoSaône - Module Odoo 16 pour ajouter le prénom dans le contact
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
    'author': 'InfoSaône',
    'license': 'LGPL-3',
}
