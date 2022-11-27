class Match{
        constructor(team_one, team_two, winner = null) {
            this.team_one = team_one;
            this.team_two = team_two;
            this.winner = winner;
            this.score_one = 0;
            this.score_two = 0;
            this.round = null;
        }

        static get TEAM_ONE(){
            return "RED";
        }
        static get TEAM_TWO(){
            return "BLUE";
        }
        static get TIE(){
            return "TIE";
        }
        getWinner(){
            return this.winner;
        }
        setWinner(winner){
            this.winner = winner;
        }
        setWinnerByScore(){
            if(this.score_one == this.score_two){
                return Match.TIE
            }else if(this.score_one > this.score_two){
                return Match.TEAM_ONE
            }else if(this.score_two > this.score_one){
                return Match.TEAM_TWO
            }
        }
        matchEnded(){
            return this.winner !== null;
        }
        static emptyMatch(){
            return new Match(null, null);
        }

     }

    //[ ----------------- Bracket class -------------------- ]
    class Bracket{
        constructor(team_list) {
            this.rounds_cnt = Bracket.getRoundsCnt((team_list).length);
            this.rounds_list = Bracket.generateStartingBracket(team_list);
            this.team_list = team_list;
            this.current_round = 1;
            this.bracket_completed = false;
        }

        // ----------   Interface with bracket -----------------
        getUncompletedMatchesForRound(current_round){
            var matches = this.rounds_list[current_round - 1];

            var uncompleted_matches = matches.map(function(match, index){
                var the_match = match;
                the_match.match_index = index;
                return the_match;
            }).filter(function (match){
                return match.matchEnded();
            })
            return uncompleted_matches;
        }
        getUncompletedMatchesForCurrentRound(){
            var uncompleted_matches = this.getUncompletedMatchesForRound(this.current_round);
            if(uncompleted_matches.length > 0){
                var random_match = uncompleted_matches[Math.floor(Math.random()*uncompleted_matches.length)];
                return random_match;
            }else{
                return null;
            }
        }

        getRoundCompleted(current_round){
            var uncopleted_matches = this.getUncompletedMatchesForRound(current_round);
            return (uncopleted_matches.length === 0);
        }

        currentRoundCompleted(){
            return (this.getRoundCompleted(this.current_round));
        }

        startNextRound(){
            if(this.current_round != this.rounds_cnt){
                this.generateNewRound();
                this.current_round += 1;
            }else{
                this.bracket_completed = this.bracketEnded();
            }
        }

        generateNewRound(){
            var matches = this.rounds_list[this.current_round - 1];
            let that = this;
            var winners = matches.map(function (match){
                var winner = match.getWinner();
                return winner;
            })
            var winners_left = winners.slice(0).reverse();
            var next_round_mathces = this.rounds_list[this.current_round].slice(0);
            var updated_mathces = next_round_mathces.map(function (match){
                var team_one;
                var team_two;
                if(winners_left.length >= 2){
                    team_one = winners_left.pop();
                    team_two = winners_left.pop();
                }else{
                    team_one = winners_left.pop();
                    team_two = null;
                }
                var match = new Match(team_one, team_two);
                return match;
            })

            this.rounds_list[this.current_round] = updated_mathces;
        }

        bracketEnded(){
            var bracket_ended = true;
            for(var i = 0; i < this.rounds_cnt; i++){
                var rounds_completed = this.getRoundCompleted(i + 1);
                if(rounds_completed == false){
                    bracket_ended == false;
                }else{
                    continue;
                }
            }
            return bracket_ended;
        }

        getBracketWinner(){
            if(this.bracket_completed){
                var final_round = this.rounds_list[this.rounds_cnt - 1];
                var winner = final_round[0].getWinner();
                return winner;
            }else{
                return undefined;
            }
        }

        // ----------------------

        static generateStartingBracket(team_list){
            var amnt_of_teams = team_list.length;
            var round_cnt = Bracket.getRoundsCnt(amnt_of_teams);
            var empty_rounds = Bracket.generateEmptyBracket(amnt_of_teams, round_cnt);
            var starting_rounds = empty_rounds.slice(0);
            var teams_left = team_list.slice(0).reverse();

            for(var i = 0; i < starting_rounds[0].length; i++){
                var team_one;
                var team_two;

                if(teams_left.length >= 2){
                    team_one = teams_left.pop();
                    team_two = teams_left.pop();
                }else{
                    team_one = teams_left.pop();
                    team_two = null;
                }
                var match = new Match(team_one, team_two);
                starting_rounds[0][i] = match;
             }
            return starting_rounds;
        }

        static generateEmptyBracket(amnt_of_teams, round_cnt){
            var rounds = [];
            var matches_for_round_amnt;
            var aux = Math.pow(2, round_cnt); // rc = 4, aux = 16 || rc = 3, aux = 8 || rc = 2, aux = 4
            // 12 / 2 = 6
            // 3 / 2 = 2
            // 5 / 2 = 3
            // 7 / 2 = 4

            if(round_cnt === 1){
                var empty_matches = Bracket.generateEmptyMatches(1);
                rounds.push(empty_matches);
            }else{
                for(var i = 0; i < round_cnt; i++){
                    // matches_for_round_amnt = Math.pow(2, round_cnt - (1 + i));
                    amnt_of_teams = Math.ceil(amnt_of_teams / 2);
                    matches_for_round_amnt = amnt_of_teams;

                    var empty_matches = Bracket.generateEmptyMatches(matches_for_round_amnt);
                    rounds.push(empty_matches);
                }
            }

            return rounds;
        }

        static generateEmptyMatches(amnt_of_matches){
            var empty_matches = [];
            for(var i = 0; i < amnt_of_matches; i++){
                empty_matches.push(Match.emptyMatch());
            }
            return empty_matches;
        }

        static getRoundsCnt(amnt_of_teams){
            var round_cnt = Math.ceil(Math.log(amnt_of_teams) / Math.log(2));
            return round_cnt;
        }
     }