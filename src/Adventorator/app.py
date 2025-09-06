# app.py

from fastapi import FastAPI, Request, HTTPException
from Adventorator.logging import setup_logging
from Adventorator.config import load_settings
from Adventorator.crypto import verify_ed25519
from Adventorator.discord_schemas import Interaction
from Adventorator.responder import respond_pong, respond_deferred, followup_message
from Adventorator.rules.dice import DiceRNG
from Adventorator.rules.checks import CheckInput, compute_check
import structlog
import asyncio

rng = DiceRNG()  # TODO: Seed per-scene later

log = structlog.get_logger()
settings = load_settings()
setup_logging()
app = FastAPI(title="Adventorator")

DISCORD_SIG_HEADER = "X-Signature-Ed25519"
DISCORD_TS_HEADER = "X-Signature-Timestamp"

@app.post("/interactions")
async def interactions(request: Request):
    raw = await request.body()
    sig = request.headers.get(DISCORD_SIG_HEADER)
    ts  = request.headers.get(DISCORD_TS_HEADER)
    if not sig or not ts:
        raise HTTPException(status_code=401, detail="missing signature headers")

    if not verify_ed25519(settings.discord_public_key, ts, raw, sig):
        raise HTTPException(status_code=401, detail="bad signature")

    inter = Interaction.model_validate_json(raw)

    # Ping = 1
    if inter.type == 1:
        return respond_pong()

    # Anything else: immediately DEFER (type 5) to satisfy the 3s budget.

    if inter.type == 2 and inter.data and inter.data.name:
        asyncio.create_task(_dispatch_command(inter))
    return respond_deferred()

async def _dispatch_command(inter: Interaction):
    name = inter.data.name
    if name == "roll":
        # expect option "expr"
        expr = _option(inter, "expr", default="1d20")
        adv = bool(_option(inter, "advantage", default=False))
        dis = bool(_option(inter, "disadvantage", default=False))
        res = rng.roll(expr, advantage=adv, disadvantage=dis)
        text = f"🎲 `{expr}` → rolls {res.rolls} {'(adv)' if adv else '(dis)' if dis else ''} = **{res.total}**"
        await followup_message(inter.application_id, inter.token, text)
    elif name == "check":
        # options: ability, score, proficient, expertise, prof_bonus, dc, advantage, disadvantage
        ability = _option(inter, "ability", default="DEX").upper()
        score = int(_option(inter, "score", default=10))
        prof = bool(_option(inter, "proficient", default=False))
        exp  = bool(_option(inter, "expertise", default=False))
        pb   = int(_option(inter, "prof_bonus", default=2))
        dc   = int(_option(inter, "dc", default=15))
        adv  = bool(_option(inter, "advantage", default=False))
        dis  = bool(_option(inter, "disadvantage", default=False))

        # d20 (1 or 2 rolls depending on adv/dis)
        res_roll = rng.roll("1d20", advantage=adv, disadvantage=dis)
        ci = CheckInput(ability=ability, score=score, proficient=prof, expertise=exp,
                        proficiency_bonus=pb, dc=dc, advantage=adv, disadvantage=dis)
        out = compute_check(ci, res_roll.rolls[:2] if len(res_roll.rolls) >= 2 else [res_roll.rolls[0]])
        verdict = "✅ success" if out.success else "❌ fail"
        text = (
            f"🧪 **{ability}** check vs DC {dc}\n"
            f"• d20: {out.d20} → pick {out.pick}\n"
            f"• mod: {out.mod:+}\n"
            f"= **{out.total}** → {verdict}"
        )
        await followup_message(inter.application_id, inter.token, text)
    else:
        await followup_message(inter.application_id, inter.token, f"Unknown command: {name}", ephemeral=True)

def _option(inter: Interaction, name: str, default=None):
    if not inter.data or not inter.data.options:
        return default
    for opt in inter.data.options:
        if opt.get("name") == name:
            return opt.get("value", default)
    return default
