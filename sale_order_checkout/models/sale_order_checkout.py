from odoo import models, fields, api
from odoo.tools import format_amount

from dateutil.relativedelta import relativedelta
from datetime import datetime

class SaleOrder(models.Model):
    _inherit = 'sale.order'
    
    check_out_date = fields.Datetime(
        string="Check-out Date",
        help="Order Completion Confirmation Date",
        default=fields.Datetime.now
    )

    @api.model
    def _remove_validity_date(self):
        if 'validity_date' in self._fields:
            del self._fields['validity_date']

    @api.model
    def get_date(self ,so, state, start_date=None, end_date=None):
        domain = [('state','in', state)]

        if start_date and end_date:
            domain += [
                ('date_order', '>=', start_date),
                ('date_order', '<=', end_date)
            ]
        return so.search(domain)

    # @api.model
    # def get_date_by_month(so, state, start_date, end_date):
    #     return so.search([
    #         ('state', 'in', state),
    #         ('date_order', '>=', start_date),
    #         ('date_order', '<=', end_date)
    #     ])

    @api.model
    def retrieve_dashboard(self):
        result = {
            'total_quotation': 0,
            'total_sale': 0,
            'number_sale': 0,
        }      

        so = self.env['sale.order']
        quotations = self.get_date(so, ['draft'])
        result['total_quotation'] = sum(quotations.mapped('amount_total'))

        sales = self.get_date(so, ['sale'])
        result['total_sale'] = sum(sales.mapped('amount_total'))
        result['number_sale'] = len(sales)

        currency = self.env.company.currency_id
        result['total_quotation'] = format_amount(self.env, result['total_quotation'], currency)
        result['total_sale'] = format_amount(self.env, result['total_sale'], currency)

        return result
    
    @api.model
    def calculate_growth(self, current, previous):
        if previous > 0:
            return round(((current - previous)/previous)*100,2)
        else:
            return 100 if current > 0 else 0

    @api.model
    def overview_dashboard(self, params):
        result = {
            'number_sale_current_month': 0,
            'number_sale_previous_month': 0,
            'growth_percentage_number_sale': 0,

            'total_sale_current_month': 0,
            'total_sale_previous_month': 0,
            'growth_percentage_total_sale': 0,

            'average_order_sale_current_month': 0,
            'average_order_sale_previous_month': 0,
            'growth_percentage_average_order_sale': 0,

            'total_order_current_month': 0,
            'total_order_previous_month': 0,
            'growth_percentage_total_order': 0,
        }      

        print("Received123 selected_month:", params)
        selected_month2=params

        today = datetime.today()
        start_current_month = today.replace(month=selected_month2 ,day=1)
        end_current_month = (start_current_month + relativedelta(months=1)) - relativedelta(days=1) 
        start_previous_month = start_current_month - relativedelta(months=1)
        end_previous_month = start_current_month - relativedelta(days=1)

        so = self.env['sale.order']

        sales_current_month = self.get_date(so, ['sale'], start_current_month, end_current_month)
        sales_previous_month = self.get_date(so, ['sale'], start_previous_month, end_previous_month)
        result['total_sale_current_month'] = sum(sales_current_month.mapped('amount_total'))
        result['total_sale_previous_month'] = sum(sales_previous_month.mapped('amount_total'))

        result['number_sale_current_month'] = len(sales_current_month)
        result['number_sale_previous_month'] = len(sales_previous_month)

        result['average_order_sale_current_month'] = (result['total_sale_current_month'] / result['number_sale_current_month']) if result['number_sale_current_month'] > 0 else 0
        result['average_order_sale_previous_month'] = (result['total_sale_previous_month'] / result['number_sale_previous_month']) if result['number_sale_previous_month'] > 0 else 0

        total_order_current_month = self.get_date(so, ['draft', 'sale', 'sent'], start_current_month, end_current_month)
        total_order_previous_month = self.get_date(so, ['draft', 'sale', 'sent'], start_previous_month, end_previous_month)
        result['total_order_current_month'] = len(total_order_current_month)
        result['total_order_previous_month'] = len(total_order_previous_month)

        # Tính % tăng trưởng
        result['growth_percentage_total_sale'] = self.calculate_growth(result['total_sale_current_month'], result['total_sale_previous_month'])
        result['growth_percentage_number_sale'] = self.calculate_growth(result['number_sale_current_month'], result['number_sale_previous_month'])
        result['growth_percentage_average_order_sale'] = self.calculate_growth(result['average_order_sale_current_month'], result['average_order_sale_previous_month'])
        result['growth_percentage_total_order'] = self.calculate_growth(result['total_order_current_month'], result['total_order_previous_month'])
        
        currency = self.env.company.currency_id
        result['total_sale_current_month'] = format_amount(self.env, result['total_sale_current_month'], currency)
        result['total_sale_previous_month'] = format_amount(self.env, result['total_sale_previous_month'], currency)
        result['average_order_sale_current_month'] = format_amount(self.env, result['average_order_sale_current_month'], currency)
        result['average_order_sale_previous_month'] = format_amount(self.env, result['average_order_sale_previous_month'], currency)

        return result
