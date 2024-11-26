# -*- coding: utf-8 -*-
import logging

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)


class PaymentTransaction(models.Model):
    _inherit = 'payment.transaction'


    user_feedback = fields.Selection([
        ('bad', 'Bad'),
        ('satisfactory', 'Satisfactory'),
        ('good', 'Good'),
        ('excellent', 'Excellent'),
    ], string="User Feedback")