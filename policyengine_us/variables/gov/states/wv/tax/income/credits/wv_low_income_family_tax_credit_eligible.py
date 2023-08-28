from policyengine_us.model_api import *


class wv_low_income_family_tax_credit_eligible(Variable):
    value_type = bool
    entity = TaxUnit
    label = "Eligible for the West Virginia low-income family tax credit"
    definition_period = YEAR
    defined_for = StateCode.WV

    def formula(tax_unit, period, parameters):
        # modified agi needed to be modified
        wv_agi = tax_unit("wv_agi", period)

        p = parameters(
            period
        ).gov.states.wv.tax.income.credits.low_income_family_tax_credit

        # max family size limit
        n = tax_unit("tax_unit_size", period)
        tax_unit = min_(n, p.max_family_size)
        fpg = tax_unit("tax_unit_fpg", period)

        # modified agi limit
        fpg_amount = p.fpg_percent * fpg
        income_threshold = p.income_threshold + fpg_amount
        return wv_agi <= income_threshold
