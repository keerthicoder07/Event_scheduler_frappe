import frappe
from frappe.utils import now_datetime

def auto_cancel_expired_events():
    expired_events=frappe.db.sql("""
    select name,title from `tabEvents`
    where
    docstatus=1
    and end_time<=%(now)s
    """,
    {
        "now":now_datetime()
    },as_dict=True)

    for event in expired_events:
        try:
            doc=frappe.get_doc("Events",event.name)
            doc.cancel()
            frappe.publish_realtime(
                event="event_auto_cancelled",
                message={
                    "event_name":doc.name,
                    "title":doc.title,
                    "message":f"Event <b>{doc.title}</b> has ended - resources released"
                }
            )
            frappe.logger().info(
                f"Auto cancelled event:{event.name}"
            )
        except Exception as e:
            frappe.logger().error(
                f"Failed to cancel event{event.name}:{str(e)}"
            )