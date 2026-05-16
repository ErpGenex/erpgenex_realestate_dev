import frappe
from frappe import _
from frappe.model.document import Document

from erpgenex_realestate_dev.coherence import assert_linked_company


class REHandoverPackage(Document):
	def validate(self):
		assert_linked_company("RE Unit Inventory", self.re_unit_inventory, self.company, None)

		if self.status == "Signed Off":
			inv_status = frappe.db.get_value("RE Unit Inventory", self.re_unit_inventory, "status")
			if inv_status != "Sold":
				frappe.throw(
					_("Inventory must be in Sold status before handover sign-off (current status: {0}).").format(
						inv_status or "?"
					),
					title=_("RE Handover Package"),
				)
			for row in self.snag_items or []:
				if row.severity == "Critical" and row.status == "Open":
					frappe.throw(
						_("Close all critical snag items before sign-off."),
						title=_("RE Handover Package"),
					)

	def on_update(self):
		if self.status != "Signed Off":
			return
		frappe.db.set_value(
			"RE Unit Inventory",
			self.re_unit_inventory,
			"status",
			"Handed Over",
			update_modified=False,
		)
