"""Cross-document checks for Erpgenex Real Estate Development."""

from __future__ import annotations

import frappe
from frappe import _
from frappe.utils import flt


def assert_linked_company(link_doctype: str, link_name: str, expected_company: str, label: str | None = None) -> None:
	if not link_name or not expected_company:
		return
	title = label or frappe.unscrub(link_doctype)
	if not frappe.db.exists(link_doctype, link_name):
		frappe.throw(_("{0} {1} does not exist.").format(title, frappe.bold(link_name)))
	lc = frappe.db.get_value(link_doctype, link_name, "company")
	if lc and lc != expected_company:
		frappe.throw(
			_("{0} {1} belongs to company {2}. Expected {3}.").format(
				title, frappe.bold(link_name), frappe.bold(lc), frappe.bold(expected_company)
			),
			title=_("Company mismatch"),
		)


def nonnegative_amount(value, label: str) -> None:
	if flt(value) < 0:
		frappe.throw(_("{0} cannot be negative.").format(label))


def optional_branch_company(branch: str, expected_company: str) -> None:
	if not branch or not expected_company:
		return
	br_co = frappe.db.get_value("Branch", branch, "company")
	if br_co and br_co != expected_company:
		frappe.throw(
			_("Branch {0} is scoped to company {1}.").format(frappe.bold(branch), frappe.bold(br_co)),
			title=_("Branch"),
		)
