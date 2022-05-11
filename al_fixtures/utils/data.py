from typing import Optional
import frappe
from frappe.utils import flt, get_number_format_info, in_words, cint, cstr

def custom_fmt_money(amount, precision=None, currency=None, format=None):
	"""
	Convert to string with commas for thousands, millions etc
	"""
	number_format = format or frappe.db.get_default("number_format") or "#,###.##"
	if precision is None:
		precision = cint(frappe.db.get_default("currency_precision")) or None

	decimal_str, comma_str, number_format_precision = get_number_format_info(number_format)

	if precision is None:
		precision = number_format_precision

	# 40,000 -> 40,000.00
	# 40,000.00000 -> 40,000.00
	# 40,000.23000 -> 40,000.23

	if isinstance(amount, str):
		amount = flt(amount, precision)

	if decimal_str:
		decimals_after = str(round(amount % 1, precision))
		parts = decimals_after.split(".")
		parts = parts[1] if len(parts) > 1 else parts[0]
		decimals = parts
		if precision > 2:
			if len(decimals) < 3:
				if currency:
					fraction = frappe.db.get_value("Currency", currency, "fraction_units", cache=True) or 100
					precision = len(cstr(fraction)) - 1
				else:
					precision = number_format_precision
			elif len(decimals) < precision:
				precision = len(decimals)

	amount = "%.*f" % (precision, round(flt(amount), precision))

	if amount.find(".") == -1:
		decimals = ""
	else:
		decimals = amount.split(".")[1]

	parts = []
	minus = ""
	if flt(amount) < 0:
		minus = "-"

	amount = cstr(abs(flt(amount))).split(".")[0]

	if len(amount) > 3:
		parts.append(amount[-3:])
		amount = amount[:-3]

		val = number_format == "#,##,###.##" and 2 or 3

		while len(amount) > val:
			parts.append(amount[-val:])
			amount = amount[:-val]

	parts.append(amount)

	parts.reverse()

	amount = comma_str.join(parts) + ((precision and decimal_str) and (decimal_str + decimals) or "")
	if amount != "0":
		amount = minus + amount

	if currency and frappe.defaults.get_global_default("hide_currency_symbol") != "Yes":
		# ------------ modified lines ------------
		# symbol is not used anymore
		#symbol = frappe.db.get_value("Currency", currency, "symbol", cache=True) or currency
		#amount = symbol + " " + amount

		# alternative money format
		amount = amount + " " + currency
		# --------- end of modified lines ---------

	return amount

def money_in_words(
	number: str, main_currency: Optional[str] = None, fraction_currency: Optional[str] = None
):
	"""
	Returns string in words with currency and fraction currency.
	"""
	from frappe.utils import get_defaults

	_ = frappe._

	try:
		# note: `flt` returns 0 for invalid input and we don't want that
		number = float(number)
	except ValueError:
		return ""

	number = flt(number)
	if number < 0:
		return ""

	d = get_defaults()
	if not main_currency:
		main_currency = d.get("currency", "INR")
	if not fraction_currency:
		fraction_currency = frappe.db.get_value("Currency", main_currency, "fraction", cache=True) or _(
			"Cent"
		)

	number_format = (
		frappe.db.get_value("Currency", main_currency, "number_format", cache=True)
		or frappe.db.get_default("number_format")
		or "#,###.##"
	)

	fraction_length = get_number_format_info(number_format)[2]

	n = "%.{0}f".format(fraction_length) % number

	numbers = n.split(".")
	main, fraction = numbers if len(numbers) > 1 else [n, "00"]

	if len(fraction) < fraction_length:
		zeros = "0" * (fraction_length - len(fraction))
		fraction += zeros

	in_million = True
	if number_format == "#,##,###.##":
		in_million = False

	# 0.00
	if main == "0" and fraction in ["00", "000"]:
		out = "{0} {1}".format(main_currency, _("Zero"))
	# 0.XX
	elif main == "0":
		out = _(in_words(fraction, in_million).title()) + " " + fraction_currency
	else:
		out = _(in_words(main, in_million).title()) + " " + main_currency
		if cint(fraction):
			out = (
				out
				+ " "
				+ _("and")
				+ " "
				+ _(in_words(fraction, in_million).title())
				+ " "
				+ fraction_currency
			)

	return out
