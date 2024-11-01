/** @odoo-module **/

import { registry } from "@web/core/registry";
import { listView } from "@web/views/list/list_view";
import { ListRenderer } from "@web/views/list/list_renderer";
import { SaleDashboard } from "@sale_order_checkout/views/sale_dashboard";

export class SaleDashboardRenderer extends ListRenderer {};

SaleDashboardRenderer.template = 'sale_order_checkout.SaleListView';
SaleDashboardRenderer.components= Object.assign({}, ListRenderer.components, {SaleDashboard})

export const SaleDashboardListView = {
    ...listView,
    Renderer: SaleDashboardRenderer,
};

registry.category("views").add("sale_dashboard_list", SaleDashboardListView);
