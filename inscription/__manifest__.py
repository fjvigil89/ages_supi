# -*- coding: utf-8 -*-
{
    'name': "Employees Inscripntion",

    'summary': """
        Employees System Inscripntion""",

    'description': """
        Employees System Inscripntion
    """,

    'website': "",

    'category': 'HR',
    'version': '0.1',

    'depends': [
        'hr',
    ],

    'data': [
        'security/ir.model.access.csv',
        'views/inscription_menu.xml',
        'views/inscription.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
