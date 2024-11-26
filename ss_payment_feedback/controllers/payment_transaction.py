import urllib.parse
import werkzeug
import logging
from odoo import _, http
from odoo.exceptions import AccessError, UserError, ValidationError
from odoo.http import request

from odoo.addons.payment import utils as payment_utils
from odoo.addons.payment.controllers.post_processing import PaymentPostProcessing
# from odoo.addons.portal.controllers import portal
from odoo.addons.payment.controllers.portal import PaymentPortal
from odoo.addons.payment.controllers import portal as payment_portal

import json
import logging
from datetime import datetime
from werkzeug.exceptions import Forbidden, NotFound
from werkzeug.urls import url_decode, url_encode, url_parse

from odoo import fields, http, SUPERUSER_ID, tools, _
from odoo.fields import Command
from odoo.http import request
from odoo.addons.base.models.ir_qweb_fields import nl2br
from odoo.addons.http_routing.models.ir_http import slug
from odoo.addons.payment import utils as payment_utils
from odoo.addons.payment.controllers import portal as payment_portal
from odoo.addons.payment.controllers.post_processing import PaymentPostProcessing
from odoo.addons.website.controllers.main import QueryURL
from odoo.addons.website.models.ir_http import sitemap_qs2dom
from odoo.exceptions import AccessError, MissingError, ValidationError
from odoo.addons.portal.controllers.portal import _build_url_w_params
from odoo.addons.website.controllers import main
from odoo.addons.website.controllers.form import WebsiteForm
from odoo.addons.sale.controllers import portal
from odoo.osv import expression
from odoo.tools import lazy
from odoo.tools.json import scriptsafe as json_scriptsafe

_logger = logging.getLogger(__name__)

class PaymentPortal(payment_portal.PaymentPortal):
    @http.route(
        '/shop/payment/transaction/<int:order_id>', type='json', auth='public', website=True
    )
    def shop_payment_transaction(self, order_id, access_token, feedback=None, **kwargs):
        
        response = super(PaymentPortal, self).shop_payment_transaction(
            order_id, access_token, **kwargs
        )
        _logger.info(str(kwargs))

        # Add the feedback to the transaction if provided
        if feedback:
            last_tx_id = request.session.get('__website_sale_last_tx_id')
            if last_tx_id:
                tx_sudo = request.env['payment.transaction'].sudo().browse(last_tx_id)
                if tx_sudo.exists():
                    _logger.info("Updating transaction %s with feedback: %s", tx_sudo.id, feedback)
                    tx_sudo.write({'user_feedback': feedback})
        
        return response

    # @http.route('/payment/transaction', type='json', auth='public', website=True)
    # def payment_transaction(self, feedback=None, **kwargs):
    #     _logger.info("Overridden controller hit: feedback=%s, kwargs=%s", feedback, kwargs)
        
    #     tx_sudo = super().payment_transaction(**kwargs)
    #     if feedback:
    #         tx_sudo.sudo().write({'user_feedback': feedback})
    #     return tx_sudo


    # def _create_transaction(
    #     self, payment_option_id, reference_prefix, amount, currency_id, partner_id, flow,feedback,
    #     tokenization_requested, landing_route, is_validation=False,
    #     custom_create_values=None, **kwargs
    # ):
    #     res = super()._create_transaction(amount=amount, currency_id=currency_id, partner_id=partner_id, feedback=feedback, **kwargs)
        
    #     return res