import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import flt

from erpgenex_realestate_dev.coherence import assert_linked_company


class DevelopmentBudget(Document):
	def validate(self):
		assert_linked_company("Development Project", self.development_project, self.company, None)
		if self.reference_boq:
			row = frappe.db.get_value(
				"RE BOQ",
				self.reference_boq,
				["company", "development_project"],
				as_dict=True,
			)
			if row and row.company != self.company:
				frappe.throw(_("Reference BOQ belongs to another company."), title=_("Development Budget"))
			if row and row.development_project and row.development_project != self.development_project:
				frappe.throw(
					_("Reference BOQ is tied to another development project."),
					title=_("Development Budget"),
				)

		self.total_budget = sum(flt(r.budget_amount) for r in (self.budget_lines or []))
		for row in self.budget_lines or []:
			if flt(row.actual_amount) < 0:
				frappe.throw(_("Actual amount cannot be negative on line {0}.").format(row.cost_code))
