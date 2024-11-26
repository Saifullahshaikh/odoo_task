from odoo import http
from odoo.http import request
from odoo.osv import expression
from collections import defaultdict
from datetime import datetime

from odoo.addons.project.controllers.portal import CustomerPortal

class ProjectCustomerPortal(CustomerPortal):
    

    # @http.route('/my/task/<int:task_id>/add_timesheet', type='http', auth="user", methods=['POST'], website=True)
    # def portal_add_timesheet(self, task_id, description, date, unit_amount, **kwargs):
    #     # Ensure the task exists and the user has access
    #     Task = request.env['project.task'].sudo().browse(task_id)
    #     if not Task.exists():
    #         return request.not_found()

    #     # Create the timesheet
    #     request.env['account.analytic.line'].sudo().create({
    #         'task_id': Task.id,
    #         'project_id': Task.project_id.id,
    #         'name': description,
    #         'date': date,
    #         'unit_amount': float(unit_amount),
    #         'user_id': request.env.user.id,
    #         'employee_id': request.env.user.employee_id.id if request.env.user.employee_id else False,
    #     })

    #     # Redirect back to the task page
    #     return request.redirect('/my/task/%d' % task_id)
    @http.route('/my/task/<int:task_id>/add_timesheet', type='http', auth="user", methods=['POST'], website=True)
    def portal_add_timesheet(self, task_id, description, date, unit_amount, **kwargs):
        # Ensure the task exists and the user has access
        Task = request.env['project.task'].sudo().browse(task_id)
        if not Task.exists():
            return request.not_found()
        
        error_message = None
        if not description:
            error_message = "Please provide a description for the timesheet."
        elif not date:
            error_message = "Please select a valid date."
        elif not unit_amount:
            error_message = "Please specify the time spent (HH:MM)."

        # If validation fails, redirect back with an error message
        if error_message:
            request.session['portal_error'] = error_message
            return request.redirect('/my/task/%d' % task_id)


        # Create the timesheet
        request.env['account.analytic.line'].sudo().create({
            'task_id': Task.id,
            'project_id': Task.project_id.id,
            'name': description,
            'date': date,
            'unit_amount': float(unit_amount),
            'user_id': request.env.user.id,
            'employee_id': request.env.user.employee_id.id if request.env.user.employee_id else False,
        })

        # Redirect back to the task page after submission
        return request.redirect('/my/task/%d' % task_id)


    def _task_get_page_view_values(self, task, access_token, **kwargs):
        values = super(ProjectCustomerPortal, self)._task_get_page_view_values(task, access_token, **kwargs)
        domain = request.env['account.analytic.line']._timesheet_get_portal_domain()
        task_domain = expression.AND([domain, [('task_id', '=', task.id)]])
        subtask_domain = expression.AND([domain, [('task_id', 'in', task.child_ids.ids)]])
        timesheets = request.env['account.analytic.line'].sudo().search(task_domain)
        subtasks_timesheets = request.env['account.analytic.line'].sudo().search(subtask_domain)
        timesheets_by_subtask = defaultdict(lambda: request.env['account.analytic.line'].sudo())
        for timesheet in subtasks_timesheets:
            timesheets_by_subtask[timesheet.task_id] |= timesheet
        values['allow_timesheets'] = task.allow_timesheets
        values['timesheets'] = timesheets
        values['timesheets_by_subtask'] = timesheets_by_subtask
        values['is_uom_day'] = request.env['account.analytic.line']._is_timesheet_encode_uom_day()
        values['task_id'] = task.id  # Pass task ID for the form
        return values
