# Copyright (c) 2026, ErpGenEx
import frappe
from frappe.tests.utils import FrappeTestCase


class TestSapParityReDev(FrappeTestCase):
	def test_dev_project_doctype_exists(self):
		self.assertTrue(frappe.db.exists("DocType", "Development Project"))
		self.assertTrue(frappe.db.exists("DocType", "RE BOQ"))
