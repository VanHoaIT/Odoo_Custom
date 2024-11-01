from odoo import models, fields
from datetime import timedelta
import logging
_logger = logging.getLogger(__name__)

class HostelRoom(models.Model):
    _inherit = 'hostel.room'
    date_terminate = fields.Date('Date of Termination')
    category_id = fields.Many2one('hostel.room.category', string="Room Category")

    def make_closed(self):
        day_to_allocate = self.category_id.max_allow_days or 10
        self.date_terminate = fields.Date.today() + timedelta(days=day_to_allocate)
        _logger.info(f"Room {self.room_name} closed, return date set to {self.date_terminate}")
        return super(HostelRoom, self).make_closed()
    
    def make_available(self):
        self.date_terminate = False
        _logger.info(f"Room {self.room_name} is now available, termination date reset.")
        return super(HostelRoom, self).make_available()