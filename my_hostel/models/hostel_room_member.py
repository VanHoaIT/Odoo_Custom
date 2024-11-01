from odoo import models, fields

class HostelRoomMember(models.Model):
    _name = 'hostel.room.member'
    _description = 'Hostel Room Member'

    name = fields.Char(string='Name', required=True)
    hostel_room_id = fields.Many2one('hostel.room', string='Hostel Room', ondelete='cascade')
