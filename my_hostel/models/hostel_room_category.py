from odoo import models, fields
from datetime import timedelta

class RoomCategory(models.Model):
    _name = 'hostel.room.category'
    _description = 'Hostel Room Category'

    name = fields.Char('Category')
    description = fields.Text('Description')

    parent_id = fields.Many2one('hostel.room.category', string='Parent Category', ondelete='restrict',index=True)
    child_ids = fields.One2many('hostel.room.category', 'parent_id', string='Child Categories')


    def create_categories(self):
        categ1 = {
            'name': 'Child category 1',
            'description': 'Description for child 1'
        }
        categ2 = {
            'name': 'Child category 2',
            'description': 'Description for child 2'
        }
        parent_category_val = {
            'name': 'Parent category',
            'description': 'Description for parent category',
            'child_ids': [
                (0, 0, categ1),
                (0, 0, categ2),
            ]
        }
        self.env['hostel.room.category'].create(parent_category_val)
        return True

