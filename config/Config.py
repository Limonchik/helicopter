import os.path

from config.config_utils import get_config

emoji_config = {
    "tree": "🌲",
    "water": "🌊",
    "helicopter": "🚁",
    "grass": "🟩",
    "fire": "🔥",
    "hospital": "🏥",
    "heart": "💛",
    "money": "💵",
    "border": "⬛",
    "tank": "\uD83E\uDDF3".encode("utf-16", "surrogatepass").decode("utf-16"),
    "score": "\uD83C\uDFC6".encode("utf-16", "surrogatepass").decode("utf-16"),
    "cloud": "⛅",
    "lightning": "🌩️".encode("utf-16", "surrogatepass").decode("utf-16")
}

default_config_dict = {
    "keybindings": {
        "move_up": ["w", "ц"],
        "move_down": ["s", "ы"],
        "move_right": ["d", "в"],
        "move_left": ["a", "ф"]
    },
    "generation": {
        "field_size": 15,
        "tree_chance": 0.2,
        "lake_size": 10,
        "clouds_quantity": 12,
        "lightning_chance": 0.4,
        "clouds_update_sec": 8,
        "fire_generation_sec": 9,
        "tree_generation_sec": 15,
        "fire_duration_sec": 7,
        "fire_chance": 0.05,
    },
    "helicopter": {
        "initial_max_tank_capacity": 10,
        "initial_tank_capacity": 10,
        "cooldown_fill_tank_sec": 0.5,
        "initial_health": 10,
        "max_health": 10,
        "extinguishing_water_cost": 10,
        "extinguishing_monetary_reward": 100,
        "extinguishing_score_reward": 100,
        "initial_heal_money_cost": 100,
        "initial_levelup_money_cost": 100
    },
    "render": {
        "fps": 30
    }
}

config_path = os.path.abspath(os.curdir) + "/gamesettings.ini"

_config = get_config(default_config_dict, config_path)

generation_config = _config.generation
keybindings_config = _config.keybindings
helicopter_config = _config.helicopter
render_config = _config.render
