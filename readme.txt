In MS SQL Server 2019, you can use the `DATEFROMPARTS()` function and the `EOMONTH()` function to achieve the same result as the PostgreSQL syntax you provided:

```
SELECT DATEFROMPARTS(YEAR(EOMONTH(GETDATE(), -2)), MONTH(EOMONTH(GETDATE(), -2)), 1) AS month_start
```

This first uses the `EOMONTH()` function to retrieve the last day of the previous month, and then subtracts one month from that date. The `YEAR()` and `MONTH()` functions are used to retrieve the year and month of the resulting date, and the `DATEFROMPARTS()` function is used to construct a new date from the year, month, and day 1.

Note that the `EOMONTH()` function is used with a negative offset of 2, which means that it returns the last day of the month that is two months before the current month. This corresponds to the last day of the previous month.

I hope this helps!
