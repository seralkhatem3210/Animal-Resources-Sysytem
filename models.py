from odoo import models, fields,api
from odoo.exceptions import UserError

class Department(models.Model):
	_name = "animaldepartment"
	name = fields.Char(required=True, string="Department Name")
	number = fields.Integer()
	description = fields.Text()
	is_active = fields.Selection(selection=[("active","Active"),("not_active","Not Active")],help="to activate this department")
	budget = fields.Float(default=100000.0, readonly=True)
	start = fields.Date()
	working = fields.Datetime()
	logo = fields.Binary()
	atype = fields.Selection(selection=[('general','General'),('sub','Sub')], default="general")
	employees = fields.One2many("animalemployee","department_id")
	payrolls = fields.One2many("animal.payroll","department_id")

	def action_activate(self):
		self.is_active = "active"

	def action_disactivate(self):
		self.is_active = "not_active"

	def cal_payroll(self):
		for rec in self:
			employees = self.env["animalemployee"].search([]) #('age','>',10)

			# employees.unlink()
			# rec.payrolls.unlink()

			for employee in employees:

				allowance = 20000
				salary_total = employee.salary + allowance

				emp_id = self.env["animal.payroll"].create({
					"employee_id": employee.id,
					"salary": salary_total,
					"department_id": rec.id, #employee.department_id.id
					})

				# employee.write({
				# 	"salary": 4000
				# 	})

	@api.model
	def create(self,vals):

		vals["name"] = vals["name"]+"HR"
		vals["description"] = "Test"

		return super(Department,self).create(vals)

	def write(self,vals):

		vals["description"] = "Test2"

		return super(Department,self).write(vals)

	def unlink(self):
		if (self.is_active == "active"):
			raise UserError("Tiis record must be canceld first")

		return super(Department,self).unlink()

class Payroll (models.Model):
	_name = "animal.payroll"
	_rec_name = "employee_id"

	employee_id = fields.Many2one("animalemployee")
	salary = fields.Float()
	department_id = fields.Many2one("animaldepartment")

class Employee(models.Model):
	_name = "animalemployee"
	name = fields.Char()
	age = fields.Integer()
	birth_date = fields.Date()
	salary = fields.Float()
	image = fields.Binary()
	department_id = fields.Many2one("animaldepartment")
	payrolls = fields.One2many("animal.payroll","employee_id")
	payroll_count = fields.Integer(compute="_cal_payroll_count",store=True)

	@api.depends("payrolls")
	def _cal_payroll_count(self):
		for employee in self:

			employee.payroll_count = len(employee.payrolls)

class Shop(models.Model):
	_name = "animalshop"
	city = fields.Char()
	days_work = fields.Integer()
	market_class = fields.Selection(selection=[("main","Main"),("secondary","Secondary"),("final","Final")])
	fish = fields.Many2many("animalfish")

	_rec_name = "city"

class fish(models.Model):
	_name = "animalfish"
	name = fields.Char()
	fish_type = fields.Char()
	price = fields.Float()









