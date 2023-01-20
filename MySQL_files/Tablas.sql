create database seven_and_half;

use seven_and_half;

# TABLE PLAYERS
create table if not exists player(
	player_id VARCHAR(25) primary key,
    player_name VARCHAR(40) not NULL,
	player_risk TINYINT not NULL,
	human TINYINT(1) not NULL);

# TABLE DECK
create table if not exists deck(
	deck_id CHAR(3) primary key,
	deck_name VARCHAR(25) not NULL);

# TABLE CARDGAME
create table if not exists cardgame(
	cardgame_id INT primary key,
	players TINYINT not NULL,
	rounds TINYINT not NULL,
	start_hour DATETIME not NULL,
	end_hour DATETIME not NULL,
	deck_id CHAR(3) not NULL,
    constraint fk_deck_id
	foreign key(deck_id)
		references deck(deck_id)
		on update cascade
		on delete cascade);

# TABLE PLAYER_GAME
create table if not exists player_game(
	cardgame_id INT not NULL,
    constraint fk_cardgame_id
    foreign key(cardgame_id)
		references cardgame(cardgame_id)
        on update cascade
        on delete cascade,
    player_id VARCHAR(25) not NULL,
    constraint fk_player_id
    foreign key(player_id)
		references player(player_id)
        on update cascade
        on delete cascade,
	initial_card_id CHAR(3) not NULL,
	starting_points TINYINT not NULL,
	ending_points TINYINT not NULL,
    primary key(cardgame_id, player_id));

# TABLE PLAYER_GAME_ROUND
create table if not exists player_game_round(
	cardgame_id INT not NULL,
    constraint fk_cardgame_id_PGR
    foreign key(cardgame_id)
		references cardgame(cardgame_id)
        on update cascade
        on delete cascade,

	round_num TINYINT not NULL,

	player_id VARCHAR(25) not NULL,
    constraint fk_player_id_PGR
    foreign key(player_id)
		references player(player_id)
        on update cascade
        on delete cascade,

	is_bank TINYINT(1) not NULL,
	bet_points TINYINT not NULL,
	cards_value DECIMAL(4,1) not NULL,
	starting_round_points TINYINT not NULL,
	ending_round_points TINYINT,
    primary key (cardgame_id, round_num, player_id));

# TABLE CARD
create table if not exists card(
    card_id CHAR(3) not NULL,
	card_name VARCHAR(25) not NULL,
	card_value DECIMAL(3,1) not NULL,
	card_priority TINYINT not NULL,
	card_real_value TINYINT not NULL,
	deck_id CHAR(3) not NULL,
    constraint fk_deck_id_C
    foreign key(deck_id)
		references deck(deck_id)
        on update cascade
        on delete cascade,
	primary key(card_id, deck_id));

# VIEW
create view player_earnings as
select p.player_id, sum(p.ending_points), count(p.player_id), sum(TIMESTAMPDIFF(MINUTE, c.start_hour, c.end_hour))
from player_game p
join cardgame c
on c.cardgame_id = p.cardgame_id
group by p.player_id;



# INFORME 7
select pb.cardgame_id, count(pb.player_id)
from (select player_id, cardgame_id
	  from player_game_round
      where is_bank = 1
      group by player_id, cardgame_id) as pb
group by cardgame_id;

# INFORME 8
select pb.cardgame_id, avg(pb.bet_points)
from (select cardgame_id, bet_points
	from player_game_round) as pb
group by pb.cardgame_id;

# INFORME 9
select ab.cardgame_id, avg(ab.bet_points)
from (select cardgame_id, bet_points
	  from player_game_round
	  where round_num = 1 and bet_points is not NULL) as ab
group by ab.cardgame_id;

# INFORME 10
select p.cardgame_id, avg(p.bet_points)
from (select cardgame_id, max(round_num) as last_round
	  from player_game_round
	  group by cardgame_id) as ab,
	 player_game_round p
where p.cardgame_id = ab.cardgame_id and
	  round_num = ab.last_round
group by p.cardgame_id;

# INFORME 3
select lb.cardgame_id, p.player_id, lb.min_bet
from (select cardgame_id, min(bet_points) as min_bet
	  from player_game_round
	  where bet_points is not null
	  group by cardgame_id) as lb,
	 player_game_round p
where p.cardgame_id = lb.cardgame_id and
	  p.bet_points = lb.min_bet;

# INFORME 5
select pg.cardgame_id, w.win_pts, pg.player_id
from (select cardgame_id, max(ending_points) as win_pts
	  from player_game
	  group by cardgame_id) as w,
	 player_game pg,
     player p
where pg.cardgame_id = w.cardgame_id and
	  p.player_id = pg.player_id and
      pg.ending_points = w.win_pts and
      p.human = 0;

# INFORME 2
select lb.cardgame_id, p.player_id, lb.max_bet
from (select cardgame_id, max(bet_points) as max_bet
	  from player_game_round
	  where bet_points is not null
	  group by cardgame_id) as lb,
	 player_game_round p
where p.cardgame_id = lb.cardgame_id and
	  p.bet_points = lb.max_bet;