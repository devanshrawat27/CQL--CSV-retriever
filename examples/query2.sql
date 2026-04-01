SELECT department, COUNT(*) as employee_count, AVG(salary) as avg_salary
FROM employees.csv
GROUP BY department
ORDER BY avg_salary DESC
