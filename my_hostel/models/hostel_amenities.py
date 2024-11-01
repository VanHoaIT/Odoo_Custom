from odoo import fields, models
class HostelAmenities(models.Model):
    _name = "hostel.amenities"
    _description = "Hostel Amenities"
    
    name = fields.Char("Amenities", help="Provided Hostel Amenity")
    active = fields.Boolean("Active", help="Activate/Deactivate whether the amenity should be given or not")