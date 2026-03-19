# Copyright (c) 2026, Keerthi and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class Events(Document):
	def validate_time(self):
		if(self.start_time > self.end_time):
			frappe.throw("End time must greater than start time")

	def validate_resource_conflicts(self):
		for row in self.resources:
			conflicts=frappe.db.sql("""
			select 
			e.name,
			e.title,
			e.start_time,
			e.end_time
			from `tabEvent Resource Allocation` era

			join

			`tabEvents e on e.name = era.parent

			where 
			era.resource=%(resource)s
			AND e.name!=%(name)s
			AND e.docstatus<2
			AND NOT(
			e.end_time<=%(start_time)s
			)
			""",
			{
				"resource":row.resource,
				"name"self.name or "new-event",
				"start_time":self.start_time,
				"end_time":self.end_time,

			},as_dict=True)


