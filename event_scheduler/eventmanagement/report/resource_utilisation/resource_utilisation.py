import frappe
from frappe.query_builder import DocType
from frappe.query_builder.functions import Count, Sum, Round
from pypika import CustomFunction
from pypika.terms import LiteralValue


def execute(filters=None):

    # ✅ Columns
    columns = [
        {
            "label": "Resource Name",
            "fieldname": "resource_name",
            "fieldtype": "Data",
            "width": 200
        },
        {
            "label": "Resource Type",
            "fieldname": "resource_type",
            "fieldtype": "Data",
            "width": 150
        },
        {
            "label": "Times Used",
            "fieldname": "times_used",
            "fieldtype": "Int",
            "width": 120
        },
        {
            "label": "Total Hours",
            "fieldname": "total_hours",
            "fieldtype": "Float",
            "width": 120
        }
    ]

    # ✅ DocTypes
    ERA      = DocType("Event Resource Allocation")
    Resource = DocType("Resource")
    Events   = DocType("Events")

    # ✅ SQL function
    TimestampDiff = CustomFunction("TIMESTAMPDIFF", ["unit", "start", "end"])

    # ✅ Query (NO FILTERS)
    data = (
        frappe.qb
        .from_(ERA)
        .join(Resource).on(Resource.name == ERA.resource)
        .join(Events).on(Events.name == ERA.parent)
        .select(
            Resource.resource_name,
            Resource.resource_type,

            # 🔹 Times Used
            Count(Events.name).distinct().as_("times_used"),

            # 🔹 Total Hours
            Round(
                Sum(
                    TimestampDiff(
                        LiteralValue("MINUTE"),
                        Events.start_time,
                        Events.end_time
                    )
                ) / 60,
                2
            ).as_("total_hours")
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

    return columns, data