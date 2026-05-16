import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import flt

from erpgenex_realestate_dev.coherence import assert_linked_company


class RESubcontractCommitment(Document):
	def validate(self):
		assert_linked_company("Development Project", self.development_project, self.company, None)
		if flt(self.committed_amount) < 0:
			frappe.throw(_("Committed amount cannot be negative."))
		if flt(self.invoiced_amount) < 0:
			frappe.throw(_("Invoiced amount cannot be negative."))
		if flt(self.invoiced_amount) > flt(self.committed_amount):
			frappe.throw(_("Invoiced amount cannot exceed committed amount."))
		self._sync_status()

	def _sync_status(self):
		if self.status == "Cancelled":
			return
		inv = flt(self.invoiced_amount)
		com = flt(self.committed_amount)
		if inv <= 0:
			self.status = "Open"
		elif inv >= com:
			self.status = "Closed"
		else:
			self.status = "Partially Invoiced"
