import frappe


@frappe.whitelist()
def preview_dev_budget_variance(budget: float, committed: float, actual: float) -> dict:
	from erpgenex_realestate_dev.re_dev_parity import preview_dev_budget_variance as _preview

	return _preview(budget, committed, actual)
