import frappe
from frappe.utils import now_datetime
from frappe.query_builder import DocType

def auto_cancel_expired_events():
    Events=DocType("Events")
    expired_events=(
        frappe.qb.from_(Events)
        .select(
            Events.name,
            Events.title
        )
        .where(
            (Events.docstatus==1)&
            (Events.end_time<=now_datetime())
        )
    ).run(as_dict=True)
    frappe.logger().info(
        f"Found{len(expired_events)} expired events"
    )

    for event in expired_events:
        try:
            doc=frappe.get_doc("Events",event.name)
            doc.cancel()
            frappe.publish_realtime(
                event="event_auto_cancelled",
                message={
                    "event_name":doc.name,
                    "title":doc.title,
                    "message":f"Event <b>{doc.title}</b> "
                              f"has ended-resources released",  
                }
            )
            frappe.logger().info(
                f"Auto cancelled:{event.name}"
            )
        except Exception as e:
            frappe.logger().error(
                f"Failed to cancel {event.name}:{str(e)}"
            )