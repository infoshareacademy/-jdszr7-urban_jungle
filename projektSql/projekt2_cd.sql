Soccer - Niezast¹pieni pi³karze - Czy s¹ pi³karze, bez których ich dru¿yny sobie nie radz¹ 
- czyli ciekawe pi³karskie statystyki, œwietne do popisu erudycji dla komentatorów

-- Liczba goli zdobytych i straconych w sezonie


SELECT t.team_long_name AS Home_Team,t2.team_long_name AS Away_Team, m.season as Season, c.name as Country , SUM(m.home_team_goal) AS 'Home Goal', 
SUM(m.away_team_goal) AS 'Away Goal'
FROM Match AS m LEFT JOIN Team AS t 
ON m.home_team_api_id = t.team_api_id 
LEFT JOIN Team AS t2 ON m.away_team_api_id = t2.team_api_id
JOIN Country as c ON c.id=m.Country_id
GROUP BY Home_Team,Away_Team, Season, Country 
ORDER BY Home_Team,Away_Team, Country 



-- Liczba zwyciêstw, pora¿ek i remisów

SELECT c.name AS Country, m.season AS Season, t.team_long_name AS Home_Team, t2.team_long_name AS Away_Team,
COUNT(CASE WHEN m.home_team_goal > away_team_goal THEN "Won" END) AS Won,
COUNT(CASE WHEN m.home_team_goal < away_team_goal THEN "Lost" END) AS Lost,
COUNT(CASE WHEN m.home_team_goal = away_team_goal THEN "Tie" END) AS Tie
FROM Match AS m
LEFT JOIN Country AS c ON m.country_id = c.id
LEFT JOIN Team as t ON m.home_team_api_id = t.team_api_id
LEFT JOIN Team AS t2 ON m.away_team_api_id = t2.team_api_id
GROUP BY Country, Home_Team, Away_Team
ORDER BY Country
                
-- Stosunek % zwyciêstw, pora¿ek i remisów do liczby rozegranych meczów


SELECT a.Home_Team, a.Away_Team , a.Season , a.Won, a.Lost , a.Tie, sum(Won+Lost+Tie) as sum_matches, 100.0 * Won/ (sum(Won+Lost+Tie) )  as proc_Won, 
100.0 * Lost/ (sum(Won+Lost+Tie) )  as proc_Lost,100.0 * Tie/ (sum(Won+Lost+Tie) )  as proc_Tie
from
(SELECT c.name AS Country, m.season AS Season, t.team_long_name AS Home_Team, t2.team_long_name as Away_Team ,
COUNT(CASE WHEN m.home_team_goal > away_team_goal THEN 1 END) AS Won,
COUNT(CASE WHEN m.home_team_goal < away_team_goal THEN 2 END) AS Lost,
COUNT(CASE WHEN m.home_team_goal = away_team_goal THEN 3 END) AS Tie
FROM Match AS m
LEFT JOIN Country AS c ON m.country_id = c.id
LEFT JOIN Team as t ON m.home_team_api_id = t.team_api_id
LEFT JOIN Team AS t2 ON m.away_team_api_id = t2.team_api_id
GROUP BY Country, Home_Team, Away_Team 
ORDER BY Country) a group by a.Home_Team, a.Away_Team , a.Season , a.Won, a.Lost , a.Tie;


