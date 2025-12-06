from neomodel import IntegerProperty, StringProperty, ArrayProperty, StructuredRel


class HasPanel(StructuredRel):
    lowest_age_years = IntegerProperty(required=False, db_property="lowestAgeYears")
    lowest_age_months = IntegerProperty(required=False, db_property="lowestAgeMonths")
    highest_age_years = IntegerProperty(required=False, db_property="highestAgeYears")
    highest_age_months = IntegerProperty(required=False, db_property="highestAgeMonths")
    gender_limitation = StringProperty(required=False, db_property="genderLimitation")
    service_population = ArrayProperty(StringProperty(), required=False, db_property="servicePopulation")
    status = StringProperty(required=False)