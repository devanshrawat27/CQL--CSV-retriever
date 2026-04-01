SELECT name, age, salary
FROM employees.csv
WHERE age > 30 AND department = 'Engineering'
ORDER BY salary DESC
