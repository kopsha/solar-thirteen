from dataclasses import dataclass
from datetime import date, timedelta
from enum import Enum


class Sol13Month(Enum):
    AURORA = 0
    JANUS = 1
    FEBRUA = 2
    MARS = 3
    APRILIS = 4
    MAIUS = 5
    IUNIUS = 6
    SOLIS = 7
    IULIUS = 8
    AUGUSTUS = 9
    SEPTEMBER = 10
    OCTOBER = 11
    NOVEMBER = 12
    DECEMBER = 13
    HELIAD = 14


class Sol13Weekday(Enum):
    LUNAE = 1
    MARTIS = 2
    MERCURII = 3
    IOVIS = 4
    VENERIS = 5
    SATURNI = 6
    DOMINICUS = 7


@dataclass
class Sol13Date:
    year: int
    ordinal: int
    gregorian_ref = date(2025, 12, 21)
    EPOCH_YEAR = 2026
    FIRST_LEAP_YEAR = 2028

    @staticmethod
    def is_leap_year(year):
        """Determine whether a year is a leap year."""
        return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)

    @property
    def month(self):
        return Sol13Month((self.ordinal - 1) // 28 + 1)

    @property
    def day(self):
        return (self.ordinal - bool(self.ordinal)) % 28 + 1

    def isoformat(self):
        parts = [f"{self.year:4}", f"{self.month.value:02}", f"{self.day:02}"]
        return ".".join(parts)

    def format(self):
        return f"{self.month.name.title()} {self.day:02}, {self.year:4}"

    def __str__(self):
        return self.format()

    def as_gregorian(self):
        assert self.year >= self.EPOCH_YEAR

        days_since_epoch = (self.year - self.EPOCH_YEAR) * 365
        days_since_epoch += sum(
            self.is_leap_year(yi) for yi in range(self.FIRST_LEAP_YEAR, self.year, 4)
        )

        days_since_epoch += self.ordinal
        return self.gregorian_ref + timedelta(days=days_since_epoch)


class Sol13Calendar:
    weekdays_header = ["# ", *(wd.name.title() for wd in Sol13Weekday)]

    def format_month_line(self, year, month, width):
        mo = Sol13Month(month)
        text = f"{mo.name.title()} {year}"
        return text.center(width)

    def format_weekday_line(self, col_width, spacing):
        separator = " " * spacing
        return separator.join(
            f"{name[:col_width]:>{col_width}}" for name in self.weekdays_header
        )

    def format_week_line(self, week_no, col_width=2, spacing=1):
        start = 1 + ((week_no - 1) % 4) * 7
        separator = " " * spacing
        values = [f"{week_no:{col_width - 1}})"]
        values.extend(f"{day:{col_width}}" for day in range(start, start + 7))
        return separator.join(values)

    def format_calendar_month(self, sol13date, col_width=3, spacing=1):
        year, month = sol13date.year, sol13date.month.value
        col_width = max(2, col_width)
        spacing = max(1, spacing)
        width = 7 * (col_width + 1) - 1

        lines = [self.format_month_line(year, month, width)]
        if month not in {0, 14}:
            lines.append(self.format_weekday_line(col_width, spacing))
            start = 1 + (month - 1) * 4
            lines.extend(
                self.format_week_line(wi, col_width) for wi in range(start, start + 4)
            )

        return lines

    def iter_days(self, year):
        yield Sol13Date(year, 0)

        for ordinal in range(1, 365):
            yield Sol13Date(year, ordinal)

        if Sol13Date.is_leap_year(year):
            yield Sol13Date(year, 365)

    def iter_weeks(self, year):
        yield Sol13Date(year, 0)

        for ordinal in range(0, 52):
            yield Sol13Date(year, 1 + ordinal * 7)

        if Sol13Date.is_leap_year(year):
            yield Sol13Date(year, 365)

    def iter_months(self, year):
        yield Sol13Date(year, 0)

        for mo in range(0, 13):
            yield Sol13Date(year, mo * 28 + 1)

        if Sol13Date.is_leap_year(year):
            yield Sol13Date(year, 365)


def main():
    print("Whole year simulation.")
    print()

    s13 = Sol13Calendar()

    for mo in s13.iter_months(2026):
        first, *lines = s13.format_calendar_month(mo)
        print("***", mo, "->", mo.as_gregorian().strftime("%a, %d %b %Y"))
        print(first)
        print(*lines, sep="\n")
        print()

    for mo in s13.iter_months(2027):
        first, *lines = s13.format_calendar_month(mo)
        print("***", mo, "->", mo.as_gregorian().strftime("%a, %d %b %Y"))
        print(first)
        print(*lines, sep="\n")
        print()

    for mo in s13.iter_months(2028):
        first, *lines = s13.format_calendar_month(mo)
        print("***", mo, "->", mo.as_gregorian().strftime("%a, %d %b %Y"))
        print(first)
        print(*lines, sep="\n")
        print()


if __name__ == "__main__":
    main()
