# Copyright (c) 2026, Keerthi and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.query_builder import DocType                    # ← missing!
from frappe.query_builder.functions import Count  
from frappe.utils import formatdate
class ResourceUtilisation(Document):
	pass
@frappe.whitelist()
def get_resource_utilisation(from_date, to_date):

    if from_date > to_date:
        frappe.throw("From Date must be less than To Date")

    # ── DocType references ─────────────────────────────────
    ERA      = DocType("Event Resource Allocation")
    Resource = DocType("Resource")
    Events   = DocType("Events")

    # ── Query Builder ──────────────────────────────────────
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
            Count(Events.name).distinct()
                .as_("times_used")
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

    # ── Render HTML ────────────────────────────────────────
    html = frappe.render_template(
        "event_scheduler/templates/resource_utilization.html",
        {
            "from_date": formatdate(from_date, "dd MMM yyyy"),
            "to_date":   formatdate(to_date,   "dd MMM yyyy"),
            "data":      data,
        }
    )

    return html
