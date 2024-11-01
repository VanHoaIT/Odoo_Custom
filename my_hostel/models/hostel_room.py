from odoo import fields, models, api
from odoo.exceptions import ValidationError
from datetime import timedelta
from odoo.exceptions import UserError
from odoo.tools.translate import _


class BaseArchive(models.AbstractModel):
    _name = 'base.archive'
    _description = 'Base Archive Model' 

    active = fields.Boolean(default=True)
    def do_archive(self):
        for record in self:
            record.active = not record.active

class HostelRoom(models.Model):
    _name = "hostel.room"
    _description = "room rates in currency"
    _inherit = ['base.archive']

    room_name = fields.Char(string="Room Name", required=True)
    room_no = fields.Integer(string="Room No.", required=True)
    floor_no = fields.Integer(string="Floor No.", help="number of floors of the room")    

    rent_amount = fields.Monetary('Rent Amount', help="Enter rent amount per month") 
    currency_id = fields.Many2one('res.currency', string="Currency")
    hostel_id = fields.Many2one('hostel.hostel', "hostel", help="Name of hostel")
    student_id = fields.One2many('hostel.student','room_id', string='Students', help='Enter students')
    hostel_amenities_ids = fields.Many2many("hostel.amenities", "hostel_room_amenities_rel", "room_id", "amenitiy_id", 
                                            string="Amenities", domain="[('active', '=', True)]", 
                                            help="Select hostel room amenities")
    member_ids = fields.One2many('hostel.room.member', 'hostel_room_id', string='Members')
    # rang buoc trong sql
    _sql_constraints = [("room_no_unique", "unique(room_no)", "Room number must be unique!")]

    student_per_room = fields.Integer("Student Per Room", required=True, help="Student allocated per room")
    availability = fields.Integer(compute="_compute_check_availability",store=True, string="Availability", help="Room availability in hostel")

    # constrains rang buoc, depent tinh toan
    @api.constrains('rent_amount') 
    def _check_rent_amout(self):
        """Constraint on negative rent amount"""
        if self.rent_amount < 0:
            raise ValidationError(("Rent Amout Per Month should not be negative value!"))
        
    @api.depends("student_per_room", "student_id")
    def _compute_check_availability(self):
        """Method to check room availability"""
        for rec in self:
            rec.availability = rec.student_per_room - len(rec.student_id.ids)

    @api.constrains('availability') 
    def _check_availability(self):
        """Constraint on negative rent amount"""
        if self.availability < 0:
            raise ValidationError(("room is full"))

    admission_date = fields.Date("Admission Date", help="Date of admission in hostel", default=fields.Datetime.today)
    discharge_date = fields.Date("Discharge Date", help="Date on which student discharge")
    duration = fields.Integer("Duration", store=True, compute="_compute_check_duration", inverse="_inverse_duration", help="Enter duration of living")

    @api.depends("admission_date", "discharge_date")
    def _compute_check_duration(self):
        """Method to check duration"""
        for rec in self:
            if rec.discharge_date and rec.admission_date:
                rec.duration = (rec.discharge_date - rec.admission_date).days
    def _inverse_duration(self):
        for stu in self:
            if stu.discharge_date and stu.admission_date:
                duration = (stu.discharge_date - stu.admission_date).days
                if duration != stu.duration:
                    stu.discharge_date = (stu.admission_date + timedelta(days=stu.duration)).strftime('%Y-%m-%d')

    state = fields.Selection([
        ('draft','Unavailable'),
        ('available','Available'),
        ('closed','Closed')
    ], 'State', default='draft')

    @api.model
    def is_allowed_transition(self, old_state, new_state):
        allowed = [('draft', 'available'),('available', 'closed'),('closed', 'draft')]
        return (old_state, new_state) in allowed
    def change_state(self, new_state):
        for room in self:
            if room.is_allowed_transition(room.state, new_state):
                room.state = new_state
            else:
                msg = _('Moving from %s to %s is not allowed')  % (room.state, new_state) 
                raise UserError(msg)
    def make_available(self):
        self.change_state('available')
    def make_closed(self):
        self.change_state('closed')

    # def post_to_webservice(self, data):
    #     try:
    #         req = requests.post('http://my-test-service.com', data=data, timeout=10)
    #         content = req.json()
    #     except IOError:
    #         error_msg = _("Something went wrong during data submission")
    #         raise UserError(error_msg)
    #     return content
	
    # hiện các member
    def log_all_room_members(self):
        # This is an empty recordset of model hostel.room.member
        hostel_room_obj = self.env['hostel.room.member']
        all_members = hostel_room_obj.search([])
        print("ALL MEMBERS:", all_members)
        return True

    def update_room_no(self):
        self.ensure_one()
        self.update({
            'state': 'draft'            
        })

    def find_room(self):
        domain = ['|',
                  '&', ('name', 'ilike', 'Room Name'), ('category_id.name', 'ilike', 'Category Name'),
                  '&', ('name', 'ilike', 'Second Room Name 2'),
                  ('category_id.name', 'ilike', 'SecondCategory Name 2')
                ]
        rooms = self.search(domain)
        print("Rooms Found:", rooms)
        return True
        
    # lọc các room có hơn 1 member
    def find_member(self):
        all_rooms = self.search([])
        filtered_rooms = self.rooms_with_multiple_members(all_rooms)
        print("Rooms:", filtered_rooms)
        return True

    @api.model
    def rooms_with_multiple_members(self, all_rooms):
        def predicate(room):
            if len(room.member_ids) > 1:
                return True
            return False
        return all_rooms.filtered(predicate)

    # lấy tên các member bằng cách map
    @api.model
    def get_members_names(self, rooms):
        return rooms.mapped('member_ids.name')
    
    # sắp xếp theo rating/ reverse=True sắp xếp ngược
    @api.model
    def sort_rooms_by_rating(self, rooms):
        return rooms.sorted(key='room_rating')
    
    remarks = fields.Text('Remarks')

    @api.model
    def create(self, vals_list):
        for vals in vals_list:
            if not self.user_has_groups('my_hostel.group_hostel_manager'):
                if vals.get('remarks'):
                    raise UserError('You are not allowed to modify ''remarks')
        return super(HostelRoom, self).create(vals_list)
    def write(self, vals):
        for record in vals:
            if not self.user_has_groups('my_hostel.group_hostel_manager'):
                if vals.get('remarks'):
                    raise UserError('You are not allowed to modify ''manager_remarks')
            return super(HostelRoom, self).write(vals)    
    
    # hiển thị tên phòng theo tùy chỉnh
    def name_get(self):
        result = []
        for room in self:
            member = room.member_ids.mapped('name')
            name = '%s (%s)' % (room.room_name, ', '.join(member))
            result.append((room.id, name))
        print(result)
        return result

    previous_room = fields.Many2one('hostel.room', string='Previous Room')
    
    # ghi đề phương thức search của Odoo
    @api.model
    def _name_search(self, name='', args=None, operator='ilike',
        limit=100, name_get_uid=None):
        args = [] if args is None else args.copy()
        if not(name == '' and operator == 'ilike'):
            args += ['|', '|',
                    ('name', operator, name),
                    ('isbn', operator, name),
                    ('author_ids.name', operator, name)]
        return super(HostelRoom, self)._name_search( name=name, args=args, operator=operator, 
                                                    limit=limit, name_get_uid=name_get_uid)
