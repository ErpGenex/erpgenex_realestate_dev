from frappe.model.document import Document

from erpgenex_realestate_dev.coherence import optional_branch_company


class DevelopmentProject(Document):
	def validate(self):
		optional_branch_company(self.branch, self.company)
