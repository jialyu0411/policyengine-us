from policyengine_us.model_api import *


class az_property_tax_credit(Variable):
    value_type = float
    entity = TaxUnit
    label = "Arizona Property Tax Credit"
    unit = USD
    definition_period = YEAR
    defined_for = "az_property_tax_credit_eligible"

    def formula(tax_unit, period, parameters):
        person = tax_unit.members
        p = parameters(period).gov.states.az.tax.income.credits.property_tax
        income = tax_unit("az_property_tax_credit_income", period)

        cohabitating = tax_unit("cohabitating_spouses", period)

        cap = where(
            cohabitating,
            p.amount.cohabitating.calc(income),
            p.amount.living_alone.calc(income),
        )

        property_tax = add(tax_unit, period, ["real_estate_taxes"])
        rent = add(tax_unit, period, ["rent"])
        payment_credit = property_tax + rent
        # property_tax and rent are equally weighted (tax form says just sum them up)

        return min_(cap, payment_credit)
