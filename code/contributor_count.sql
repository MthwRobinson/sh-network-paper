SELECT MAX(package_count)
FROM(
	SELECT COUNT(DISTINCT(package_id)) as package_count, user_id
	 FROM (
		SELECT package_id, a.user_id, a.issue_id, commit_pct
		FROM open_source.issue_contributors a
		INNER JOIN open_source.issue_comments b
		 ON (a.issue_id = b.issue_id)
		 WHERE commit_pct > 0
	) x
	GROUP BY user_id
) y
WHERE package_count >= 5

-- Submitted Requirements
-- Total: 26611
-- Multi: 1954
-- Over 10: 5

-- Committed Code
-- Total: 5607
-- Multi: 390
-- Max: 9
			
