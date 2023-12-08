from policyengine_us.model_api import *


class refundable_child_care_credit(Variable):
    value_type = float
    entity = TaxUnit
    label = "Maine refundable child care credit"
    unit = USD
    documentation = "Refundable portion of the Maine child care credit"
    definition_period = YEAR
    reference = "https://www.mainelegislature.org/legis/statutes/36/title36sec5218.html"
    defined_for = StateCode.ME

    def formula(tax_unit, period, parameters):
        p = parameters(period).gov.states.me.tax.income.credits.child_care
        return min_(p.max_amount, tax_unit("child_care_credit", period))