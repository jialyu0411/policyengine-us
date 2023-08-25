from policyengine_us.model_api import *


class co_itemized_or_standard_deduction_addback_eligible(Variable):
    value_type = bool
    entity = TaxUnit
    label = "Eligible for the Colorado itemized or standard deduction add back"
    definition_period = YEAR
    reference = (
        # C.R.S. 39-22-104 . Income tax imposed on individuals, estates, and trusts - section (3)(p) - (p.5)
        "https://casetext.com/statute/colorado-revised-statutes/title-39-taxation/specific-taxes/income-tax/article-22-income-tax/part-1-general/section-39-22-104-effective-upon-official-proclamation-by-governor-income-tax-imposed-on-individuals-estates-and-trusts-single-rate-report-legislative-declaration-definitions-repeal",
        # 2022 Colorado Individual Income Tax Filing Guide - Additions - Line 4
        "https://tax.colorado.gov/sites/tax/files/documents/DR_104_Book_2022.pdf#page=5",
        # Individual Income Tax Guide - Part 3 Additions to Taxable Income - Federal itemized or standard deductions
        "https://tax.colorado.gov/individual-income-tax-guide",
    )
    defined_for = StateCode.CO

    def formula(tax_unit, period, parameters):
        p = parameters(
            period
        ).gov.states.co.tax.income.additions.itemized_or_standard_deduction_addback
        return tax_unit("adjusted_gross_income", period) > p.agi_threshold