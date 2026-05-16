from frappe.model.document import Document

from erpgenex_realestate_dev.coherence import assert_linked_company


class LandParcel(Document):
	def validate(self):
		if getattr(self, "development_project", None):
			assert_linked_company(
				"Development Project",
				self.development_project,
				self.company,
				None,
			)
