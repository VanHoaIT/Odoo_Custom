/** @odoo-module */
import { ControlPanel } from "@web/search/control_panel/control_panel";
import { standardActionServiceProps } from "@web/webclient/actions/action_service";
import { useService } from "@web/core/utils/hooks";
import { Component, useState, onWillStart } from "@odoo/owl";
import { registry } from "@web/core/registry";

export class SpreadsheetDashboardAction extends Component {
    setup() {
        this.orm = useService('orm');
        this.action = useService('action');
        this.state = useState({
            selectedMonth: new Date().getMonth() + 1,
            activeDashboard: {},
            // months: Array.from({ length: 12 }, (_, i) => i + 1)
            months: [
                { value: 1, name: 'January' },
                { value: 2, name: 'February' },
                { value: 3, name: 'March' },
                { value: 4, name: 'April' },
                { value: 5, name: 'May' },
                { value: 6, name: 'June' },
                { value: 7, name: 'July' },
                { value: 8, name: 'August' },
                { value: 9, name: 'September' },
                { value: 10, name: 'October' },
                { value: 11, name: 'November' },
                { value: 12, name: 'December' }
            ],
        })    
        onWillStart(async () => {                  
            await this.loadDashboardData(parseInt(this.state.selectedMonth));
        });
    }
    async loadDashboardData(selectedMonth) {
        try {
            this.selectedMonth = selectedMonth  
            const result = await this.orm.call("sale.order", "overview_dashboard", [this.selectedMonth]);
            this.state.activeDashboard = result;
            console.log('state.activeDashboard: ', this.state.activeDashboard['average_order_sale_current_month'])
        } catch (error) {
            console.error("Error loading dashboard data:", error);
        }
    }

    onMonthChange(event) {
        const month = parseInt(event.target.value, 10);
        if (!isNaN(month)) {
            this.state.selectedMonth = month;
            this.loadDashboardData(this.state.selectedMonth);
        } else {
            console.error("Invalid month value selected:12324", event.target.value);
        }
    }
}

SpreadsheetDashboardAction.template = "sale_order_checkout.DashboardAction";
SpreadsheetDashboardAction.components = {
    ControlPanel
};
SpreadsheetDashboardAction.props = { ...standardActionServiceProps };

registry.category("actions").add("action_spreadsheet_dashboard_sale", SpreadsheetDashboardAction, { force: true });

