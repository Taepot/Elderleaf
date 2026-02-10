TEA_CHANNEL_ID = 1469580223552028807


import random
import os
import discord
from discord.ext import commands

# ---------- BOT SETUP ----------
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# ---------- MENU WITH ALIASES ----------
MENU = {
    "Teas": [
        {"name": "Hawthorn Tea", "aliases": ["hawthorn", "thorn"], "effect": "Calms the nerves and steadies the heart."},
        {"name": "Lavender Nightsteep", "aliases": ["lavender", "night"], "effect": "Invites rest and gentler thoughts."},
        {"name": "Elderflower White", "aliases": ["elder", "flower"], "effect": "Lifts the spirit softly."},
        {"name": "Thornrose Oolong", "aliases": ["thornrose", "rose"], "effect": "Brings emotional clarity."},
        {"name": "Chamomile Gold", "aliases": ["chamomile", "gold"], "effect": "Soothes anxiety and tension."},
        {"name": "Mint Fern Tea", "aliases": ["mint", "fern"], "effect": "Refreshes the mind."},
        {"name": "Birchroot Brew", "aliases": ["birch", "root"], "effect": "Grounds wandering thoughts."},
        {"name": "Moonpetal Tea", "aliases": ["moonpetal", "moon"], "effect": "Enhances intuition."},
        {"name": "Rosehip Ember", "aliases": ["rosehip", "ember"], "effect": "Restores warmth and balance."},
        {"name": "Hearthleaf Green", "aliases": ["hearthleaf", "hearth"], "effect": "Clears mental fog."}
    ],

    "Coffee": [
        {"name": "Hexfire Roast", "aliases": ["hexfire", "hex"], "effect": "Restores stamina and resolve."},
        {"name": "Cinnamon Sigil Brew", "aliases": ["cinnamon", "sigil"], "effect": "Encourages courage."},
        {"name": "Midnight Familiar Espresso", "aliases": ["midnight", "familiar"], "effect": "Sharpens alertness."},
        {"name": "Star-Anise Mocha", "aliases": ["anise", "star"], "effect": "Focus with warmth."},
        {"name": "Witchwake Latte", "aliases": ["witchwake", "latte"], "effect": "Gently awakens the senses."},
        {"name": "Dark Orchard Roast", "aliases": ["orchard", "dark"], "effect": "Steady productivity."},
        {"name": "Smoked Acorn Coffee", "aliases": ["acorn", "smoked"], "effect": "Slow-burning energy."},
        {"name": "Ashen Morning Brew", "aliases": ["ashen", "morning"], "effect": "Cuts through exhaustion."},
        {"name": "Velvet Dusk Coffee", "aliases": ["velvet", "dusk"], "effect": "Calm focus."},
        {"name": "Runescribed Cappuccino", "aliases": ["rune", "cappuccino"], "effect": "Mental clarity."}
    ],

    "Juices & Gentle Drinks": [
        {"name": "Wildberry Tonic", "aliases": ["wildberry", "berry"], "effect": "Refreshes body and spirit."},
        {"name": "Honeyed Pear Nectar", "aliases": ["pear", "honey"], "effect": "Comforting calm."},
        {"name": "Cucumber Mint Springwater", "aliases": ["cucumber", "spring"], "effect": "Cooling clarity."},
        {"name": "Dewdrop Apple Cider", "aliases": ["dewdrop", "apple"], "effect": "Light warmth and cheer."},
        {"name": "Elderberry Juice", "aliases": ["elderberry", "berryjuice"], "effect": "Restorative vitality."},
        {"name": "Golden Citrus Infusion", "aliases": ["citrus", "golden"], "effect": "Brightens mood."},
        {"name": "Pomegranate Mist", "aliases": ["pomegranate", "mist"], "effect": "Emotional renewal."},
        {"name": "Plum Grove Juice", "aliases": ["plum", "grove"], "effect": "Grounding sweetness."},
        {"name": "Frostmelon Water", "aliases": ["frostmelon", "melon"], "effect": "Cooling calm."},
        {"name": "Rosewater Lemonade", "aliases": ["rosewater", "lemon"], "effect": "Gentle uplift."}
    ],

    "Potions (Arcane)": [
        {"name": "Starlight Draught", "aliases": ["starlight", "star"], "effect": "Inspiration and creativity."},
        {"name": "Verdant Elixir", "aliases": ["verdant", "green"], "effect": "Renewal and growth."},
        {"name": "Shadowglass Tonic", "aliases": ["shadowglass", "shadow"], "effect": "Quiet introspection."},
        {"name": "Phoenix Sap Syrup", "aliases": ["phoenix", "sap"], "effect": "Emotional recovery."},
        {"name": "Moonveil Philter", "aliases": ["moonveil", "veil"], "effect": "Heightened intuition."},
        {"name": "Ironroot Tonic", "aliases": ["ironroot", "iron"], "effect": "Inner strength."},
        {"name": "Dreamer’s Distillate", "aliases": ["dreamer", "dream"], "effect": "Vivid imagination."},
        {"name": "Feystep Serum", "aliases": ["feystep", "fey"], "effect": "Restless curiosity."},
        {"name": "Obsidian Calm", "aliases": ["obsidian", "calm"], "effect": "Protective stillness."},
        {"name": "Aurora Bloom Potion", "aliases": ["aurora", "bloom"], "effect": "Hope and motivation."}
    ]
}

# ---------- LOOKUP TABLE ----------
LOOKUP = {}
ALL_ITEMS = []

for items in MENU.values():
    for item in items:
        ALL_ITEMS.append(item)
        LOOKUP[item["name"].lower()] = item
        for alias in item["aliases"]:
            LOOKUP[alias.lower()] = item

# ---------- SERVING VARIETY ----------
SERVE_LINES = [
    "{name} is served. {effect}",
    "Elderleaf pours {name}. {effect}",
    "A cup of {name} waits for you. {effect}",
    "{name} is prepared with care. {effect}"
]

# ---------- MOOD MAP ----------
MOODS = {
    "tired": ["Lavender Nightsteep", "Chamomile Gold", "Velvet Dusk Coffee"],
    "anxious": ["Hawthorn Tea", "Obsidian Calm", "Honeyed Pear Nectar"],
    "focused": ["Runescribed Cappuccino", "Mint Fern Tea", "Golden Citrus Infusion"],
    "sad": ["Elderflower White", "Rosewater Lemonade", "Phoenix Sap Syrup"],
    "creative": ["Starlight Draught", "Dreamer’s Distillate", "Moonpetal Tea"]
}

# ---------- EVENTS ----------
@bot.event
async def on_ready():
    print(f"Elderleaf has entered the hearth as {bot.user}")

# ---------- COMMANDS ----------

@bot.command()
async def drinks(ctx, *, choice=None):
    if not choice:
        await ctx.send("Tell me the name… or say `!drinks random`.")
        return

    if choice.lower() == "random":
        item = random.choice(ALL_ITEMS)
    else:
        item = LOOKUP.get(choice.lower())

    if not item:
        await ctx.send("That brew is not on the shelves tonight.")
        return

    line = random.choice(SERVE_LINES)
    await ctx.send(line.format(name=item["name"], effect=item["effect"]))




# ---------- RUN BOT ----------

import os
bot.run(os.getenv("DISCORD_TOKEN"))




