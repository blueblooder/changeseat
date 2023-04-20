好的，如果您希望開始日期始終為當月的第一天，而結束日期為當前日期，可以使用 GETDATE 函數和 DATEADD 函數來計算這兩個值，如下所示：

SELECT (DATEDIFF(DAY, DATEADD(MONTH, DATEDIFF(MONTH, 0, GETDATE()), 0), GETDATE()) + 1)
       - (DATEDIFF(WEEK, DATEADD(MONTH, DATEDIFF(MONTH, 0, GETDATE()), 0), GETDATE()) * 2)
       - (CASE WHEN DATEPART(WEEKDAY, DATEADD(MONTH, DATEDIFF(MONTH, 0, GETDATE()), 0)) = 1 THEN 1 ELSE 0 END)
       - (CASE WHEN DATEPART(WEEKDAY, GETDATE()) = 7 THEN 1 ELSE 0 END)
       AS WorkingDays;
這個查詢使用 GETDATE 函數獲取當前日期，然後使用 DATEADD 和 DATEDIFF 函數計算當月的第一天。接下來，它使用與前面的查詢相同的方法來計算工作日天數。
