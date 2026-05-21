# Copyright (c) 2026, Omnexa and contributors
# License: MIT. See license.txt

import frappe
from frappe import _

from omnexa_core.omnexa_core.report_print.report_query_filters import (
	get_all_filters,
	policy_version_filters,
	prepare_filters,
	sql_conditions,
)



def execute(filters=None):
	filters = prepare_filters(filters)
	filters_dict = get_all_filters(filters, "Development Budget", date_field="creation", company=True, branch=True, extra_links={})
	data = frappe.get_all(
		"Development Budget",
		fields=['name', 'development_project', 'status', 'total_budget'],
		filters=filters_dict,
		limit_page_length=5000,
	)

	return [
		{"label": _("Budget"), "fieldname": "development_budget", "fieldtype": "Link", "options": "Development Budget", "width": 120},
		{"label": _("Project"), "fieldname": "development_project", "fieldtype": "Link", "options": "Development Project", "width": 130},
		{"label": _("Status"), "fieldname": "budget_status", "fieldtype": "Data", "width": 90},
		{"label": _("BAC"), "fieldname": "bac", "fieldtype": "Currency", "width": 110},
		{"label": _("Earned Value"), "fieldname": "earned_value", "fieldtype": "Currency", "width": 120},
		{"label": _("Variance"), "fieldname": "variance", "fieldtype": "Currency", "width": 110},
		{"label": _("% Complete"), "fieldname": "percent_complete", "fieldtype": "Percent", "width": 100},
		{"label": _("Lines"), "fieldname": "line_count", "fieldtype": "Int", "width": 70},
	], data
