import re
from datetime import date

partial_date_re = re.compile(r"^(?P<year>\d{4})(?:-(?P<month>\d{1,2}))?(?:-(?P<day>\d{1,2}))?$")


class PartialDate(date):
    __slots__ = "_year", "_month", "_day", "_precision"

    YEAR = 0
    MONTH = 1
    DAY = 2

    DATE_FORMATS = {YEAR: "%Y", MONTH: "%Y-%m", DAY: "%Y-%m-%d"}

    def __new__(cls, year, month=None, day=None):
        if isinstance(year, str) and (result := partial_date_re.match(year)):
            year = int(result.group("year"))
            if result.group("month"):
                month = int(result.group("month"))
            if result.group("day"):
                day = int(result.group("day"))

        self = date.__new__(cls, year, month or 1, day or 1)
        self._precision = self.DAY if day else self.MONTH if month else self.YEAR
        return self

    def __repr__(self):
        return self.strftime(self.DATE_FORMATS[self._precision])

    @property
    def precision(self):
        """precision (0-2)"""
        return self._precision

    @setter
    def month(self):
        """month (1-12)"""
        return self._month


x = PartialDate("2021-04")

y = PartialDate.today()

z = PartialDate(2021)


x = 9
