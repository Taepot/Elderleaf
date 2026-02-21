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

ALLOWED_ROLE = "Merlins"

FAVOURED_USER = "kae"
PARTICULAR_USER = "Element"

DIALOGUE = {
    "kae": [
        "Hi Kae. The kettle was already warm for you.",
        "Kae… I was hoping you would come by today.",
        "For you, Kae, the drinks are on the house.",
        "Boy, masaya ba akong makita ka kae, masaya ka ba na makita ako?"
    ],
    "element": [
        "Element… I trust this preparation meets your standards.",
        "I have measured this carefully, Element. As you prefer.",
        "Element, I adjusted the steeping time precisely.",
        "I trust that you shan't worry about giving off wrong first impressions?"
    ],
    "default": [
        "Our hearth is always open for you.",
        "Come grab a sit. The kettle is humming gently.",
        "Relax, make yourself at home here.",
        "How is the AFKJ journey going?"
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
    await bot.tree.sync()
    print(f"Elderleaf has entered the hearth as {bot.user}")

# ---------- COMMANDS ----------

class DrinkSelect(discord.ui.Select):
    def __init__(self):
        options = []

        for item in ALL_ITEMS[:25]:  # Discord limit is 25 options per menu
            options.append(
                discord.SelectOption(
                    label=item["name"],
                    description=item["effect"][:100]
                )
            )

        super().__init__(
            placeholder="Choose a drink from the hearth...",
            min_values=1,
            max_values=1,
            options=options
        )

    async def callback(self, interaction: discord.Interaction):
        selected_name = self.values[0]
        item = LOOKUP.get(selected_name.lower())

        line = random.choice(SERVE_LINES)
        await interaction.response.send_message(
            line.format(name=item["name"], effect=item["effect"])
        )

class DrinkView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=60)
        self.add_item(DrinkSelect())

@bot.tree.command(name="order", description="Order a drink from Elderleaf")
async def order(interaction: discord.Interaction):
    await interaction.response.send_message(
        "The kettle hums softly. Choose your drink:",
        view=DrinkView()
    )

@bot.command()
async def say(ctx, member: discord.Member = None):
    if not member:
        await ctx.send("Tell me who you wish me to address.")
        return

    name = member.name.lower()

    if name == FAVOURED_USER:
        line = random.choice(DIALOGUE["kae"])
    elif name == PARTICULAR_USER:
        line = random.choice(DIALOGUE["element"])
    else:
        line = random.choice(DIALOGUE["default"])

    await ctx.send(f"{member.mention} — {line}")

@bot.command()
async def serve(ctx, member: discord.Member, *, choice=None):
    # Check role permission
    if ALLOWED_ROLE not in [role.name for role in ctx.author.roles]:
        await ctx.send("Only the entrusted may pour for others :)")
        return

    if not choice:
        await ctx.send("Tell me what you wish to serve… or say `random`.")
        return

    # Select drink
    if choice.lower() == "random":
        item = random.choice(ALL_ITEMS)
    else:
        item = LOOKUP.get(choice.lower())

    if not item:
        await ctx.send("That brew is not on the shelves tonight.")
        return

    line = random.choice(SERVE_LINES)

    await ctx.send(
        f"🌿 {item['name']} is served to {member.mention}. {item['effect']}"
    )

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















