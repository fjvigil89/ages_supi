# -*- coding: utf-8 -*-
{
    'name': "Supi Integration",

    'summary': """
        All needed models and functions to integrate Odoo with Supi Application""",

    'description': """
       
    """,

    'author': "Ronny Montano",
    'category': 'Others',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'product', 'muk_web_theme'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/res_users_view.xml',
        'views/res_partner_views.xml',
        'views/product_product_view.xml',
        'views/maestras_view.xml',
    ],
}
