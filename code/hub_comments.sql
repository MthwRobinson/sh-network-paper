SELECT count(*)
FROM(
 	SELECT DISTINCT x.user_id, x.organization, x.package, EXTRACT(DAY FROM '2019-01-01' - max_issue) as retention_time, betweenness_centrality
    FROM(
        SELECT organization, package, user_id, MAX(created_at) as  max_issue, MIN(created_at) as min_issue
        FROM open_source.comments
        WHERE created_at < '2019-01-01'
        group by organization, package, user_id
    ) x
	INNER JOIN (
		SELECT *	
		FROM open_source.network_centrality 
		WHERE betweenness_centrality > 0.01
	) b
	ON (x.organization = b.organization) and (x.package = b.package) and (x.user_id = b.user_id)
) y
-- WHERE retention_time < 365
-- 1630 / 2001
-- 3950 / 6147
