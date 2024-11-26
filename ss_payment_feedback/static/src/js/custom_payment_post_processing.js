odoo.define('custom_module.PaymentPostProcessing', function (require) {
    'use strict';

    const PaymentPostProcessing = require('payment.post_processing');
    const core = require('web.core');
    const publicWidget = require('web.public.widget');

    const _t = core._t;

    // Extend the PaymentPostProcessing widget
    publicWidget.registry.PaymentPostProcessing = publicWidget.registry.PaymentPostProcessing.extend({
        /**
         * Override the poll method to include the feedback parameter.
         */
        poll: function () {
            const self = this;
            const feedback = $("#feedback").val(); // Get the feedback value from the DOM

            this._rpc({
                route: '/payment/status/poll',
                params: {
                    'csrf_token': core.csrf_token,
                    'feedback': feedback, // Include feedback in the payload
                }
            }).then(function (data) {
                if (data.success === true) {
                    self.processPolledData(data.display_values_list);
                } else {
                    switch (data.error) {
                        case "tx_process_retry":
                            break;
                        case "no_tx_found":
                            self.displayContent("payment.no_tx_found", {});
                            break;
                        default: // if an exception is raised
                            self.displayContent("payment.exception", {exception_msg: data.error});
                            break;
                    }
                }
                self.startPolling();

            }).guardedCatch(function () {
                self.displayContent("payment.rpc_error", {});
                self.startPolling();
            });
        },
    });

    return publicWidget.registry.PaymentPostProcessing;
});
