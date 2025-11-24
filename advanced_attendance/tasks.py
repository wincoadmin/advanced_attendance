import frappe
from frappe.utils import now_datetime, add_days, getdate
from .utils import (
    process_attendance_window,
    summarize_anomalies_for_date
)

def sync_biometric_devices():
    """
    Scheduled job to sync all enabled biometric devices.
    Runs every 5 minutes (configured in hooks.py).
    """
    from advanced_attendance.zkteco_connector import sync_all_devices
    
    try:
        frappe.logger().info("Starting biometric device sync...")
        result = sync_all_devices()
        
        if result.get('success'):
            frappe.logger().info(
                f"Biometric sync completed: {result.get('total_records', 0)} records "
                f"from {result.get('devices_synced', 0)} device(s)"
            )
            
            # Log errors if any
            if result.get('errors'):
                frappe.logger().warning(f"Sync errors: {result.get('errors')}")
        else:
            frappe.logger().error(f"Biometric sync failed: {result.get('message')}")
            
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Biometric Sync Task Failed")
        frappe.logger().error(f"Biometric sync exception: {str(e)}")


def process_attendance_punches():
    """
    Scheduled job to process attendance for recent days.
    Typical window: yesterday and today (or last 2-3 days).
    """
    today = getdate()
    from_date = add_days(today, -2)
    to_date = today

    frappe.logger().info(f"advanced_attendance.process_attendance_punches: processing from {from_date} to {to_date}")

    process_attendance_window(from_date, to_date)


def generate_daily_anomaly_snapshot():
    """
    Scheduled job to summarize anomalies for previous day.
    Can be extended to send emails or update dashboard.
    """
    today = getdate()
    target_date = add_days(today, -1)

    frappe.logger().info(f"advanced_attendance.generate_daily_anomaly_snapshot: summarizing for {target_date}")

    summarize_anomalies_for_date(target_date)
