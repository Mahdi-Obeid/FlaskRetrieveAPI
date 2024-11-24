from persiantools.jdatetime import JalaliDate


def jalali_to_gregorian_year(jalali_year: int) -> int:
    jalali_date = JalaliDate(jalali_year, 1, 1)
    return jalali_date.to_gregorian().year
