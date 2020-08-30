-- This script was used to count the number of connector nodes who were also contributors
SELECT COUNT(*) AS commit_and_central
FROM open_source.issue_contributors a
INNER JOIN (
	SELECT id as package_id, package_name as package, org_name as organization
	FROM open_source.packages 
) b
on a.package_id = b.package_id
INNER JOIN open_source.network_centrality c
ON (c.package = b.package) AND (c.organization = b.organization) and (a.user_id = c.user_id)
WHERE commit = 0 and  betweenness_centrality > 0.01

-- 0 Threshold
-- Central - 85,775
-- Central and Committed - 69,800

-- Not Central - 37,975
-- Not Central and Committed - 7,517


-- 0.01 Threshold

-- Central - 60,923
-- Central and Committed - 58,282

-- Not Central - 62,284
-- Not Central and Committed - 19,069
