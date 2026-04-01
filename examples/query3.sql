SELECT department, SUM(salary) as total_salary, COUNT(*) as num_employees
FROM employees.csv
WHERE age < 40
GROUP BY department
HAVING COUNT(*) >= 2
ORDER BY total_salary DESC
