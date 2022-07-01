# -*- coding: utf-8 -*-
{
    'name': "Supi Integration AGES",

    'summary': """
        All needed models and functions to integrate Odoo with Supi Application""",

    'description': """
       
    """,

    'author': "Ronny Montano <<rmontano1992@gmail.com>>",
    'category': 'Others',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'product', 'web', 'muk_web_theme', 'web_domain_field', 'odoo_rest_api'],

    # always loaded
    'data': [
        'views/res_users_view.xml',
        'wizard/wizard_gallery_picture.xml',
        'data/data_secuences.xml',
        # 'data/expresiones_validacion_variables.xml',
        'data/product_product_data.xml',
        'data/data_variable_present_times.xml',
        'data/product_product_muebles_data.xml',
        'views/res_partner_views.xml',
        'views/product_product_view.xml',
        'views/training_consult_view.xml',
        'views/supi_operations_view.xml',
        'views/variable_validations_view.xml',
        'views/maestras_view.xml',
        'wizard/import_planograma.xml',
        'security/ir.model.access.csv',
    ],
}
