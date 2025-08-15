
import json

class ToneGenerator:
    def __init__(self, main_planet):
        self.main_planet = main_planet

        # ファイル読み込み
        with open("modulation_tag_map.json", "r", encoding="utf-8") as f:
            self.modulation_tag = json.load(f)
        with open("conjunction_category_map.json", "r", encoding="utf-8") as f:
            self.conjunction_map = json.load(f)
        with open(f"tone_style_prompts_{main_planet.lower()}.json", "r", encoding="utf-8") as f:
            self.prompts = json.load(f)[main_planet]
        with open("tone_style_prompts_noaspect.json", "r", encoding="utf-8") as f:
            self.noaspect = json.load(f)

    def generate(self, sign, aspects):
        # tone_1
        tone_1 = {
            "modulation_inputs": [self.modulation_tag[self.main_planet][sign]["modulation_input"]],
            "expression_hint": self.modulation_tag[self.main_planet][sign]["expression_hint"],
            "example": self.modulation_tag[self.main_planet][sign]["example"]
        }

        # tone_2 / tone_3 init
        tone_2_inputs, tone_3_inputs = [], []
        tone_2_main, tone_3_main = None, None
        min_soft, min_hard = float("inf"), float("inf")

        for asp in aspects:
            target = asp["相手天体"]
            orb = asp["orb"]
            kind = asp["種別"]

            if kind == "soft" and target in self.prompts and "soft" in self.prompts[target]:
                if orb < min_soft:
                    min_soft = orb
                    tone_2_main = self.prompts[target]["soft"]
                tone_2_inputs += self.prompts[target]["soft"]["modulation_seed"]

            elif kind == "hard" and target in self.prompts and "hard" in self.prompts[target]:
                if orb < min_hard:
                    min_hard = orb
                    tone_3_main = self.prompts[target]["hard"]
                tone_3_inputs += self.prompts[target]["hard"]["modulation_seed"]

            elif kind == "conjunction":
                conj = self.conjunction_map.get(self.main_planet, {}).get("self_conjunction", {}).get(target)
                if not conj:
                    continue
                if conj["classification"] in ["soft", "neutral"]:
                    tone_2_inputs += conj["positive_keywords"]
                if conj["classification"] in ["hard", "neutral"]:
                    tone_3_inputs += conj["negative_keywords"]

        # tone_2出力
        tone_2 = {
            "modulation_inputs": tone_2_inputs,
            "expression_hint": tone_2_main["expression_hint"] if tone_2_main else "（soft toneなし）",
            "example": tone_2_main["example"] if tone_2_main else "（例なし）"
        }

        # tone_3出力
        tone_3 = {
            "modulation_inputs": tone_3_inputs,
            "expression_hint": tone_3_main["expression_hint"] if tone_3_main else "（hard toneなし）",
            "example": tone_3_main["example"] if tone_3_main else "（例なし）"
        }

        return {
            "base": tone_1,
            "tone_elements": {
                "tone_2": tone_2,
                "tone_3": tone_3
            }
        }
