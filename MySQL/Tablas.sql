create database seven_and_half;

use seven_and_half;

create table if not exists player(
	player_id VARCHAR(25) primary key,
    player_name VARCHAR(40) not NULL,
	player_risk TINYINT not NULL,
	human TINYINT(1) not NULL);
    
create table if not exists deck(
	deck_id CHAR(3) primary key,
	deck_name VARCHAR(25) not NULL);
    
create table if not exists cardgame(
	cardgame_id INT auto_increment primary key,
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
    
