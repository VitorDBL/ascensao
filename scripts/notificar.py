import os, datetime, urllib.request, zoneinfo
tz = zoneinfo.ZoneInfo("America/Sao_Paulo")
hoje = datetime.datetime.now(tz).date()
inicio = datetime.date(2026, 11, 9)
n = (hoje - inicio).days + 1
noite = os.environ.get("EVENT_SCHEDULE", "") == "30 23 * * *"
dow = hoje.weekday()  # 0 = segunda
quests = {0: "kickboxing", 1: "Superior A na academia", 2: "kickboxing", 3: "Inferior + core na academia",
          4: "Superior B na academia", 5: "desafio em casa (e refeição livre)", 6: "treino em casa"}
especiais = {datetime.date(2026, 11, 11): "Inferior + core na academia",
             datetime.date(2026, 11, 12): "kickboxing",
             datetime.date(2026, 11, 13): "Superior B na academia"}
quest = especiais.get(hoje, quests[dow])

def h32(n):
    M = 0xffffffff
    x = ((n ^ 0x9e3779b9) & M) * 2654435761 & M
    x ^= x >> 15; x = x * 2246822519 & M; x ^= x >> 13; x = x * 3266489917 & M; x ^= x >> 16
    return x

EXCL = {datetime.date(2026, 11, 14), datetime.date(2026, 11, 21), datetime.date(2026, 11, 28),
        datetime.date(2026, 12, 5), datetime.date(2026, 12, 26), datetime.date(2027, 1, 2)}
def _kick_days():
    by_m, out = {}, []
    for k in range(6, 180):
        d = inicio + datetime.timedelta(days=k - 1)
        if d.weekday() != 5 or k % 30 == 0 or d in EXCL:
            continue
        by_m.setdefault(d.year * 12 + (d.month - 1), []).append(k)
    for m in sorted(by_m):
        c = [k for k in by_m[m] if not out or k - out[-1] >= 14]
        if c:
            out.append(c[h32(m * 7 + 5) % len(c)])
    return set(out)
KICK = _kick_days()
def kick_sabado(k):
    return k in KICK
if n < 1:
    titulo, msg = "Físico dos Deuses", "A campanha ainda não começou."
elif n > 180:
    titulo, msg = "Campanha concluída", "Os 180 dias acabaram. Abra o app para ver sua retrospectiva e começar a próxima temporada."
elif noite:
    titulo, msg = "Sistema", f"Dia {n} de 180. Já registrou o dia? Conte ao Sistema o que treinou e comeu antes de dormir."
    if kick_sabado(n + 1):
        msg = f"Dia {n} de 180. Sinal detectado para amanhã cedo. Conclua a quest de hoje no app para revelar o boss de sábado."
else:
    chefe = " Hoje é dia de CHEFÃO." if n % 30 == 0 else ""
    titulo, msg = "Bom dia, Vitor", f"Dia {n} de 180: {quest}.{chefe} Abra o app e faça o check-in."
import urllib.parse
qs = urllib.parse.urlencode({"title": titulo, "click": os.environ["APP_URL"], "tags": "crossed_swords"})
req = urllib.request.Request("https://ntfy.sh/" + os.environ["NTFY_TOPIC"] + "?" + qs, data=msg.encode("utf-8"), method="POST",
                             headers={"Content-Type": "text/plain; charset=utf-8"})
urllib.request.urlopen(req, timeout=20)
print("enviado:", titulo, "|", msg)
