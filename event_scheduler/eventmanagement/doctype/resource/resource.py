# Copyright (c) 2026, Keerthi and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Resource(Document):
	@frappe.whitelist()
	def get_resource_utilisation_pdf(from_date, to_date):

		if from_date > to_date:
			frappe.throw("From Date must be less than To Date")

		data = frappe.db.sql("""
			SELECT
				r.resource_name,
				r.resource_type,
				COUNT(DISTINCT e.name)   AS times_used
			FROM
				`tabEvent Resource Allocation` era
			JOIN
				`tabResource` r ON r.name = era.resource
			JOIN
				`tabEvents`   e ON e.name = era.parent
			WHERE
				e.start_time >= %(from_date)s
				AND e.end_time <= %(to_date)s
			GROUP BY
				r.name,
				r.resource_name,
				r.resource_type
			ORDER BY
				times_used DESC
		""", {
			"from_date": from_date,
			"to_date":   to_date,
		}, as_dict=True)

		html = frappe.render_template(
			"event_scheduler/templates/resource_utilisation.html",
			{
				"data":      data,
				"from_date": from_date,
				"to_date":   to_date,
			}
		)

		pdf = frappe.utils.pdf.get_pdf(html)

		frappe.local.response.filename = f"Resource_Utilisation_{from_date}_to_{to_date}.pdf"
		frappe.local.response.filecontent = pdf
		frappe.local.response.type = "download"


