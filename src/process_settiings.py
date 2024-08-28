import pandas as pd
import json


settings = "npc_settings.csv"
df = pd.read_csv(settings, encoding="utf-8")

npc_names = df["npc_name"][1:6].values
settings = df["setting"][1:6].values
npc_instructions = df["npc_instruction"][1:6].values
npc_settings = df["npc_setting"][1:6].values
npc_styles = df["npc_style"][1:6].values
npc_locations = df["npc_location"][1:6].values
backgrounds = df["background"][1:6].values
speech_examples = df["台词示例"][1:6].values
pc_settings = df["pc_setting"][1:6].values

res = {}
for i in range(5):
    res[npc_names[i]] = {
        "npc_name": npc_names[i],
        "setting": settings[i],
        "npc_instruction": npc_instructions[i],
        "npc_setting": npc_settings[i],
        "npc_style": npc_styles[i],
        "npc_location": npc_locations[i],
        "background": backgrounds[i],
        "speech_example": speech_examples[i],
        "pc_setting": pc_settings[i]
    }

# res = []
# for i in range(5):
#     res.append({
#         "npc_name": npc_names[i],
#         "setting": settings[i],
#         "npc_instruction": npc_instructions[i],
#         "npc_setting": npc_settings[i],
#         "npc_style": npc_styles[i],
#         "npc_location": npc_locations[i],
#         "background": backgrounds[i],
#         "speech_example": speech_examples[i],
#         "pc_setting": pc_settings[i]
#         })

with open("npc_settings.json", "w", encoding="utf-8") as fp:
    json.dump(res, fp, ensure_ascii=False, indent=4)
