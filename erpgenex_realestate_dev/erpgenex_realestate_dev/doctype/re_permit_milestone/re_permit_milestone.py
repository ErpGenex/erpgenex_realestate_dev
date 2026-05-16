import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import getdate, today

from erpgenex_realestate_dev.coherence import assert_linked_company


class REPermitMilestone(Document):
	def validate(self):
		assert_linked_company("Development Project", self.development_project, self.company, None)
		if self.status not in ("Approved", "Cancelled") and self.due_date:
			if getdate(self.due_date) < getdate(today()) and self.status not in ("Overdue",):
				self.status = "Overdue"
		if self.status == "Approved" and not self.completed_date:
			self.completed_date = today()
