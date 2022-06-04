# -*- coding: utf-8 -*-
{
    'name': "Consistencia de precios",

    'summary': """
        Consistencia de precios""",
    'description': """
    """,
    'author': "Ronny Montano <<rmontano1992@gmail.com>>",
    'category': 'Others',
    'version': '0.1',
    'depends': ['base', 'product', 'supi_integration'],

    # always loaded
    'data': [
        'views/price_consistence.xml',
        'security/ir.model.access.csv'
    ],
    'qweb': [
        # "static/src/xml/purchase_dashboard.xml",
        # "static/src/xml/purchase_toaster_button.xml",
    ],
}
