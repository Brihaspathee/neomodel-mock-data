from neomodel import IntegerProperty, StringProperty, ArrayProperty, StructuredRel


class HasPanel(StructuredRel):
    lowest_age_years = IntegerProperty(required=False)
    lowest_age_months = IntegerProperty(required=False)
    highest_age_years = IntegerProperty(required=False)
    highest_age_months = IntegerProperty(required=False)
    gender_limitation = StringProperty(required=False)
    service_population = ArrayProperty(StringProperty(), required=False)
    status = StringProperty(required=False)