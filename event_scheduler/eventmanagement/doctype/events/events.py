# Copyright (c) 2026, Keerthi and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import getdate

class Events(Document):

	def validate(self):
		self.validate_time()
		self.validate_resource_conflicts()
	def on_submit(self):
		frappe.msgprint("Event fixed succesfully")
	def on_cancel(self):
		frappe.msgprint("Event completed and resource is free")

	#Logic Functions
	def validate_time(self):
		if(self.start_time > self.end_time):
			frappe.throw("End time must greater than start time")

	def validate_resource_conflicts(self):
		for row in self.resources:
			conflicts=frappe.db.sql("""
                SELECT
                    e.name,
                    e.title,
                    e.start_time,
                    e.end_time
                FROM
                    `tabEvent Resource Allocation` era
                JOIN
                    `tabEvents` e ON e.name = era.parent
                WHERE
                    era.resource   = %(resource)s
                    AND e.name    != %(name)s
                    AND e.docstatus < 2
                    AND NOT (
                        e.end_time   <= %(start_time)s
                        OR e.start_time >= %(end_time)s
                    )
            """,
			{
				"resource":row.resource,
				"name":self.name or "new-event",
				"start_time":self.start_time,
				"end_time":self.end_time,

			},as_dict=True)
			if conflicts:
				frappe.throw(
					f"Resource <b>{row.resource}</b> is already booked"
					f"in Event <b>{conflicts[0]['title']}</b> "
					f"Try again after <b>{conflicts[0]['end_time']}"
				)
	


