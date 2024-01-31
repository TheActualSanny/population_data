from pydantic import BaseModel, field_validator

class Residental_Data(BaseModel):
    residental_area: str
    stated_year: int
    below_6: int
    from_6_to_10: int
    from_10_to_18: int
    from_18_to_25: int
    from_25_to_30: int
    from_30_to_50: int
    from_50_to_65: int
    from_65_to_75: int
    older_than_75: int
    
    @field_validator('from_10_to_18', 'from_6_to_10', 'from_10_to_18', 
                     'from_18_to_25', 'from_25_to_30', 'from_30_to_50',
                     'from_50_to_65', 'from_65_to_75', 'older_than_75',
                     'below_6', mode = 'before')
    @classmethod
    def check_below_6(cls, val):
        if val == '.' or not val:
            return 0
        return int(val)