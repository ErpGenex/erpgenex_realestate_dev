# Copyright (c) 2026, ErpGenEx

from __future__ import annotations

import frappe
from frappe.utils import getdate, today


def flag_overdue_permit_milestones() -> int:
	"""Mark pending permit milestones past due_date as Overdue."""
	due = getdate(today())
	names = frappe.get_all(
		"RE Permit Milestone",
		filters={
			"status": ["in", ["Pending", "Submitted"]],
			"due_date": ["<", due],
		},
		pluck="name",
	)
	for name in names:
		frappe.db.set_value("RE Permit Milestone", name, "status", "Overdue", update_modified=False)
	return len(names)
