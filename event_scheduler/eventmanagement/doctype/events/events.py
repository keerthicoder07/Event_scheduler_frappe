# Copyright (c) 2026, Keerthi and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import getdate,format_datetime

class Events(Document):
	def before_save(self):
		self.calculate_end_time()


	def validate(self):
		self.validate_time()
		self.validate_resource_conflicts()
	def on_submit(self):
		
		self.update_resource_status("Booked")
		frappe.msgprint("Event fixed succesfully")
	def on_cancel(self):
		self.update_resource_status("Available")
		frappe.msgprint("Event completed and resource is free")


	#Logic Functions
	def validate_time(self):
		if(self.total_hours<=0):
			frappe.throw("Total hours must be grater than 0")
		

	def validate_resource_conflicts(self):
		all_conflicts = []
		seen_resources=[]
		for res in self.resources:
			if(res.resource in seen_resources):
				frappe.throw(
					f"Resource <b>{res.resource}</b> "
					f"is added more than once!")
			seen_resources.append(res.resource)
		for row in self.resources:
			resource_data = frappe.db.get_value(
        "Resource",
        row.resource,
        ["status", "end_time", "event"],
        as_dict=True
    )

			if resource_data.status == "Booked":
				all_conflicts.append(
					f"Resource <b>{row.resource}</b> "
					f"is currently <b>Booked</b> "
					f"by Event <b>{resource_data.event}</b>!<br>"
					f"Please try again after "
				f"<b>{format_datetime(resource_data.end_time, 'dd MMM yyyy hh:mm a')}</b>"
			)

		# ✅ Show ALL booked resources at once
		if all_conflicts:
			conflict_message = "<br><br>".join(all_conflicts)
			frappe.throw(
				f"The following conflicts were found:"
				f"<br><br>{conflict_message}"
			)
	def update_resource_status(self,status):
		for row in self.resources:
			if frappe.db.exists("Resource",row.resource):
				frappe.db.sql("""
					update `tabResource`
					set status=%(status)s,end_time=%(end_time)s,event=%(event)s
					where name=%(resource)s
				""",
				{
					"status":status,
					"end_time":self.end_time,
					"event":self.name,
					"resource":row.resource,
				}
				)
			else:
				frappe.msgprint(
					f"Resource <b>{row.resource}</b> not found"
				)
	
	def calculate_end_time(self):
		if self.start_time and self.total_hours:
			# Convert hours to seconds
			import datetime
			duration_seconds = self.total_hours * 3600

			# Calculate end time
			if isinstance(self.start_time, str):
				from frappe.utils import get_datetime
				start = get_datetime(self.start_time)
			else:
				start = self.start_time

			# ✅ Set end_time
			self.end_time = start + datetime.timedelta(
				seconds=duration_seconds
			)