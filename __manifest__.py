{
    'name': 'Estate Management',
    'version': '1.0',
    'category': 'Real Estate',
    'author': 'Your Name',
    'website': 'https://yourwebsite.com',
    'summary': 'Manage properties in the estate module.',
    'depends': ['base'],
    'data': [
        'security/res_groups.xml',
        'security/ir.model.access.csv',
        'views/estate_property_type_tag.xml',
        'views/estate_property_type_view.xml',
        'views/estate_property_view.xml',
        'views/estate_property_offer_view.xml',
        'views/estate_menu.xml',
    ],
    'demo': [
        'demo/demo.xml',  # Add this line for demo data
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
