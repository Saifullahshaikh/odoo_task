# -*- coding: utf-8 -*-
import logging

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)


class ProjectTask(models.Model):
    _inherit = 'project.task'
    
    # user_ids = fields.Many2many(
    #     'res.users',
    #     relation='project_task_user_rel',
    #     column1='task_id',
    #     column2='user_id',
    #     string='Assignees',
    #     context={'active_test': False},  # Ensures inactive users are also visible if needed
    #     domain=[('share', '=', True)],  # Include portal users (users with 'share=True')
    #     tracking=True
    # )
