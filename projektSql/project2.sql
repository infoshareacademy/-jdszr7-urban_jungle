create table if not exists team2player2match (player_api_id integer, team_api_id integer, match_id integer);


insert into team2player2match
select p.player_api_id, m.home_team_api_id, m.id from "Match" m
left join Player p on p.player_api_id
in (m.home_player_1,
	m.home_player_2,
	m.home_player_3,
	m.home_player_4,
	m.home_player_5,
	m.home_player_6,
	m.home_player_7,
	m.home_player_8,
	m.home_player_9,
	m.home_player_10,
	m.home_player_11)
where m.home_player_1 is not null
	and m.home_player_2 is not null
	and m.home_player_3 is not null
	and m.home_player_4 is not null
	and m.home_player_5 is not null
	and m.home_player_6 is not null
	and m.home_player_7 is not null
	and m.home_player_8 is not null
	and m.home_player_9 is not null
	and m.home_player_10 is not null
	and m.home_player_11 is not null
	and m.away_player_1 is not null
	and m.away_player_2 is not null
	and m.away_player_3 is not null
	and m.away_player_4 is not null
	and m.away_player_5 is not null
	and m.away_player_6 is not null
	and m.away_player_7 is not null
	and m.away_player_8 is not null
	and m.away_player_9 is not null
	and m.home_player_10 is not null
	and m.away_player_11 is not null;


insert into team2player2match
select p.player_api_id, m.away_team_api_id, m.id from "Match" m
left join Player p on p.player_api_id
in (m.away_player_1,
	m.away_player_2,
	m.away_player_3,
	m.away_player_4,
	m.away_player_5,
	m.away_player_6,
	m.away_player_7,
	m.away_player_8,
	m.away_player_9,
	m.away_player_10,
	m.away_player_11)
where m.home_player_1 is not null
	and m.home_player_2 is not null
	and m.home_player_3 is not null
	and m.home_player_4 is not null
	and m.home_player_5 is not null
	and m.home_player_6 is not null
	and m.home_player_7 is not null
	and m.home_player_8 is not null
	and m.home_player_9 is not null
	and m.home_player_10 is not null
	and m.home_player_11 is not null
	and m.away_player_1 is not null
	and m.away_player_2 is not null
	and m.away_player_3 is not null
	and m.away_player_4 is not null
	and m.away_player_5 is not null
	and m.away_player_6 is not null
	and m.away_player_7 is not null
	and m.away_player_8 is not null
	and m.away_player_9 is not null
	and m.home_player_10 is not null
	and m.away_player_11 is not null;


create table if not exists season_summary(league_name text, season text, team_long_name text, avg_team_rating_pro_season numeric, last_season_rating numeric, points_in_season integer, points_in_last_season integer);

insert into season_summary
select league_name, season, team_long_name, avg_team_rating_pro_season, last_season_rating, points_in_season, points_in_last_season
from(
with overall_rating_per_season as
(
select
	l.name league_name,
	m.season,
	t.team_api_id,
	t.team_long_name,
	avg(pa.overall_rating) team_avg_rating
from team2player2match tpm
left join Player_Attributes pa on tpm.player_api_id = pa.player_api_id
inner join "Match" m on m.id = tpm.match_id
inner join team t on t.team_api_id = tpm.team_api_id
inner join League l on l.id = m.league_id
where strftime('%Y', m.date) = strftime('%Y', pa.date)
group by l.name, tpm.team_api_id, m.season
order by l.name, t.team_short_name, m.season
),
home_team_season_points as
(
select
	m.home_team_api_id,
	m.season,
	sum(case
		when m.home_team_goal > m.away_team_goal then 3
		when m.home_team_goal = m.away_team_goal then 1
		else 0
	end) as home_team_points_in_season
from "Match" m
group by m.season, m.home_team_api_id
),
away_team_season_points as
(
select
	m.away_team_api_id ,
	m.season,
	sum(case
		when m.away_team_goal > m.home_team_goal then 3
		when m.away_team_goal = m.home_team_goal then 1
		else 0
	end) as away_team_points_in_season
from "Match" m
group by m.season, m.away_team_api_id
)
select
	league_name,
	overall_rating_per_season.season,
	overall_rating_per_season.team_long_name,
	ROUND(overall_rating_per_season.team_avg_rating,2) avg_team_rating_pro_season,
	lag(ROUND(overall_rating_per_season.team_avg_rating,2),1) over (partition by league_name, overall_rating_per_season.team_long_name order by overall_rating_per_season.season) last_season_rating,
	home_team_points_in_season + away_team_points_in_season points_in_season,
	lag(home_team_points_in_season + away_team_points_in_season, 1) over (partition by league_name, overall_rating_per_season.team_long_name order by overall_rating_per_season.season) points_in_last_season
from overall_rating_per_season
join home_team_season_points on home_team_season_points.home_team_api_id = overall_rating_per_season.team_api_id and home_team_season_points.season = overall_rating_per_season.season
join away_team_season_points on away_team_season_points.away_team_api_id = overall_rating_per_season.team_api_id and away_team_season_points.season = overall_rating_per_season.season
order by overall_rating_per_season.league_name, overall_rating_per_season.team_long_name, overall_rating_per_season.season);

select "rating_increases_points_increases" as "result", count(*) as liczba_rezultatow
from season_summary ss
where avg_team_rating_pro_season > ss.last_season_rating and points_in_season > points_in_last_season
UNION 
select "rating_increases_points_decreases" as "result", count(*) as liczba_rezultatow
from season_summary ss
where avg_team_rating_pro_season > ss.last_season_rating and points_in_season < points_in_last_season
UNION
select "rating_decreases_points_increases" as "result", count(*) as liczba_rezultatow
from season_summary ss
where avg_team_rating_pro_season < ss.last_season_rating and points_in_season > points_in_last_season
UNION
select "rating_decreases_points_decreases" as "result", count(*) as liczba_rezultatow
from season_summary ss
where avg_team_rating_pro_season < ss.last_season_rating and points_in_season < points_in_last_season



