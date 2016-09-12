#! /usr/bin/python

'''
Created: 
Author: Tuck Williamson

Copyright© T.H.W LLC 2016
Based on the wonderful work behind poke.isitin.org
'''
from pokemonData import *
from math import floor, sqrt, sin, cos, pow, pi

def polarToCartesian(centerX,centerY,radius,angleInDegrees):
	
  angleInRadians = (angleInDegrees + 90) * pi / 180.0

  return (round(centerX + (radius * cos(angleInRadians))),
    round(centerY + (radius * sin(angleInRadians))))

def getPossibleArcPoints(trainer_level):
  return [90 + ((CpM[i]-0.094)*202.037116/CpM[trainer_level*2-2]) for i in range(0, min((trainer_level) * 2 + 2, 79))]

ind_attack = 7
ind_defense = 7
ind_stamina = 7

good_against = {}
bad_against = {}
resistance = {}

def ratePokemon(trainer_level, pokemon_level, pk_id, user_cp, user_hp):

  return_info = {}
  
  #Use this to verify pokemon_level
  pokemon_level_slider_max = min(parseInt(trainer_level) + 1.5, 40)
  
  min_cp = max(floor(pokemon[pk_id].BaseAttack * sqrt(pokemon[pk_id].BaseDefense) * sqrt(pokemon[pk_id].BaseStamina) * pow(CpM[pokemon_level*2-2], 2) / 10), 10)
  max_cp = max(floor((pokemon[pk_id].BaseAttack+15) * sqrt(pokemon[pk_id].BaseDefense+15) * sqrt(pokemon[pk_id].BaseStamina+15) * pow(CpM[pokemon_level*2-2], 2) / 10), 10)
  
  
  return_info["min_cp"] = min_cp
  return_info["max_cp"] = max_cp
  return_info["cp_rank"] = pokemon[pk_id]["CP Rank"]
  return_info["cp_norm"] = ((pokemon[pk_id]["CP Normalised"] - 1)*100)

  min_hp = max(floor((pokemon[pk_id].BaseStamina) * CpM[pokemon_level*2-2]), 10)
  max_hp = max(floor((pokemon[pk_id].BaseStamina+15) * CpM[pokemon_level*2-2]), 10)
  return_info["min_hp"] = min_hp
  return_info["max_hp"] = max_hp
  return_info["hp_rank"] = pokemon[pk_id]["HP Rank"]
  return_info["hp_norm"] = ((pokemon[pk_id]["HP Normalised"] - 1)*100)

  total_attack = pokemon[pk_id].BaseAttack + ind_attack
  total_defense = pokemon[pk_id].BaseDefense + ind_defense
  total_stamina = pokemon[pk_id].BaseStamina + ind_stamina

  calc_cp = total_attack * sqrt(total_defense) * sqrt(total_stamina) * pow(CpM[pokemon_level*2-2], 2) / 10
  rounded_calc_cp = max(floor(calc_cp), 10)
  return_info["calc_cp"] = calc_cp
  return_info["rounded_calc_cp"] = rounded_calc_cp

  calc_hp = total_stamina * CpM[pokemon_level*2-2]
  rounded_calc_hp = max(floor(calc_hp), 10)
  return_info["calc_hp"] = calc_hp.toPrecision(5)
  return_info["rounded_calc_hp"] = rounded_calc_hp

  min_est_total_stamina = (user_hp) / CpM[pokemon_level*2-2]
  est_total_stamina = (user_hp + 0.5) / CpM[pokemon_level*2-2]
  max_est_total_stamina = (user_hp + 1) / CpM[pokemon_level*2-2]
  
  min_br_cp = max(max(floor(pokemon[pk_id].BaseAttack * sqrt(pokemon[pk_id].BaseDefense) * sqrt(min_est_total_stamina) * pow(CpM[pokemon_level*2-2], 2) / 10), 10), min_cp)
  
  max_br_cp = min(max(floor((pokemon[pk_id].BaseAttack + 15) * sqrt(pokemon[pk_id].BaseDefense + 15) * sqrt(max_est_total_stamina) * pow(CpM[pokemon_level*2-2], 2) / 10), 10), max_cp)
  
  per_diff_cp = (-1 + (user_cp+0.5) / ((pokemon[pk_id].BaseAttack + 7.5) * sqrt(pokemon[pk_id].BaseDefense + 7.5) * sqrt(pokemon[pk_id].BaseStamina + 7.5) * pow(CpM[pokemon_level*2-2], 2) / 10)) * 100
  
  per_diff_sta = (-1 + (user_hp+0.5) / ((pokemon[pk_id].BaseStamina + 7.5) * CpM[pokemon_level*2-2])) * 100
  
  per_diff_br = (-1 + (user_cp+0.5) / ((pokemon[pk_id].BaseAttack + 7.5) * sqrt(pokemon[pk_id].BaseDefense + 7.5) * sqrt(est_total_stamina) * pow(CpM[pokemon_level*2-2], 2) / 10)) * 100
  
  return_info["cp_rating"] = (user_cp - min_cp) / (max_cp - min_cp) * 100;
  return_info["hp_rating"] = (user_hp - min_hp) / (max_hp - min_hp) * 100;
  return_info["br_rating"] = (user_cp - min_br_cp) / (max_br_cp - min_br_cp) * 100


