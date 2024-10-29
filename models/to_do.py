from odoo import fields, models, api, _
from odoo.exceptions import ValidationError
from datetime import date

class TodoTask(models.Model):
    _name = 'todo.task'
    _description = "To-Do Tasks"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Task Name", required=True)
    partner_id = fields.Many2one('res.partner', string="Assign To")
    description = fields.Text(string="Description")
    due_date = fields.Date(string="Due Date")
    active = fields.Boolean(default=True)
    estimated_time = fields.Float(string="Estimated Time", required=True)  # الحقل المطلوب
    is_late = fields.Boolean(string="Is Late")

    timesheet_ids = fields.One2many('timesheet.lines', 'task_id')
    
    status = fields.Selection([
        ('new', 'New'),
        ('progress', 'In Progress'),
        ('completed', 'Completed'),
        ('closed', 'Closed'),
        ('draft', 'Draft'),
    ], default='new', string='Status', tracking=True)

    # Computed field to store the total time
    total_time = fields.Float(string="Total Time", compute="_compute_total_time", store=True)
    
    @api.depends('timesheet_ids.time')
    def _compute_total_time(self):
        for rec in self:
            total_time = sum(line.time for line in rec.timesheet_ids)
            if total_time > rec.estimated_time:
                raise ValidationError(_("Total time exceeds the estimated time for this task."))
            rec.total_time = total_time
    
   
    @api.model
    def mark_late_tasks(self):
        today = date.today()  # Get today's date
        # Get all tasks and mark them as late if their due_date is before today
        tasks = self.search([])
        for task in tasks:
            if task.due_date and task.due_date < today:
                task.is_late = True
            else:
                task.is_late = False
    # Action methods to update the status
    def action_start_progress(self):
        self.status = "progress"
      
    def action_mark_completed(self):
        self.status = "completed"
      
    def action_reset_to_new(self):
        self.status = "new"
        
    def action_reset_to_progress(self):   
        self.status = "progress"
    
    def action_to_closed(self):   
        for rec in self:
            rec.status = "closed"

    def action_to_draft(self):   
        for rec in self:
            rec.status = "draft"

class TimeSheet(models.Model):
    _name = 'timesheet.lines'
    _description = "Timesheet"
    
    task_id = fields.Many2one('todo.task', string="Task")
    start_date = fields.Date()
    des = fields.Text(string="Description")  # Corrected attribute for string
    time = fields.Float()
