import frappe
from frappe.model.document import Document
from frappe.query_builder import DocType
from frappe.query_builder.functions import Count


class Resource(Document):
    pass


@frappe.whitelist()
def get_resource_utilisation(from_date, to_date):

    if from_date > to_date:
        frappe.throw("From Date must be less than To Date")
    ERA=DocType("Event Resource Allocation")
    Resource=DocType("Resource")
    Events=DocType("Events")

    data = (
        frappe.qb
        .from_(ERA)
        .join(Resource)
        .on(Resource.name == ERA.resource)
        .join(Events)
        .on(Events.name == ERA.parent)
        .select(
            Resource.resource_name,
            Resource.resource_type,
            Count(Events.name).as_("times_used")
        )
        .where(
            (Events.start_time >= from_date) &
            (Events.end_time   <= to_date)
        )
        .groupby(
            Resource.name,
            Resource.resource_name,
            Resource.resource_type
        )
        .orderby(
            Count(Events.name),
            order=frappe.qb.desc
        )
    ).run(as_dict=True)
    # ✅ Just return HTML — no PDF!
    html = frappe.render_template(
        "event_scheduler/templates/resource_utilization.html",
        {
            "data":      data,
            "from_date": frappe.utils.formatdate(from_date,"dd MMM YY"),
            "to_date":   frappe.utils.formatdate(to_date,"dd MMM YY")
        }
    )

    return html