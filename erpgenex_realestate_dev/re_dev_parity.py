# Copyright (c) 2026, ErpGenEx
from frappe.utils import flt


def preview_dev_budget_variance(budget: float, committed: float, actual: float) -> dict:
	b = flt(budget)
	c = flt(committed)
	a = flt(actual)
	return {
		"budget": b,
		"committed": c,
		"actual": a,
		"variance_budget_actual": flt(b - a, 2),
		"variance_committed_actual": flt(c - a, 2),
		"sap_module": "PS/RE",
	}
