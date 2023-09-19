from policyengine_us.model_api import *


class ga_retirement_exclusion(Variable):
    value_type = float
    entity = TaxUnit
    label = "Georgia retirement exclusion"
    unit = USD
    definition_period = YEAR
    reference = (
        "https://dor.georgia.gov/document/booklet/2021-it-511-individual-income-tax-booklet/download#page=15"
        "https://dor.georgia.gov/document/document/2022-it-511-individual-income-tax-booklet/download#page=15"
        "https://advance.lexis.com/documentpage/?pdmfid=1000516&crid=fb5db531-a80f-4790-bddb-eefc8327ef60&config=00JAA1MDBlYzczZi1lYjFlLTQxMTgtYWE3OS02YTgyOGM2NWJlMDYKAFBvZENhdGFsb2feed0oM9qoQOMCSJFX5qkd&pddocfullpath=%2Fshared%2Fdocument%2Fstatutes-legislation%2Furn%3AcontentItem%3A65D2-CDH3-CGX8-044N-00008-00&pdcontentcomponentid=234186&pdteaserkey=sr1&pditab=allpods&ecomp=8s65kkk&earg=sr1&prid=66f02b0a-c5ae-4162-9535-127751546807"
    )
    defined_for = StateCode.GA

    def formula(tax_unit, period, parameters):
        person = tax_unit.members
        p = parameters(period).gov.states.ga.tax.income.agi.exclusions
        retirement_income = person("ga_retirement_income", period)
        age_younger = (person("age", period) >= p.retirement.age.younger) & (
            person("age", period) < p.retirement.age.older
        )
        age_older = person("age", period) >= p.retirement.age.older
        cap_younger = p.retirement.cap.exclusion.younger
        cap_older = p.retirement.cap.exclusion.older
        capped_younger_exclusion = min_(retirement_income, cap_younger)
        capped_older_exclusion = min_(retirement_income, cap_older)

        head = person("is_tax_unit_head", period)
        spouse = person("is_tax_unit_spouse", period)
        head_or_spuse = head | spouse
        disabled = person("is_disabled", period)
        older_eligible = (head_or_spuse) & age_older
        older_exclusion = where(older_eligible, capped_older_exclusion, 0)
        younger_eligible = (head_or_spuse) & age_younger
        disabled_eligible = (head_or_spuse) & disabled
        younger_exclusion = where(
            younger_eligible | disabled_eligible, capped_younger_exclusion, 0
        )
        return tax_unit.sum(older_exclusion + younger_exclusion)
