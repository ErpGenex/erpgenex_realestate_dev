import frappe
from frappe.model.document import Document


class REBOQItem(Document):
	def validate(self):
		qty = float(self.qty or 0)
		rate = float(self.rate or 0)
		self.amount = qty * rate

