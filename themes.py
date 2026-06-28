THEMES = {

    "Light": {
        "bg": "#F5F5F5",
        "fg": "#222222",
        "button_bg": "#4CAF50",
        "button_fg": "#FFFFFF"
    },

    "Dark": {
        "bg": "#2B2B2B",
        "fg": "#FFFFFF",
        "button_bg": "#555555",
        "button_fg": "#FFFFFF"
    },

    "Ocean Blue": {
        "bg": "#DCEFFF",
        "fg": "#003366",
        "button_bg": "#2196F3",
        "button_fg": "#FFFFFF"
    },

    "Sakura": {
        "bg": "#FFF0F5",
        "fg": "#C2185B",
        "button_bg": "#F48FB1",
        "button_fg": "#FFFFFF"
    },

    "Forest Green": {
        "bg": "#E8F5E9",
        "fg": "#1B5E20",
        "button_bg": "#43A047",
        "button_fg": "#FFFFFF"
    },

    "Lavender": {
        "bg": "#F3E5F5",
        "fg": "#6A1B9A",
        "button_bg": "#AB47BC",
        "button_fg": "#FFFFFF"
    }

}


def get_theme(name):

    return THEMES.get(
        name,
        THEMES["Light"]
    )