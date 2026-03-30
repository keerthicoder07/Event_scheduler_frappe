import frappe
from frappe.query_builder import DocType
from frappe.query_builder.functions import Count, Sum
from pypika import CustomFunction
from pypika.terms import LiteralValue


@frappe.whitelist()
def get_resource_utilisation(from_date=None, to_date=None):

    ERA      = DocType("Event Resource Allocation")
    Resource = DocType("Resource")
    Events   = DocType("Events")

    TimestampDiff = CustomFunction("TIMESTAMPDIFF", ["unit", "start", "end"])

    query = (
        frappe.qb
        .from_(ERA)
        .join(Resource).on(Resource.name == ERA.resource)
        .join(Events).on(Events.name == ERA.parent)
        .select(
            Resource.resource_name,
            Resource.resource_type,
            Count(Events.name).distinct().as_("times_used"),
            Sum(
                TimestampDiff(
                    LiteralValue("MINUTE"),
                    Events.start_time,
                    Events.end_time
                )
            ).as_("total_minutes")
        )
        .groupby(
            Resource.name,
            Resource.resource_name,
            Resource.resource_type
        )
    )

    # ✅ Apply filters if given
    if from_date and to_date:
        query = query.where(
            (Events.start_time >= from_date) &
            (Events.end_time   <= to_date)
        )

    data = query.run(as_dict=True)

    # Convert minutes → hours
    for row in data:
        row["total_hours"] = round((row.get("total_minutes") or 0) / 60, 2)

    return data