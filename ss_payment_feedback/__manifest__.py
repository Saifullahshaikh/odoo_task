# -*- coding: utf-8 -*-
{
    'name': 'Ss_payment_feedback',
    'version': '16.0.1.0.0',
    'summary': """ Ss_payment_feedback Summary """,
    'author': 'Saif',
    'website': '',
    'category': '',
    'depends': ['base', 'web','payment','website_sale'],
    'data': [
        'views/payment_template.xml',
        'views/payment_transaction_views.xml',
        
    ],'assets': {
              'web.assets_frontend': [
                  'ss_payment_feedback/static/src/js/custom_payment_post_processing.js'
              ],
          },
    'application': True,
    'installable': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
