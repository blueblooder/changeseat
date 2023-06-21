In MS SQL Server 2019, you can use the `DATEPART()` function and a `CASE` statement within a subquery to achieve the same result as the PostgreSQL syntax you provided:

```
SELECT SUM(CASE WHEN DATEPART(WEEKDAY, d) BETWEEN 2 AND 6 THEN 1 ELSE 0 END) AS month_working_days
FROM (
    SELECT CAST(DATEADD(DAY, number, DATEFROMPARTS(YEAR(GETDATE()), MONTH(GETDATE()), 1)) AS DATE) AS d
    FROM master..spt_values
    WHERE type = 'P'
    AND number <= DATEDIFF(DAY, DATEFROMPARTS(YEAR(GETDATE()), MONTH(GETDATE()), 1), GETDATE())
) AS x
```

This first generates a series of dates for the current month using a subquery. The `DATEFROMPARTS()` function is used to retrieve the year and month of the current date, and the `master..spt_values` table is used to generate a series of numbers from 0 to the number of days in the current month. The `DATEADD()` function is used to add each number to the first day of the current month to generate a series of dates.

The subquery then calculates the number of working days for the current month by using a `CASE` statement within the `SUM()` function. The `DATEPART()` function is used to retrieve the day of the week for each date in the series, and the `CASE` statement checks if the day of the week is between Monday and Friday (represented as 2-6 in SQL Server), and if so, returns 1. Otherwise, it returns 0.

Note that in SQL Server, the `master..spt_values` table is a system table that can be used for generating a series of numbers. Also, the `::int` syntax used in PostgreSQL to cast a boolean value to an integer is not needed in SQL Server, as the `CASE` statement already returns an integer value.
