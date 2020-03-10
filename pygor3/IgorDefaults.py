#      Author: Carlos Olivares
#
#   Copyright (C) 2020 Carlos Olivares
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.

#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <https://www.gnu.org/licenses/>.


Igor_event_type_list = ['GeneChoice', 'Deletion', 'Insertion', 'DinucMarkov']

igor_nickname_list = ["v_choice", "j_choice", "d_gene", "v_3_del",
                     "d_3_del", "d_5_del", "j_5_del",
                     "vd_ins", "vd_dinucl", "dj_ins", "dj_dinucl",
                     "vj_ins", "vj_dinucl"]



IgorRec_Event_default_dict = {
    # GeneChoice;V_gene;Undefined_side;7;v_choice
    'v_choice': {
        "event_type": "GeneChoice",
        "seq_type": "V_gene",
        "seq_side": "Undefined_side",
        "priority": 7,
        "realizations": list(),
        "name": "",
        "nickname": "v_choice"
    },
    # GeneChoice;J_gene;Undefined_side;7;j_choice
    'j_choice': {
        "event_type": "GeneChoice",
        "seq_type": "J_gene",
        "seq_side": "Undefined_side",
        "priority": 7,
        "realizations": list(),
        "name": "",
        "nickname": "j_choice"
    },
    # GeneChoice;D_gene;Undefined_side;6;d_gene
    'd_gene': {
        "event_type": "GeneChoice",
        "seq_type": "D_gene",
        "seq_side": "Undefined_side",
        "priority": 6,
        "realizations": list(),
        "name": "",
        "nickname": "d_gene"
    },
    # Deletion;V_gene;Three_prime;5;v_3_del
    'v_3_del': {
        "event_type": "Deletion",
        "seq_type": "V_gene",
        "seq_side": "Three_prime",
        "priority": 5,
        "realizations": list(),
        "name": "",
        "nickname": "v_3_del"
    },
    # Deletion;D_gene;Three_prime;5;d_3_del
    'd_3_del': {
        "event_type": "Deletion",
        "seq_type": "D_gene",
        "seq_side": "Three_prime",
        "priority": 5,
        "realizations": list(),
        "name": "",
        "nickname": "d_3_del"
    },
    # Deletion;D_gene;Five_prime;5;d_5_del
    'd_5_del': {
        "event_type": "Deletion",
        "seq_type": "D_gene",
        "seq_side": "Five_prime",
        "priority": 5,
        "realizations": list(),
        "name": "",
        "nickname": "d_5_del"
    },
    # Deletion;J_gene;Five_prime;5;j_5_del
    'j_5_del': {
        "event_type": "Deletion",
        "seq_type": "J_gene",
        "seq_side": "Five_prime",
        "priority": 5,
        "realizations": list(),
        "name": "",
        "nickname": "j_5_del"
    },
    # Insertion;VD_genes;Undefined_side;4;vd_ins
    'vd_ins': {
        "event_type": "Insertion",
        "seq_type": "VD_genes",
        "seq_side": "Undefined_side",
        "priority": 4,
        "realizations": list(),
        "name": "",
        "nickname": "vd_ins"
    },
    # DinucMarkov;VD_genes;Undefined_side;3;vd_dinucl
    'vd_dinucl': {
        "event_type": "DinucMarkov",
        "seq_type": "VD_genes",
        "seq_side": "Undefined_side",
        "priority": 3,
        "realizations": list(),
        "name": "",
        "nickname": "vd_dinucl"
    },
    # Insertion;DJ_gene;Undefined_side;2;dj_ins
    'dj_ins': {
        "event_type": "Insertion",
        "seq_type": "DJ_gene",
        "seq_side": "Undefined_side",
        "priority": 2,
        "realizations": list(),
        "name": "",
        "nickname": "dj_ins"
    },
    # DinucMarkov;DJ_gene;Undefined_side;1;dj_dinucl
    'dj_dinucl': {
        "event_type": "DinucMarkov",
        "seq_type": "DJ_gene",
        "seq_side": "Undefined_side",
        "priority": 1,
        "realizations": list(),
        "name": "",
        "nickname": "dj_dinucl"
    },
    #Insertion;VJ_gene;Undefined_side;4;vj_ins
    'vj_ins': {
        "event_type": "Insertion",
        "seq_type": "VJ_gene",
        "seq_side": "Undefined_side",
        "priority": 4,
        "realizations": list(),
        "name": "",
        "nickname": "vj_ins"
    },
    #DinucMarkov;VJ_gene;Undefined_side;3;vj_dinucl
    'vj_dinucl': {
        "event_type": "DinucMarkov",
        "seq_type": "VJ_gene",
        "seq_side": "Undefined_side",
        "priority": 3,
        "realizations": list(),
        "name": "",
        "nickname": "vj_dinucl"
    }
}
#SingleErrorRate

vdj_dict_default = {
    'v_choice' : {},
    'j_choice' : {'v_choice'},
    'd_gene' : {'v_choice', 'j_choice'},
    'v_3_del' : {'v_choice'},
    'd_5_del' : {'d_gene'},
    'd_3_del' : {'d_gene', 'd_5_del'},
    'j_5_del' : {'j_choice'},
    'vd_ins' : {},
    'vd_dinucl' : {},
    'dj_ins' : {},
    'dj_dinucl' : {}
}

vj_dict_default = {
    'v_choice' : {},
    'j_choice' : {'v_choice'},
    'd_gene' : {'v_choice', 'j_choice'},
    'v_3_del' : {'v_choice'},
    'd_5_del' : {'d_gene'},
    'd_3_del' : {'d_gene', 'd_5_del'},
    'j_5_del' : {'j_choice'},
    'vd_ins' : {},
    'vd_dinucl' : {},
    'dj_ins' : {},
    'dj_dinucl' : {}
}