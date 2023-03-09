import urllib.parse, urllib.request, urllib.error, json
import pprint


def get_poke_data(wanted_info):
    baseurl = "http://pokeapi.co/api/v2/"
    url = baseurl + wanted_info
    try:
        request = urllib.request.Request(url)
        request.add_header('User-Agent', "pokemon")
        data = urllib.request.urlopen(request).read()
    except urllib.error.HTTPError as e:
        print("Error trying to retrieve data: HTTP Error " + str(e.code) + ": Bad Request")
        return None
    except urllib.error.URLError as e:
        print("Error trying to retrieve data: Failed to reach server. Reason: " + e.reason)
        return None
    return json.loads(data)


def get_pokemon_list(limit=100000, offset=0):
    pokemon_name_list = []
    args = {"limit": limit, "offset": offset}
    paramstr = "pokemon?" + urllib.parse.urlencode(args)
    full_pokemon_list = get_poke_data(paramstr)["results"]
    if len(full_pokemon_list) == 0:
        print("There might be no Pokemon within those bounds")
        return None
    for pokemon in full_pokemon_list:
        pokemon_name_list.append(pokemon["name"])
    return pokemon_name_list


def get_pokemon_info(wanted_pokemon):
    return get_poke_data("pokemon/" + str(wanted_pokemon).strip().replace(" ", "-").lower())


def get_ability_info(wanted_ability):
    return get_poke_data("ability/" + wanted_ability.strip().replace(" ", "-").lower())


def get_type_info(wanted_type):
    return get_poke_data("type/" + str(wanted_type).lower())


def name_to_id(pokemon_name):
    try:
        print(get_pokemon_info(pokemon_name)["id"])
    except TypeError:
        print("There might not be a Pokemon with that name")


def id_to_name(pokemon_id):
    try:
        print(get_pokemon_info(pokemon_id)["forms"][0]["name"])
    except TypeError:
        print("There might not be a Pokemon with that id")


def poke_with_ability(ability):
    try:
        data = get_ability_info(ability)
        ability_list = []
        for pokemon in data["pokemon"]:
            ability_list.append(pokemon["pokemon"]["name"])
    except TypeError:
        return []
    return ability_list


def poke_with_type(poke_type):
    try:
        data = get_type_info(poke_type)
        type_list = []
        for pokemon in data["pokemon"]:
            type_list.append(pokemon["pokemon"]["name"])
    except TypeError:
        return []
    return type_list


def sort_by_exp_gain(poke_list):
    exp_dict = {}
    try:
        for pokemon in poke_list:
            if get_pokemon_info(pokemon)["base_experience"] is not None:
                exp_dict[pokemon.lower()] = get_pokemon_info(pokemon)["base_experience"]
            elif get_pokemon_info(pokemon)["base_experience"] is None:
                exp_dict[pokemon.lower()] = 0
    except TypeError:
        print("There might not be a Pokemon with one of those names")
        return None
    sorted_exp_dict = sorted(exp_dict.items(), key=get_exp, reverse=True)
    return sorted_exp_dict


def get_exp(poke_exp):
    return poke_exp[1]


class Pokemon_Info:
    def __init__(self, info_dict):
        self.info = info_dict

    def sprite(self):
        return self.info["sprites"]["front_default"]

    def name(self):
        return self.info["name"].replace("-", " ")

    def type(self):
        types = ""
        for poke_type in self.info["types"]:
            types += " " + poke_type["type"]["name"] + " "
        return types

    def id(self):
        return self.info["id"]

    def stats(self):
        stat_spread = []
        stat_total = 0
        for stat in self.info["stats"]:
            stat_total += int(stat["base_stat"])
            stat_spread.append(stat["base_stat"])
        stat_spread.append(str(stat_total))
        return stat_spread

    def abilities(self):
        ability_to_desc = {}
        for ability in self.info["abilities"]:
            abl_desc = get_ability_info(ability["ability"]["name"])
            desc = abl_desc["effect_entries"][1]["effect"]
            ability_to_desc[ability["ability"]["name"].replace("-", " ").upper()] = desc
        return ability_to_desc
