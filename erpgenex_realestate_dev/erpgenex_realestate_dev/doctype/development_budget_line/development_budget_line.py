import frappe
from frappe import _
from frappe.model.document import Document

from erpgenex_realestate_dev.coherence import nonnegative_amount


class DevelopmentBudgetLine(Document):
	def validate(self):
		nonnegative_amount(self.budget_amount, _("Budget Amount"))
