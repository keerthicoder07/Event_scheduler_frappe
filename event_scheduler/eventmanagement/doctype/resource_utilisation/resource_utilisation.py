# Copyright (c) 2026, Keerthi and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.query_builder import DocType                    # ← missing!
from frappe.query_builder.functions import Count  
from frappe.utils import formatdate
class ResourceUtilisation(Document):
	pass
