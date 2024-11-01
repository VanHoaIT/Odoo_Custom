from odoo import fields, models, api
class Hostel(models.Model):
    _name = 'hostel.hostel'
    _description = "Information about hostel"
    _order = "id desc, name"
    _rec_name='hostel_code'

    name = fields.Char(string="Hostel Name", required=True)
    hostel_code = fields.Char(string="Code", required=True)
    street = fields.Char('Street')
    street2 = fields.Char('Street2')
    state_id = fields.Many2one("res.country.state", string="State")

    zip = fields.Char('Zip', change_default=True)
    city = fields.Char('City')
    country_id = fields.Many2one('res.country', string='Country')
    phone = fields.Char('Phone',required=True)
    mobile = fields.Char('Mobile',required=True)
    email = fields.Char('Email')

    hostel_floors = fields.Integer(string="Total Floors")
    image = fields.Binary('Hostel Image')
    active = fields.Boolean("Active", default=True, help="Activate/Deactivate hostel record")
    type = fields.Selection([("male", "Boys"), ("female", "Girls"), ("common", "Common")], "Type", 
                            help="Type of Hostel", required=True, default="common")
    other_info = fields.Text("Other Information", help="Enter more information")
    description = fields.Html('Description')
    hostel_rating = fields.Float('Hostel Average Rating', digits="Rating Value")

    category_id = fields.Many2one('hostel.category')
    display_name = fields.Char(compute='_compute_display_name')

    @api.depends('name', 'hostel_code')
    def _compute_display_name(self):
        for record in self:
            if record.hostel_code:
                record.display_name = f'{record.name} ({record.hostel_code})'
            else:
                record.display_name = record.name
        
    # ?? Adding dynamic relations using reference fields
    @api.model
    def _referencable_models(self):
        models = self.env['ir.model'].search([('field_id.name', '=', 'message_ids')])
        return [(x.model, x.name) for x in models]

    ref_doc_id = fields.Reference(selection='_referencable_models', string='Reference Document')
    