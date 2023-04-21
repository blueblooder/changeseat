SELECT (CURRENT_DATE - (EXTRACT(DOW FROM CURRENT_DATE)::int + 6) % 7 - 2)::date AS last_weekday;
