# Copyright (c) 2024, Wins O. Win Nig Ltd and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class BiometricDeviceSettings(Document):
	pass

@frappe.whitelist()
def get_dashboard_data(data):
	"""Add custom buttons to the form"""
	return {
		'fieldname': 'device_name',
		'transactions': [
			{
				'label': 'Actions',
				'items': ['Employee Checkin']
			}
		]
	}
