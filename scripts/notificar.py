import os, json, datetime, urllib.request, zoneinfo
tz = zoneinfo.ZoneInfo("America/Sao_Paulo")
agora = datetime.datetime.now(tz)
hoje = agora.date()
inicio = datetime.date(2026, 11, 9)
quests = {0: "kickboxing", 1: "Superior A na academia", 2: "kickboxing", 3: "Inferior + core na academia",
          4: "Superior B na academia", 5: "desafio em casa (e refeição livre)", 6: "treino em casa"}
especiais = {datetime.date(2026, 11, 11): "Superior B na academia",
             datetime.date(2026, 11, 12): "kickboxing",
             datetime.date(2026, 11, 13): "Inferior + core na academia"}

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
import urllib.parse

def mensagem(dia, noite):
    n = (dia - inicio).days + 1
    if n < 1:
        return None
    if n > 180:
        return None if noite or n > 181 else ("Campanha concluída", "Os 180 dias acabaram. Abra o app para ver sua retrospectiva e começar a próxima temporada.")
    if noite:
        if kick_sabado(n + 1):
            return ("Sistema", f"Dia {n} de 180. Sinal detectado para amanhã cedo. Conclua a quest de hoje no app para revelar o boss de sábado.")
        return ("Sistema", f"Dia {n} de 180. Já registrou o dia? Conte ao Sistema o que treinou e comeu antes de dormir.")
    quest = especiais.get(dia, quests[dia.weekday()])
    chefe = " Hoje é dia de CHEFÃO." if n % 30 == 0 else ""
    return ("Bom dia, Vitor", f"Dia {n} de 180: {quest}.{chefe} Abra o app e faça o check-in.")

def ja_agendadas():
    try:
        url = "https://ntfy.sh/" + os.environ["NTFY_TOPIC"] + "/json?poll=1&scheduled=1&since=all"
        linhas = urllib.request.urlopen(url, timeout=20).read().decode("utf-8").splitlines()
        return {(j.get("time"), j.get("message")) for j in map(json.loads, linhas) if j.get("event") == "message"}
    except Exception as e:
        print("não consegui ler os agendados:", e)
        return set()
AGENDADAS = None

def enviar(titulo, msg, quando=None):
    global AGENDADAS
    if quando is not None:
        if AGENDADAS is None:
            AGENDADAS = ja_agendadas()
        if (int(quando.timestamp()), msg) in AGENDADAS:
            print("já estava agendado:", quando.isoformat(), "|", msg)
            return
    params = {"title": titulo, "click": os.environ["APP_URL"], "tags": "crossed_swords"}
    if quando is not None:
        params["at"] = str(int(quando.timestamp()))
    req = urllib.request.Request("https://ntfy.sh/" + os.environ["NTFY_TOPIC"] + "?" + urllib.parse.urlencode(params),
                                 data=msg.encode("utf-8"), method="POST", headers={"Content-Type": "text/plain; charset=utf-8"})
    urllib.request.urlopen(req, timeout=20)
    print("enviado" if quando is None else "agendado para " + quando.isoformat(), "|", titulo, "|", msg)

# O agendamento do GitHub atrasa horas. Por isso, uma execução por dia (à tarde) deixa as mensagens
# agendadas no próprio ntfy: a da noite de hoje (20h30) e a da manhã de amanhã (7h40).
if os.environ.get("MODO") == "agora":
    m = mensagem(hoje, False)
    if m:
        enviar(*m)
else:
    noite_hoje = datetime.datetime.combine(hoje, datetime.time(20, 30), tz)
    m = mensagem(hoje, True)
    if m and agora < noite_hoje:
        enviar(*m, quando=noite_hoje)
    elif m and agora.hour < 23:
        enviar(*m)
    amanha = hoje + datetime.timedelta(days=1)
    m = mensagem(amanha, False)
    if m:
        enviar(*m, quando=datetime.datetime.combine(amanha, datetime.time(7, 40), tz))
