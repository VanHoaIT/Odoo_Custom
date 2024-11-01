/** @odoo-module */
import { Component } from "@odoo/owl";
import { registry } from "@web/core/registry";

export class AverageOrderValue extends Component {
    static props = {
        currentMonthSales: { type: Number, optional: false },
        previousMonthSales: { type: Number, optional: false },
        growthPercentage: { type: Number, optional: false },
    };
}

// Gán template cho component
AverageOrderValue.template = "sale_order_checkout.AverageOrderValue";
registry.category("components").add("sale_sub_dashboard_average_order_value", AverageOrderValue)