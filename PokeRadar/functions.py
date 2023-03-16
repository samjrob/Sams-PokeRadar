import urllib.request, urllib.error, json


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


def get_pokemon_info(wanted_pokemon):
    return get_poke_data("pokemon/" + str(wanted_pokemon).strip().replace(" ", "-").lower())


def get_ability_info(wanted_ability):
    return get_poke_data("ability/" + wanted_ability.strip().replace(" ", "-").lower())


def get_type_info(wanted_type):
    return get_poke_data("type/" + str(wanted_type).lower())


def get_move_learn_list(wanted_move):
    return get_poke_data("move/" + wanted_move.strip().replace(" ", "-").lower())


def get_poke_in_generation(wanted_gen):
    return get_poke_data("generation/" + wanted_gen.strip().replace(" ", "-").lower())


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


def poke_with_move(poke_move):
    try:
        data = get_move_learn_list(poke_move)
        type_list = []
        for pokemon in data["learned_by_pokemon"]:
            type_list.append(pokemon["name"])
    except TypeError:
        return []
    return type_list


def poke_in_generation(poke_gen):
    try:
        data = get_poke_in_generation(poke_gen)
        type_list = []
        for pokemon in data["pokemon_species"]:
            type_list.append(pokemon["name"])
    except TypeError:
        return []
    return type_list


def poke_forms():
    form_dict = {"mimikyu": ["mimikyu-disguised", "mimikyu-busted"],
                 "oricorio": ["oricorio-baile", "oricorio-pom-pom", "oricorio-pau", "oricorio-sensu"],
                 "shaymin": ["shaymin-land", "shaymin-sky"],
                 "deoxys": ["deoxys-normal", "deoxys-attack", "deoxys-defense", "deoxys-speed"],
                 "tauros-paldea": ["tauros-paldea-combat-breed", "tauros-paldea-blaze-breed", "tauros-paldea-aqua-breed"],
                 "squawkabilly": ["squawkabilly-base-form", "squawkabilly-blue-plumage", "squawkabilly-yellow-plumage",
                                  "squawkabilly-white-plumage"],
                 "pikachu": ["pikachu-base-form", "pikachu-original-cap", "pikachu-hoenn-cap", "pikachu-sinnoh-cap",
                             "pikachu-unova-cap", "pikachu-kalos-cap", "pikachu-alola-cap", "pikachu-partner-cap"],
                 "castform": ["castform-base-form", "castform-sunny", "castform-rainy", "castform-snowy"],
                 "wormadam": ["wormadam-plant", "wormadam-sandy", "wormadam-trash"],
                 "tatsugiri": ["tatsugiri-base-form", "tatsugiri-droopy", "tatsugiri-stretchy"],
                 "rotom": ["rotom-base-form", "rotom-heat", "rotom-wash", "rotom-frost", "rotom-fan", "rotom-mow"],
                 "basculegion": ["basculegion-female", "basculegion-male"],
                 "basculin": ["basculin-red-striped", "basculin-blue-striped", "basculin-white-striped"],
                 "darmanitan": ["darmanitan-standard", "darmanitan-zen"],
                 "darmanitan-galar": ["darmanitan-galar-standard", "darmanitan-galar-zen"],
                 "kyurem": ["kyurem-base-form", "kyurem-black", "kyurem-white"],
                 "keldeo": ["keldeo-ordinary", "keldeo-resolute"],
                 "meloetta": ["meloetta-aria", "meloetta-pirouette"],
                 "greninja": ["greninja-base-form", "greninja-battle-bond", "greninja-ash"],
                 "aegislash": ["aegislash-shield", "aegislash-blade"],
                 "zygarde": ["zygarde-50", "zygarde-10-power-construct", "zygarde-50-power-construct", "zygarde-complete"],
                 "lycanroc": ["lycanroc-midday", "lycanroc-dusk", "lycanroc-midnight"],
                 "wishiwashi": ["wishiwashi-solo", "wishiwashi-school"],
                 "minior": ["minior-red-meteor", "minior-orange-meteor", "minior-yellow-meteor", "minior-green-meteor",
                            "minior-blue-meteor", "minior-indigo-meteor", "minior-violet-meteor", "minior-red",
                            "minior-orange", "minior-yellow", "minior-green", "minior-blue", "minior-indigo", "minior-violet"],
                 "necrozma": ["necrozma-base-form", "necrozma-dusk", "necrozma-dawn"],
                 "magearna": ["magearna-base-form", "magearna-original"],
                 "toxtricity": ["toxtricity-amped", "toxtricity-low-key"],
                 "eiscue": ["eiscue-ice", "eiscue-noice"],
                 "morpeko": ["morpeko-full-belly", "morpeko-hangry"],
                 "urshifu": ["urshifu-single-strike", "urshifu-rapid-strike"],
                 "palafin": ["palafin-base-form", "palafin-hero"]}
    return form_dict


def get_effect(poke_list):
    return poke_list[1]


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

    def type_interaction(self):
        type_list = {}
        im_re_we = {"Immune To": [], "Resists": [], "Weak To": []}
        for poke_type in self.info["types"]:
            type_info = get_type_info(poke_type["type"]["name"])
            for immunity in type_info["damage_relations"]["no_damage_from"]:
                type_name = immunity["name"]
                type_list[type_name] = type_list.get(type_name, 1) * 0
            for resistance in type_info["damage_relations"]["half_damage_from"]:
                type_name = resistance["name"]
                type_list[type_name] = type_list.get(type_name, 1) * 0.5
            for weakness in type_info["damage_relations"]["double_damage_from"]:
                type_name = weakness["name"]
                type_list[type_name] = type_list.get(type_name, 1) * 2
        for type_name in type_list.keys():
            type_interaction = type_name, type_list[type_name]
            if type_list[type_name] == 0:
                im_re_we["Immune To"].append(type_interaction)
            elif type_list[type_name] < 1:
                im_re_we["Resists"].append(type_interaction)
            elif type_list[type_name] > 1:
                im_re_we["Weak To"].append(type_interaction)
        return im_re_we

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
            lang_index = 0
            abl_desc = get_ability_info(ability["ability"]["name"])
            if len(abl_desc["effect_entries"]) > 0:
                while abl_desc["effect_entries"][lang_index]["language"]["name"] != "en":
                    lang_index += 1
                desc = abl_desc["effect_entries"][lang_index]["effect"]
            elif len(abl_desc["flavor_text_entries"]) > 0:
                while abl_desc["flavor_text_entries"][lang_index]["language"]["name"] != "en":
                    lang_index += 1
                desc = abl_desc["flavor_text_entries"][lang_index]["flavor_text"]
            else:
                desc = "Could Not Find Information on this Ability."
            ability_name = str(ability["ability"]["name"].replace("-", " ").upper())
            if ability["is_hidden"]:
                ability_name += " (Hidden)"
            ability_to_desc[ability_name] = desc
        return ability_to_desc

    def exp(self):
        return self.info["base_experience"]
