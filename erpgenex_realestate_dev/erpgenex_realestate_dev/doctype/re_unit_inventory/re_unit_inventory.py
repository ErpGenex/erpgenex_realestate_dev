import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import flt

from erpgenex_realestate_dev.coherence import assert_linked_company


class REUnitInventory(Document):
	def validate(self):
		assert_linked_company("Development Project", self.development_project, self.company, None)
		for label, field in (
			(_("GIA"), "gia_sqm"),
			(_("NIA"), "nia_sqm"),
			(_("Salable Area"), "salable_area_sqm"),
		):
			val = getattr(self, field, None)
			if val is not None and flt(val) < 0:
				frappe.throw(_("{0} cannot be negative.").format(label), title=_("RE Unit Inventory"))
		gia, nia = flt(self.gia_sqm), flt(self.nia_sqm)
		if gia and nia and nia > gia:
			frappe.throw(_("NIA cannot exceed GIA."), title=_("RE Unit Inventory"))
		if self.status == "Available" and not self.is_new():
			if frappe.db.exists(
				"Sales Booking",
				{"re_unit_inventory": self.name, "status": ["in", ["Approved", "Registered"]]},
			):
				frappe.throw(
					_("Cannot set inventory to Available while an approved or registered booking exists."),
					title=_("RE Unit Inventory"),
				)
