from odoo import fields, models, api
class HostelCategory(models.Model):
    _name = 'hostel.category'
    _description = 'category is about the relationship between parents and children'

    name = fields.Char('Category')
    parent_id = fields.Many2one('hostel.category', string='Parent Category', ondelete='restrict', index=True)
    parent_path = fields.Char(index=True)
    child_ids = fields.One2many('hostel.category', 'parent_id', string='Child Categories')

    _parent_store = True

    @api.constrains('parent_id')
    def _check_hierarchy(self):
        if not self._check_recursion():
            raise models.ValidationError('Error! You cannot create recursive categories.')