types_symbol_lookup = {
"Normal": 6,
"Fighting": 9,
"Flying": 3,
"Poison": 1,
"Ground": 8,
"Rock": 11,
"Bug": 5,
"Ghost": 14,
"Steel": 12,
"Fire": 2,
"Water": 4,
"Grass": 0,
"Electric": 7,
"Psychic": 10,
"Ice": 13,
"Dragon": 15,
"Dark": 16,
"Fairy": 17
}

types_text_lookup = {
"Normal": "black",
"Fighting": "black",
"Flying": "black",
"Poison": "black",
"Ground": "black",
"Rock": "black",
"Bug": "black",
"Ghost": "black",
"Steel": "black",
"Fire": "black",
"Water": "black",
"Grass": "black",
"Electric": "black",
"Psychic": "black",
"Ice": "black",
"Dragon": "white",
"Dark": "black",
"Fairy": "black"
}

'''
def bestGuess() {
  var stamina;
  for (stamina = 0; stamina < 16; stamina++) {
    if (floor((pokemon[pk_id].BaseStamina + stamina) * CpM[pokemon_level*2-2]) == user_hp) {
      break;
    }
  }
  possible_attacks = [];
  possible_defenses = [];
  for (var attack = 0; attack < 16; attack++) {
    for (var defense = 0; defense < 16; defense++) {
      if (max(floor((pokemon[pk_id].BaseAttack + attack)*sqrt(pokemon[pk_id].BaseDefense + defense)*sqrt(pokemon[pk_id].BaseStamina + stamina)*pow(CpM[pokemon_level*2-2],2)/10), 10) == user_cp) {
        possible_attacks.push(attack);
        possible_defenses.push(defense);
      }
    }
  }
}

def updatePokemon() {
  good_against = {}
  bad_against = {}
  resistance = {}
  attack_array1 = attack_matrix[types_lookup[pokemon[pk_id].Type1]];
  defense_array1 = defense_matrix[types_lookup[pokemon[pk_id].Type1]];

  if (pokemon[pk_id].Type2 == "None") {
    for (var i = 0; i < attack_array1.length; i++) {
      if (attack_array1[i] > 1) {
        good_against[types_dict[i]] = attack_array1[i];
      }
      if (defense_array1[i] > 1) {
        bad_against[types_dict[i]] = defense_array1[i];
      }
      if (defense_array1[i] < 1) {
        resistance[types_dict[i]] = defense_array1[i];
      }
    }
  } else {
    attack_array2 = attack_matrix[types_lookup[pokemon[pk_id].Type2]];
    defense_array2 = defense_matrix[types_lookup[pokemon[pk_id].Type2]];
    for (var i = 0; i < attack_array1.length; i++) {
      if (attack_array1[i] > 1 || attack_array2[i] > 1) {
        good_against[types_dict[i]] = max(attack_array1[i], attack_array2[i]);
      }
      if (defense_array1[i] * defense_array2[i] > 1) {
        bad_against[types_dict[i]] = defense_array1[i] * defense_array2[i];
      }
      if (defense_array1[i] * defense_array2[i] < 1) {
        resistance[types_dict[i]] = defense_array1[i] * defense_array2[i];
      }
    }
  }

  quick_moves = [];
  for (var i = 0; i < pokemon[pk_id].QuickMoves.length; i++) {
    var temp_move = JSON.parse(JSON.stringify(moves[pokemon[pk_id].QuickMoves[i]]));
    if (temp_move.Type == pokemon[pk_id].Type1 || temp_move.Type == pokemon[pk_id].Type2)
      temp_move.DPS *= 1.25;
    temp_move.Id = pokemon[pk_id].QuickMoves[i];
    quick_moves[quick_moves.length] = temp_move;
  }
  cinematic_moves = [];
  for (var i = 0; i < pokemon[pk_id].CinematicMoves.length; i++) {
    var temp_move = JSON.parse(JSON.stringify(moves[pokemon[pk_id].CinematicMoves[i]]));
    if (temp_move.Type == pokemon[pk_id].Type1 || temp_move.Type == pokemon[pk_id].Type2)
      temp_move.DPS *= 1.25;
    temp_move.Id = pokemon[pk_id].CinematicMoves[i];
    cinematic_moves[cinematic_moves.length] = temp_move;
  }

  moves_bad_against = [];
  for (var type in bad_against) {
    for(var i in moves) {
      if (moves[i].Type == type) {
        temp_move = JSON.parse(JSON.stringify(moves[i]));
        temp_move.DPS *= bad_against[type];
        moves_bad_against[moves_bad_against.length] = temp_move;
      }
    }
  }

  def compare_moves(a,b) {
    if (a.DPS > b.DPS)
      return -1;
    if (a.DPS < b.DPS)
      return 1;
    return 0;
  }

  moves_bad_against.sort(compare_moves);
  all_moves = quick_moves.concat(cinematic_moves);
  quick_moves.sort(compare_moves);
  cinematic_moves.sort(compare_moves);
  all_moves.sort(compare_moves);

  var type_good_against_label = document.getElementById("type_good_against");
  while (type_good_against_label.firstChild) {
      type_good_against_label.removeChild(type_good_against_label.firstChild);
  }
  var type_bad_against_label = document.getElementById("type_bad_against");
  while (type_bad_against_label.firstChild) {
      type_bad_against_label.removeChild(type_bad_against_label.firstChild);
  }
  for (var type in good_against) {
    var type_label = document.createElement("div");
    type_label.className = "type_comp " + type;
    type_label.innerHTML = type + " <span>x" + good_against[type].toPrecision(3) + "</span>";
    type_good_against_label.appendChild(type_label);
  }
  for (var type in bad_against) {
    var type_label = document.createElement("div");
    type_label.className = "type_comp " + type;
    type_label.innerHTML = type + " <span>x" + bad_against[type].toPrecision(3) + "</span>";
    type_bad_against_label.appendChild(type_label);
  }

  var moves_best_label = document.getElementById("moves_best");
  while (moves_best_label.firstChild) {
      moves_best_label.removeChild(moves_best_label.firstChild);
  }

  // for (var i in quick_moves) {
  //   var move_label = document.createElement("div");
  //   move_label.className = "move " + quick_moves[i].Type;
  //   move_label.innerHTML = quick_moves[i].Name + "<span class='power'>" + quick_moves[i].Power + "</span><span class='DPS'>" + quick_moves[i].DPS.toPrecision(3) + " DPS</span>";
  //   moves_best_label.appendChild(move_label);
  // }  
  // moves_best_label.appendChild(document.createElement("hr"));
  // for (var i in cinematic_moves) {
  //   var move_label = document.createElement("div");
  //   move_label.className = "move " + cinematic_moves[i].Type;
  //   move_label.innerHTML = cinematic_moves[i].Name + "<span class='power'>" + cinematic_moves[i].Power + "</span><span class='DPS'>" + cinematic_moves[i].DPS.toPrecision(3) + " DPS</span>";
  //   moves_best_label.appendChild(move_label);
  // }
  for (var i in all_moves) {
    var move_label = document.createElement("div");
    move_label.className = "move " + all_moves[i].Type;
    var fast = "";
    if (all_moves[i].Speed == "Fast")
      fast = " (fast)";
    move_label.innerHTML = "<input type='checkbox' id='"+all_moves[i].Id+"-move' class='move-check' /> " + all_moves[i].Name + fast + "<span class='power'>" + all_moves[i].Power + "</span><span class='DPS'>" + all_moves[i].DPS.toPrecision(3) + makeFraction("PWR", "SEC", "Power per Second") + "</span>";
    moves_best_label.appendChild(move_label);
    document.getElementById(all_moves[i].Id+"-move").addEventListener("change", drawImage);
  } 

  var moves_best_against_label = document.getElementById("moves_best_against");
  while (moves_best_against_label.firstChild) {
      moves_best_against_label.removeChild(moves_best_against_label.firstChild);
  }
  for (var i = 0; i < all_moves.length; i++) {
    var move_label = document.createElement("div");
    move_label.className = "move " + moves_bad_against[i].Type;
    move_label.innerHTML = moves_bad_against[i].Name + "<span class='power'>" + moves_bad_against[i].Power + "</span><span class='DPS'>" + moves_bad_against[i].DPS.toPrecision(3) + makeFraction("PWR", "SEC", "Power per Second") + "</span>";
    moves_best_against_label.appendChild(move_label);
  }

  var pokemon_good_against_label = document.getElementById("pokemon_good_against");
  while (pokemon_good_against_label.firstChild) {
      pokemon_good_against_label.removeChild(pokemon_good_against_label.firstChild);
  }
  var pokemon_worst_against_label = document.getElementById("pokemon_worst_against");
  while (pokemon_worst_against_label.firstChild) {
      pokemon_worst_against_label.removeChild(pokemon_worst_against_label.firstChild);
  }
  // for (var i = 1; i < pokemon.length; i++) {
  //   for (var type in good_against) {
  //     if (pokemon[i].Type1 == type || pokemon[i].Type2 == type) {
  //       pokemon_good_against[pokemon_good_against.length] = pokemon[i];
  //     }
  //   }
  // }

  best_move_dps = 0;
  for (var i in pokemon_x_moves) {
    if (pokemon_x_moves[i].Id == pk_id) {
      best_move_dps = max(pokemon_x_moves[i].DPS, best_move_dps);
    }
  }

  var pokemon_good_against = [];
  var pokemon_worst_against = [];
  for (var i in pokemon_x_moves) {
    if (pokemon[pk_id].Type1 == "Normal" && pokemon[pk_id].Type2 == "None" && best_move_dps > pokemon_x_moves[i].DPS) {
        pokemon_good_against[pokemon_good_against.length] = pokemon_x_moves[i];
    } else {
      for (var type in good_against) {
        if ((pokemon_x_moves[i].Type1 == type || pokemon_x_moves[i].Type2 == type) && best_move_dps > pokemon_x_moves[i].DPS) {
          pokemon_good_against[pokemon_good_against.length] = pokemon_x_moves[i];
        }
      }
    }
    for (var type in bad_against) {
      if (pokemon_x_moves[i].Move.Type == type) {
        pkmv = JSON.parse(JSON.stringify(pokemon_x_moves[i]));
        pkmv.DPS *= bad_against[type];
        pokemon_worst_against[pokemon_worst_against.length] = pkmv;
      }
    }
  }

  for (var i = 0; i < min(10, pokemon_good_against.length); i++) {
    var mon = document.createElement("div");
    mon.className = "move " + pokemon_good_against[i].Move.Type;
    mon.innerHTML = pokemon_good_against[i].Name + " with " + pokemon_good_against[i].Move.Name + "<span class='DPS'>" + parseInt(pokemon_good_against[i].DPS) + makeFraction("AP", "SEC", "Attack-Power per Second") +"</span>";
    pokemon_good_against_label.appendChild(mon);
  }
  for (var i = 0; i < min(10, pokemon_worst_against.length); i++) {
    var mon = document.createElement("div");
    mon.className = "move " + pokemon_worst_against[i].Move.Type;
    mon.innerHTML = pokemon_worst_against[i].Name + " with " + pokemon_worst_against[i].Move.Name + "<span class='DPS'>" + parseInt(pokemon_worst_against[i].DPS) + makeFraction("AP", "SEC", "Attack-Power per Second") +"</span>";
    pokemon_worst_against_label.appendChild(mon);
  }


}



def compare_pokemon_x_move(a,b) {
  if (a.DPS > b.DPS)
    return -1;
  if (a.DPS < b.DPS)
    return 1;
  return 0;
}

pokemon_x_moves = [];
for (var i = 1; i < pokemon.length; i++) {
  for (var move_id in pokemon[i].QuickMoves) {
    var pk = JSON.parse(JSON.stringify(pokemon[i]));
    pk.Move = JSON.parse(JSON.stringify(moves[pk.QuickMoves[move_id]]));
    pk.DPS = pk.Move.DPS * (pk.BaseAttack + 7.5);
    if (pk.Move.Type == pk.Type1 || pk.Move.Type == pk.Type2)
      pk.DPS *= 1.25;
    pokemon_x_moves[pokemon_x_moves.length] = pk;
  }
  for (var move_id in pokemon[i].CinematicMoves) {
    var pk = JSON.parse(JSON.stringify(pokemon[i]));
    pk.Move = JSON.parse(JSON.stringify(moves[pk.CinematicMoves[move_id]]));
    pk.DPS = pk.Move.DPS * (pk.BaseAttack + 7.5);
    if (pk.Move.Type == pk.Type1 || pk.Move.Type == pk.Type2)
      pk.DPS *= 1.25;
    pokemon_x_moves[pokemon_x_moves.length] = pk;
  }
}

pokemon_x_moves.sort(compare_pokemon_x_move);
// for (var i in pokemon_x_moves) {
//   console.log(pokemon_x_moves[i].Name + " with " + pokemon_x_moves[i].Move.Name + "\t" + pokemon_x_moves[i].DPS);
// }
'''


