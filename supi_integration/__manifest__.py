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
    'depends': ['base'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
}
