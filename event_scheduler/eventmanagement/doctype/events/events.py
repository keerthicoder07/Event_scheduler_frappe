# Copyright (c) 2026, Keerthi and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import getdate,format_datetime,get_datetime
from frappe.query_builder import DocType

class Events(Document):
	def before_save(self):
		self.calculate_end_time()


	def validate(self):
		self.validate_time()
		self.validate_resource_conflicts()
	def on_submit(self):
		
		frappe.msgprint("Event fixed succesfully")
	def on_cancel(self):
		frappe.msgprint("Event completed and resource is free")


	#Logic Functions
	def validate_time(self):
		if not self.start_time:
			frappe.throw("Start Time is required")
		if not self.total_hours:
			frappe.throw("Total Hours is required")
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
		ERA=DocType("Event Resource Allocation")
		Event=DocType("Events")
		for row in self.resources:
			conflicts=(
				frappe.qb.from_(ERA)
				.join(Event)
				.on(Event.name==ERA.parent)
				.select(
					Event.name,
					Event.title,
					Event.start_time,
					Event.end_time,
					ERA.resource
				)
				.where(
					(ERA.resource==row.resource)&(Event.name!=(self.name or "new-event"))&(Event.docstatus==1)&
					(
						(Event.end_time>=self.start_time)&(Event.start_time<=self.end_time)
					)
				)
			).run(as_dict=True)
			for conflict in conflicts:
				all_conflicts.append(
					f"Resource <b>{conflict['resource']}</b>"
					f"is already booked in <b>{conflict['title']}</b>"
					f"Try again after <b>{format_datetime(conflict['end_time'],'dd MMM YYYY hh:mm a')}</b>"
				)
		if all_conflicts:
			frappe.throw(
				"The following conflicts were found:"
				"<br><br>"+"<br><br>".join(all_conflicts)
				)
		#frappe.msgprint(str(all_conflicts))

	
	def calculate_end_time(self):
		if self.start_time and self.total_hours:
			# Convert hours to seconds
			import datetime
			duration_seconds = self.total_hours * 3600

			# Calculate end time
			if isinstance(self.start_time, str):
				
				start = get_datetime(self.start_time)
			else:
				start = self.start_time

			# ✅ Set end_time
			self.end_time = start + datetime.timedelta(
				seconds=duration_seconds
			)