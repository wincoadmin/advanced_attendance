// Copyright (c) 2024, Wins O. Win Nig Ltd and contributors
// For license information, please see license.txt

frappe.ui.form.on('Biometric Device Settings', {
	refresh: function(frm) {
		// Add Test Connection button
		if (!frm.is_new()) {
			frm.add_custom_button(__('Test Connection'), function() {
				if (!frm.doc.device_ip || !frm.doc.device_port) {
					frappe.msgprint(__('Please set Device IP and Device Port before testing.'));
					return;
				}
				
				frappe.call({
					method: 'advanced_attendance.zkteco_connector.test_device_connection',
					args: {
						device_ip: frm.doc.device_ip,
						device_port: frm.doc.device_port
					},
					freeze: true,
					freeze_message: __('Testing connection to device...'),
					callback: function(r) {
						if (r.message && r.message.success) {
							frappe.show_alert({
								message: r.message.message || __('Successfully connected to device.'),
								indicator: 'green'
							}, 5);
							
							// Show device info if available
							if (r.message.device_info) {
								let info = r.message.device_info;
								let msg = '<b>Device Information:</b><br>';
								if (info.model) msg += 'Model: ' + info.model + '<br>';
								if (info.firmware) msg += 'Firmware: ' + info.firmware + '<br>';
								if (info.serial_number) msg += 'Serial: ' + info.serial_number + '<br>';
								if (info.user_count !== undefined) msg += 'Users: ' + info.user_count + '<br>';
								if (info.log_count !== undefined) msg += 'Logs: ' + info.log_count;
								
								frappe.msgprint({
									title: __('Connection Successful'),
									message: msg,
									indicator: 'green'
								});
							}
						} else {
							let err = (r.message && (r.message.error || r.message.message)) || __('Connection failed.');
							frappe.show_alert({
								message: __('Connection failed: ') + err,
								indicator: 'red'
							}, 7);
						}
					},
					error: function(err) {
						frappe.show_alert({
							message: __('Connection test failed: ') + (err.message || ''),
							indicator: 'red'
						}, 7);
					}
				});
			}, __('Actions'));
		}
	}
});
