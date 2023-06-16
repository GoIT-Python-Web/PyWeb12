SELECT s.fullname, ROUND(AVG(g.grade), 2) as avg_grade
FROM grades g 
LEFT JOIN students s ON s.id = g.student_id 
GROUP BY s.id
ORDER BY avg_grade DESC
LIMIT 5;

SELECT sbj.name, s.fullname, ROUND(AVG(g.grade), 2) as avg_grade
FROM grades g 
LEFT JOIN students s ON s.id = g.student_id 
LEFT JOIN subjects sbj ON sbj.id = g.subject_id 
WHERE sbj.id = 4
GROUP BY s.id
ORDER BY avg_grade DESC
LIMIT 1;