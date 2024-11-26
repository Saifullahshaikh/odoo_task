# -*- coding: utf-8 -*-
{
    'name': 'Ss_portal_user_timesheet',
    'version': '16.0.1.0.0',
    'summary': """ Ss_portal_user_timesheet Summary """,
    'author': 'Saif',
    'website': '',
    'category': '',
    'depends': ['base', 'project','hr_timesheet', 'hr'],
    "data": [
        "views/project_task_views.xml",
        "views/portal_task_view_inherit.xml",
        "views/employee_view_inherit.xml",
    ],'assets': {
            #   'web.assets_backend': [
            #       'ss_portal_user_timesheet/static/src/**/*'
            #   ],
          },
    'application': True,
    'installable': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
