# Copyright (c) 2026, ErpGenEx

from __future__ import annotations

import frappe
from frappe import _
from frappe.utils import flt


def execute(filters=None):
	filters = frappe._dict(filters or {})
	if not filters.get("company"):
		frappe.throw(_("Company is required"))

	budget_filters: dict = {"company": filters.company}
	if filters.get("development_project"):
		budget_filters["development_project"] = filters.development_project

	budgets = frappe.get_all(
		"Development Budget",
		filters=budget_filters,
		fields=["name", "development_project", "status", "total_budget"],
	)

	rows: list[dict] = []
	for b in budgets:
		lines = frappe.get_all(
			"Development Budget Line",
			filters={"parent": b.name},
			fields=["cost_code", "description", "budget_amount", "actual_amount"],
		)
		bac = sum(flt(l.budget_amount) for l in lines)
		ev = sum(flt(l.actual_amount) for l in lines)
		variance = ev - bac
		pct = round(100.0 * ev / bac, 2) if bac else 0.0
		rows.append(
			{
				"development_budget": b.name,
				"development_project": b.development_project,
				"budget_status": b.status,
				"bac": bac,
				"earned_value": ev,
				"variance": variance,
				"percent_complete": pct,
				"line_count": len(lines),
			}
		)

	columns = [
		{"label": _("Budget"), "fieldname": "development_budget", "fieldtype": "Link", "options": "Development Budget", "width": 120},
		{"label": _("Project"), "fieldname": "development_project", "fieldtype": "Link", "options": "Development Project", "width": 130},
		{"label": _("Status"), "fieldname": "budget_status", "fieldtype": "Data", "width": 90},
		{"label": _("BAC"), "fieldname": "bac", "fieldtype": "Currency", "width": 110},
		{"label": _("Earned Value"), "fieldname": "earned_value", "fieldtype": "Currency", "width": 120},
		{"label": _("Variance"), "fieldname": "variance", "fieldtype": "Currency", "width": 110},
		{"label": _("% Complete"), "fieldname": "percent_complete", "fieldtype": "Percent", "width": 100},
		{"label": _("Lines"), "fieldname": "line_count", "fieldtype": "Int", "width": 70},
	]

	return columns, rows
