/** @odoo-module */
import { Component } from "@odoo/owl";
import { registry } from "@web/core/registry";

export class TotalSales extends Component {
    static props = {
        currentMonthSales: { type: Number, optional: false },
        previousMonthSales: { type: Number, optional: false },
        growthPercentage: { type: Number, optional: false },
    };
}

// Gán template cho component
TotalSales.template = "sale_order_checkout.TotalSales";
registry.category("components").add("sale_sub_dashboard_total", TotalSales)