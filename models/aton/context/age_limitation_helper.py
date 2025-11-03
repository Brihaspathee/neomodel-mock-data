class AgeLimitationHelper:

    def __init__(self, lowest_units: str | None,
                 highest_units: str | None,
                 lowest_age: int | None,
                 highest_age: int | None):
        self.lowest_units = lowest_units
        self.highest_units = highest_units
        self.lowest_age = lowest_age
        self.highest_age = highest_age