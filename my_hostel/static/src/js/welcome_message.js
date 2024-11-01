/** @odoo-module **/

import { Component } from 'owl';

class WelcomeMessage extends Component {
    static template = 'my_module.WelcomeMessage';

    constructor() {
        super(...arguments);
        this.name = 'World'; // Trạng thái mặc định
    }

    changeName(newName) {
        this.name = newName;
        this.render(); // Cập nhật giao diện
    }
}

// Đăng ký component
const app = new WelcomeMessage();
app.mount(document.body);
