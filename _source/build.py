#!/usr/bin/env python3
"""Générateur du site hiboumalin.fr (statique, sans dépendance).

Usage : python3 _source/build.py   (depuis la racine du dépôt)
Écrit les pages HTML à la racine du dépôt (servie par GitHub Pages).

LANCEMENT DE L'APPLI : passer APP_OUVERTE à True et renseigner APP_URL.
Tous les boutons « Rejoindre la liste d'attente » deviennent alors « Installer l'application ».
"""
import html, json, os, datetime

APP_OUVERTE = False
APP_URL = "https://app.hiboumalin.fr/"
SITE = "https://hiboumalin.fr"
YOUTUBE = "https://www.youtube.com/@HibouMalinJeuxsansecran"
CONTACT = "contact@hiboumalin.fr"

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = json.load(open(os.path.join(ROOT, "_source", "jeux.json"), encoding="utf-8"))
NOTIONS = {n["slug"]: n for n in DATA["notions"]}
JEUX = DATA["games"]
# Fiches publiées en entier sur le site (les autres : réservées à l'application)
PUBLIES = ["coucou-cache-du-hibou", "le-trieur", "robot-tartine", "hibou-chats-roux", "vrai-ou-invente"]
IMAGES = {"le-trieur", "robot-tartine", "hibou-chats-roux", "vrai-ou-invente"}

e = html.escape
PAGES = []  # pour le plan du site


def ages(j):
    a, b = j["age_min"], j["age_max"]
    return f"{a} – {b} ans" if a else f"0 – {b} ans"


def cta_href():
    return APP_URL if APP_OUVERTE else "/#inscription"


def cta_label(court=False):
    if APP_OUVERTE:
        return "Installer l'appli" if court else "Installer l'application"
    return "Liste d'attente" if court else "Rejoindre la liste d'attente"


NAV = [("/jeux/", "Les jeux"), ("/methode/", "La méthode"), ("/parents/", "Pour les parents"),
       ("/ecoles/", "Écoles et associations"), ("/faq/", "FAQ")]


def layout(path, title, description, body, active=None):
    nav = "".join(
        f'<a href="{h}"{" aria-current=page" if h == active else ""}>{e(t)}</a>' for h, t in NAV)
    canon = SITE + path
    PAGES.append(path)
    return f"""<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(description)}">
<link rel="canonical" href="{canon}">
<link rel="icon" href="/assets/img/favicon.png">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Houlou Débranché">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(description)}">
<meta property="og:url" content="{canon}">
<meta property="og:image" content="{SITE}/assets/img/hibou.png">
<meta name="theme-color" content="#FFF4E0">
<link rel="stylesheet" href="/assets/site.css">
</head>
<body>
<a class="skip" href="#contenu">Aller au contenu</a>
<header class="top"><div class="wrap">
  <a class="brand" href="/"><img src="/assets/img/favicon.png" alt="" width="40" height="40">Houlou Débranché</a>
  <button class="burger" aria-expanded="false" aria-controls="nav">Menu</button>
  <nav class="nav" id="nav" aria-label="Menu principal">{nav}<a class="cta" href="{cta_href()}">{e(cta_label(True))}</a></nav>
</div></header>
<main id="contenu">
{body}
</main>
<footer class="foot"><div class="wrap">
  <div class="cols">
    <div><a class="brand" href="/"><img src="/assets/img/favicon.png" alt="" width="40" height="40">Houlou Débranché</a>
      <p class="muted">Préparer les enfants de 0 à 10 ans à l'intelligence artificielle, par le jeu et sans écran.</p></div>
    <div><h4>Le site</h4><ul>
      <li><a href="/jeux/">Les jeux</a></li><li><a href="/methode/">La méthode</a></li>
      <li><a href="/parents/">Pour les parents</a></li><li><a href="/ecoles/">Écoles et associations</a></li>
      <li><a href="/faq/">Questions fréquentes</a></li><li><a href="/a-propos/">Qui sommes-nous</a></li></ul></div>
    <div><h4>Nous suivre</h4><ul>
      <li><a href="{YOUTUBE}" rel="noopener">YouTube : Jeux sans écran</a></li>
      <li><a href="mailto:{CONTACT}">{CONTACT}</a></li>
      <li><a href="/confidentialite/">Confidentialité et mentions légales</a></li></ul></div>
  </div>
  <p class="legal">© {datetime.date.today().year} Houlou Débranché, un projet de RLBX (SASU) · Ce site ne dépose aucun cookie et n'utilise aucun outil de mesure d'audience.</p>
</div></footer>
<script src="/assets/inscription.js" defer></script>
</body>
</html>
"""


def signup_block(titre="Rejoignez la liste d'attente", sous="L'application est en préparation. Inscrivez-vous pour être prévenu de l'ouverture et nous aider à la construire.", ident="inscription"):
    if APP_OUVERTE:
        return f"""<section id="{ident}" class="tight"><div class="wrap"><div class="card center">
<h2>L'application Houlou Débranché est disponible</h2>
<p class="lead">Un jeu sans écran par semaine, expliqué pas à pas, pour toute la famille.</p>
<div class="btns" style="justify-content:center"><a class="btn primary" href="{APP_URL}">Installer l'application</a></div>
</div></div></section>"""
    return f"""<section id="{ident}" class="tight"><div class="wrap"><div class="card signup">
<h2>{e(titre)}</h2>
<p class="muted">{e(sous)}</p>
<form class="signup-form" novalidate>
  <label class="f" for="email-{ident}">Votre adresse e-mail</label>
  <input type="email" id="email-{ident}" autocomplete="email" placeholder="vous@exemple.fr" required>
  <span class="f">L'âge de vos enfants</span>
  <div class="chips" role="group" aria-label="Âge de vos enfants">
    <label><input type="checkbox" name="age" value="0-3"><span>0 – 3 ans</span></label>
    <label><input type="checkbox" name="age" value="4-6"><span>4 – 6 ans</span></label>
    <label><input type="checkbox" name="age" value="7-10"><span>7 – 10 ans</span></label>
    <label><input type="checkbox" name="age" value="pro"><span>Je suis enseignant / animateur</span></label>
    <label><input type="checkbox" name="age" value="autre"><span>Autre</span></label>
  </div>
  <div class="hp" aria-hidden="true"><input type="text" name="email_address_check" tabindex="-1" autocomplete="off"></div>
  <label class="consent"><input type="checkbox" required>
    <span>J'accepte de recevoir les e-mails de Houlou Débranché au sujet de la liste d'attente et du lancement de l'application. Je peux me désinscrire à tout moment. <a href="/confidentialite/">Politique de confidentialité</a>.</span></label>
  <button type="submit">Je m'inscris</button>
  <div class="msg" role="status" aria-live="polite"></div>
</form>
</div></div></section>"""


def game_card(j):
    n = NOTIONS[j["notion_slug"]]
    pub = j["slug"] in PUBLIES
    if j["slug"] in IMAGES:
        img = f'<img src="/assets/img/{j["slug"]}.jpg" alt="" loading="lazy" width="600" height="600">'
    elif pub:
        img = '<img src="/assets/img/hibou-carre.png" alt="" loading="lazy" width="600" height="600">'
    else:
        img = ''
    badges = f'<span class="badge">{ages(j)}</span><span class="badge t">{e(n["name"])}</span>'
    if pub:
        badges += '<span class="badge free">Gratuit</span>'
    inner = f'{img}<div class="body"><div class="badges">{badges}</div><h3>{e(j["title"])}</h3><p class="muted small" style="margin:0">{e(n["short"])}</p></div>'
    data = f'data-ages="{j["age_min"]}-{j["age_max"]}"'
    if pub:
        return f'<a class="card game-card" {data} href="/jeux/{j["slug"]}/">{inner}</a>'
    return f'<div class="card game-card" {data}>{inner}</div>'


def write(path, content):
    out = os.path.join(ROOT, path.strip("/"), "index.html") if path != "/" else os.path.join(ROOT, "index.html")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, "w", encoding="utf-8").write(content)


# ---------------------------------------------------------------- Accueil
vedettes = [j for j in JEUX if j["slug"] in ["le-trieur", "robot-tartine", "hibou-chats-roux", "vrai-ou-invente"]]
notions_html = "".join(
    f'<div class="card notion"><h3>{e(n["name"])}</h3><p class="muted" style="margin:0">{e(n["short"])}</p></div>'
    for n in DATA["notions"])
accueil = f"""
<section style="padding:0"><div class="wrap hero">
  <div>
    <span class="eyebrow">Pour les enfants de 0 à 10 ans</span>
    <h1>Préparer vos enfants à l'IA… <em>sans écran.</em></h1>
    <p class="lead">Des jeux de 10 minutes, à faire en famille avec ce que vous avez à la maison, pour que vos enfants comprennent comment « pense » une machine et gardent toujours leur esprit critique.</p>
    <div class="btns"><a class="btn primary" href="{cta_href()}">{cta_label()}</a><a class="btn ghost" href="/jeux/">Voir les jeux</a></div>
  </div>
  <div class="owl"><img src="/assets/img/hibou.png" alt="Le hibou de Houlou Débranché" width="340" height="340"></div>
</div></section>

<section class="tight"><div class="wrap">
  <div class="grid g3">
    <div class="card"><div class="step-n">1</div><h3>Zéro écran pour l'enfant</h3><p class="muted" style="margin:0">L'application guide le parent. Le jeu, lui, se fait avec un foulard, des chaussettes, une tartine…</p></div>
    <div class="card"><div class="step-n">2</div><h3>10 minutes, une idée</h3><p class="muted" style="margin:0">Trier, donner des instructions, repérer une erreur, vérifier une information : une notion à chaque jeu.</p></div>
    <div class="card"><div class="step-n">3</div><h3>Pas besoin d'être expert</h3><p class="muted" style="margin:0">Chaque fiche explique ce que l'enfant vient de comprendre, et comment répondre à ses questions.</p></div>
  </div>
</div></section>

<section><div class="wrap">
  <div class="center"><span class="eyebrow">À essayer dès ce soir</span><h2>Quelques jeux de la collection</h2>
  <p class="lead">Les fiches complètes sont gratuites. Imprimez-les, ou suivez-les en vidéo sur notre chaîne.</p></div>
  <div class="grid g4" style="margin-top:22px">{"".join(game_card(j) for j in vedettes)}</div>
  <div class="btns" style="justify-content:center"><a class="btn ghost" href="/jeux/">Toute la collection</a><a class="btn ghost" href="{YOUTUBE}" rel="noopener">La chaîne YouTube</a></div>
</div></section>

<section><div class="wrap">
  <div class="center"><span class="eyebrow">La méthode</span><h2>8 idées simples pour comprendre l'IA</h2>
  <p class="lead">Ce qu'une machine sait faire, ce qu'elle ne sait pas faire, et ce qui reste à nous. Chaque jeu en fait vivre une.</p></div>
  <div class="grid g4" style="margin-top:22px">{notions_html}</div>
</div></section>

{signup_block()}

<section><div class="wrap"><div class="grid g2">
  <div class="card"><h3>Pour les parents</h3><p class="muted">Pourquoi en parler si tôt ? Comment répondre à « c'est quoi ChatGPT ? » Et les écrans, alors ?</p><a href="/parents/">Lire la page parents →</a></div>
  <div class="card"><h3>Pour les écoles, crèches et associations</h3><p class="muted">Des ateliers débranchés, faciles à animer en groupe, qui s'inscrivent dans ce que l'école commence à enseigner.</p><a href="/ecoles/">Découvrir →</a></div>
</div></div></section>
"""
write("/", layout("/", "Houlou Débranché – Préparer vos enfants à l'IA, sans écran",
                  "Des jeux de 10 minutes, sans écran, pour que les enfants de 0 à 10 ans comprennent comment pense une machine. Fiches gratuites et application en préparation.",
                  accueil))

# ---------------------------------------------------------------- Catalogue
filtres = ('<div class="filters" role="group" aria-label="Filtrer par âge">'
           '<button data-f="all" aria-pressed="true">Tous</button>'
           '<button data-f="0-3" aria-pressed="false">0 – 3 ans</button>'
           '<button data-f="4-6" aria-pressed="false">4 – 6 ans</button>'
           '<button data-f="7-10" aria-pressed="false">7 – 10 ans</button></div>')
catalogue = f"""
<section><div class="wrap">
  <span class="eyebrow">{len(JEUX)} jeux, et d'autres à venir</span>
  <h1>Les jeux Houlou Débranché</h1>
  <p class="lead">Chaque jeu dure une dizaine de minutes, se joue sans écran et fait comprendre une idée sur l'intelligence artificielle. Les fiches marquées « Gratuit » sont à vous dès maintenant ; les autres arrivent avec l'application.</p>
  <h2 style="margin-top:28px">Les fiches gratuites</h2>
  <div class="grid g5" style="margin-top:14px">{"".join(game_card(j) for j in JEUX if j["slug"] in PUBLIES)}</div>
  <h2 style="margin-top:40px">Bientôt dans l'application</h2>
  {filtres}
  <div class="grid g3">{"".join(game_card(j) for j in JEUX if j["slug"] not in PUBLIES)}</div>
</div></section>
{signup_block("Recevez les nouveaux jeux", "Inscrivez-vous à la liste d'attente : vous serez prévenu à l'ouverture de l'application, avec un jeu sans écran chaque semaine.")}
"""
write("/jeux/", layout("/jeux/", "Les jeux sans écran pour comprendre l'IA – Houlou Débranché",
                       "Le catalogue des jeux Houlou Débranché : des activités sans écran de 10 minutes, par âge, pour expliquer l'intelligence artificielle aux enfants de 0 à 10 ans.",
                       catalogue, "/jeux/"))

# ---------------------------------------------------------------- Fiches
for j in JEUX:
    if j["slug"] not in PUBLIES:
        continue
    n = NOTIONS[j["notion_slug"]]
    img = (f'<img src="/assets/img/{j["slug"]}.jpg" alt="Illustration du jeu {e(j["title"])}" width="600" height="600">'
           if j["slug"] in IMAGES else '<img src="/assets/img/hibou.png" alt="Le hibou de Houlou Débranché" width="340" height="340" style="border-radius:50%;max-width:340px">')
    mats = "".join(f"<li>{e(m)}</li>" for m in j["materials"])
    steps = "".join(f"<li>{e(s)}</li>" for s in j["steps"])
    autres = [x for x in JEUX if x["slug"] in PUBLIES and x["slug"] != j["slug"]][:3]
    fiche = f"""
<section><div class="wrap">
  <p class="small"><a href="/jeux/">← Tous les jeux</a></p>
  <div class="fiche">
    <div>{img}</div>
    <div>
      <div class="badges"><span class="badge">{ages(j)}</span><span class="badge">{j["duration_min"]} min</span><span class="badge t">{e(n["name"])}</span><span class="badge free">Gratuit</span></div>
      <h1 style="font-size:clamp(30px,4.4vw,44px)">{e(j["title"])}</h1>
      <h3>Il vous faut</h3><ul>{mats}</ul>
      <h3>Comment jouer</h3><ol>{steps}</ol>
      <div class="box"><b>Pour varier</b>{e(j["variant"])}</div>
      <div class="box t"><b>Ce que votre enfant a compris</b>{e(j["child_takeaway"])}</div>
      <div class="box"><b>Le mot pour les parents</b>{e(j["parent_note"])}</div>
      <div class="box t"><b>S'il vous pose la question qui pique</b>{e(j["hard_question"])}</div>
      <p class="muted small">Compétence travaillée : {e(j["human_skill"])}.</p>
    </div>
  </div>
</div></section>
<section class="tight"><div class="wrap"><h2>D'autres jeux gratuits</h2>
  <div class="grid g3" style="margin-top:14px">{"".join(game_card(x) for x in autres)}</div></div></section>
{signup_block("Un jeu comme celui-ci chaque semaine", "Inscrivez-vous à la liste d'attente de l'application Houlou Débranché.")}
"""
    p = f"/jeux/{j['slug']}/"
    write(p, layout(p, f"{j['title']} – jeu sans écran pour comprendre l'IA ({ages(j)}) – Houlou Débranché",
                    f"{j['title']} : un jeu sans écran de {j['duration_min']} minutes pour expliquer « {n['name'].lower()} » aux enfants de {ages(j)}. {j['child_takeaway']}",
                    fiche, "/jeux/"))

# ---------------------------------------------------------------- Méthode
methode = f"""
<section><div class="wrap prose">
  <span class="eyebrow">La méthode</span>
  <h1>Comprendre avant d'utiliser</h1>
  <p class="lead">Houlou Débranché ne met pas les enfants devant une intelligence artificielle. Il leur fait vivre, avec leur corps et des objets du quotidien, les quelques idées qui permettent de comprendre ce qu'est une machine qui « apprend ».</p>
  <h2>Le principe : l'enfant joue la machine, ou la dresse</h2>
  <p>Dans la plupart des jeux, le parent fait la machine et l'enfant lui donne des exemples, des règles ou des instructions. Il voit la machine réussir, se tromper, être corrigée. Puis on inverse les rôles. C'est ainsi que l'idée s'installe : par l'expérience, pas par un discours.</p>
  <h2>Une progression de 0 à 10 ans</h2>
  <p>Avant 3 ans, on joue avec les régularités et l'anticipation. De 3 à 6 ans, on trie, on suit et on donne des instructions. Après 6 ans, on parle de hasard, d'erreur, de vrai et de faux, et de ce qu'on ne confie pas à une machine.</p>
  <h2>Les 8 idées</h2>
</div>
<div class="wrap"><div class="grid g4" style="margin-top:10px">{notions_html}</div></div>
<div class="wrap prose">
  <h2>Ce que nous ne faisons pas</h2>
  <p>Pas d'écran pour l'enfant, pas d'intelligence artificielle générative dans l'application, pas de compte enfant, pas de publicité ni de traqueur. L'application s'adresse au parent, qui joue ensuite avec son enfant.</p>
</div></section>
{signup_block()}
"""
write("/methode/", layout("/methode/", "La méthode Houlou Débranché – comprendre l'IA par le jeu, sans écran",
                          "Comment Houlou Débranché explique l'intelligence artificielle aux enfants : 8 idées simples, une progression de 0 à 10 ans, des jeux où l'enfant joue la machine.",
                          methode, "/methode/"))

# ---------------------------------------------------------------- Parents
parents = f"""
<section><div class="wrap prose">
  <span class="eyebrow">Pour les parents</span>
  <h1>Parler d'IA à son enfant, sans écran et sans être expert</h1>
  <p class="lead">Vos enfants grandissent avec des assistants vocaux, des recommandations de vidéos et des outils qui répondent à tout. Ils n'ont pas besoin de s'en servir tôt. Ils ont besoin de comprendre tôt.</p>
  <h2>Pourquoi si tôt ?</h2>
  <p>Les idées de base, comme « une machine apprend avec des exemples » ou « elle peut se tromper en ayant l'air sûre d'elle », se comprennent très bien dès la maternelle, à condition de les vivre par le jeu. Un enfant qui les a comprises posera les bonnes questions le jour où il utilisera ces outils.</p>
  <h2>Et les écrans ?</h2>
  <p>Houlou Débranché ne demande aucun écran à l'enfant : l'application sert au parent, pour préparer le jeu. C'est un choix de départ, cohérent avec les recommandations publiques sur les jeunes enfants, qui rappellent notamment que les écrans n'ont pas leur place avant 3 ans dans les lieux d'accueil de la petite enfance (<a href="https://www.info.gouv.fr/actualite/les-ecrans-interdits-dans-les-lieux-daccueil-pour-jeunes-enfants" rel="noopener">info.gouv.fr</a>).</p>
  <h2>Ce que l'école commence à faire</h2>
  <p>L'Éducation nationale a publié en 2025 un cadre d'usage de l'IA en éducation (<a href="https://www.ac-paris.fr/l-ia-en-education-cadre-d-usage-132788" rel="noopener">présentation par l'académie de Paris</a>). À l'école primaire, l'accent est mis sur la compréhension plutôt que sur l'usage par les élèves. Houlou Débranché va dans le même sens, à la maison.</p>
  <h2>« C'est quoi, ChatGPT ? » : trois réponses simples</h2>
  <ul>
    <li><b>Avant 6 ans :</b> « C'est une machine qui a lu énormément de textes et qui devine les mots qui vont ensemble. »</li>
    <li><b>Vers 7 ans :</b> « Elle ne sait pas vraiment les choses : elle devine. Parfois elle se trompe, alors on vérifie. »</li>
    <li><b>Vers 9-10 ans :</b> « Elle a appris avec des exemples écrits par des gens. Si les exemples sont incomplets, ses réponses le seront aussi. »</li>
  </ul>
  <p>Chaque fiche de jeu propose aussi une « réponse à la question qui pique », pour ne jamais être pris de court.</p>
  <p><a class="btn ghost" href="/jeux/">Essayer un jeu gratuit</a></p>
</div></section>
{signup_block()}
"""
write("/parents/", layout("/parents/", "Expliquer l'intelligence artificielle à son enfant – Houlou Débranché",
                          "Pourquoi et comment parler d'IA à un enfant de 0 à 10 ans, sans écran : idées clés, recommandations publiques et réponses simples aux questions des enfants.",
                          parents, "/parents/"))

# ---------------------------------------------------------------- Écoles
ecoles = f"""
<section><div class="wrap prose">
  <span class="eyebrow">Écoles, crèches, centres de loisirs, associations</span>
  <h1>Des ateliers débranchés sur l'IA, faciles à animer</h1>
  <p class="lead">Les jeux Houlou Débranché fonctionnent aussi en groupe : pas de matériel informatique, des objets du quotidien, 10 à 20 minutes par atelier.</p>
  <h2>Pour qui ?</h2>
  <p>Enseignants de maternelle et d'élémentaire, professionnels de la petite enfance, animateurs de centres de loisirs, médiathèques, associations de parents et structures de soutien à la parentalité.</p>
  <h2>Ce que nous préparons</h2>
  <ul>
    <li>des fiches d'atelier adaptées au groupe (10 à 25 enfants) ;</li>
    <li>des affiches et des cartes à imprimer ;</li>
    <li>un déroulé pour une réunion de parents « Parler d'IA en famille ».</li>
  </ul>
  <h2>Vous êtes intéressé ?</h2>
  <p>Écrivez-nous à <a href="mailto:{CONTACT}?subject=Ateliers%20Hibou%20Malin">{CONTACT}</a> en précisant votre structure et l'âge des enfants, ou inscrivez-vous ci-dessous en cochant « Je suis enseignant / animateur ».</p>
</div></section>
{signup_block("Être prévenu des ressources pour les groupes", "Nous vous enverrons les fiches d'atelier dès qu'elles seront prêtes.")}
"""
write("/ecoles/", layout("/ecoles/", "Ateliers sans écran sur l'IA pour écoles et associations – Houlou Débranché",
                         "Des ateliers débranchés pour expliquer l'intelligence artificielle aux enfants en groupe : écoles, crèches, centres de loisirs, médiathèques et associations.",
                         ecoles, "/ecoles/"))

# ---------------------------------------------------------------- FAQ
faq_items = [
    ("Mon enfant va-t-il utiliser un écran ?", "Non. L'application est faite pour le parent : elle explique le jeu, le matériel et ce que l'enfant va comprendre. Le jeu se fait ensuite sans écran, avec des objets de la maison."),
    ("À partir de quel âge ?", "Dès la naissance pour les tout premiers jeux (anticipation, régularités), puis jusqu'à 10 ans. Chaque jeu indique la tranche d'âge conseillée."),
    ("Faut-il s'y connaître en informatique ?", "Pas du tout. Chaque fiche explique l'idée en quelques phrases simples, et propose une réponse aux questions difficiles des enfants."),
    ("L'application utilise-t-elle de l'intelligence artificielle ?", "Non. Houlou Débranché explique l'IA, mais n'en utilise pas : pas d'IA générative, pas de profilage, pas de publicité."),
    ("Quand l'application sera-t-elle disponible ?", "Elle est en préparation. Les inscrits à la liste d'attente seront prévenus les premiers, et pourront donner leur avis pour la construire."),
    ("Combien coûtera-t-elle ?", "Une partie des jeux restera gratuite, comme les fiches déjà publiées sur ce site. Le prix de l'accès complet sera fixé après avoir consulté les inscrits à la liste d'attente."),
    ("Mes données sont-elles protégées ?", "Nous ne demandons que votre e-mail et, si vous le souhaitez, l'âge de vos enfants (sans nom ni date de naissance). Aucune donnée n'est vendue. Détails sur la page Confidentialité."),
    ("Puis-je utiliser les jeux en classe ?", "Oui, les fiches gratuites peuvent être utilisées en classe ou en atelier. Des versions adaptées aux groupes sont en préparation : voir la page Écoles et associations."),
]
faq = f"""
<section><div class="wrap prose">
  <span class="eyebrow">Questions fréquentes</span>
  <h1>Vos questions</h1>
  {"".join(f"<details><summary>{e(q)}</summary><p>{e(r)}</p></details>" for q, r in faq_items)}
  <p>Une autre question ? Écrivez-nous à <a href="mailto:{CONTACT}">{CONTACT}</a>.</p>
</div></section>
{signup_block()}
"""
write("/faq/", layout("/faq/", "Questions fréquentes – Houlou Débranché",
                      "Écrans, âge, prix, données personnelles : les réponses aux questions fréquentes sur Houlou Débranché et ses jeux sans écran pour comprendre l'IA.",
                      faq, "/faq/"))

# ---------------------------------------------------------------- À propos
apropos = f"""
<section><div class="wrap prose">
  <span class="eyebrow">Qui sommes-nous</span>
  <h1>Houlou Débranché</h1>
  <p class="lead">Houlou Débranché est né d'une conviction : nos enfants vivront avec l'intelligence artificielle, et le meilleur moyen de les y préparer n'est pas de les mettre devant un écran, mais de les aider à comprendre.</p>
  <p>Le projet est porté par RLBX, une société nantaise qui conçoit des outils numériques. Les jeux sont conçus pour être simples, joyeux et justes sur le fond : chaque fiche explique une vraie notion, sans jargon et sans exagération.</p>
  <p>Vous pouvez suivre les jeux en vidéo sur notre <a href="{YOUTUBE}" rel="noopener">chaîne YouTube « Jeux sans écran »</a>, et nous écrire à <a href="mailto:{CONTACT}">{CONTACT}</a>.</p>
</div></section>
{signup_block()}
"""
write("/a-propos/", layout("/a-propos/", "Qui sommes-nous – Houlou Débranché", "Houlou Débranché, un projet de RLBX pour préparer les enfants à l'intelligence artificielle par le jeu, sans écran.", apropos))

# ---------------------------------------------------------------- Merci (après confirmation)
merci = f"""
<section><div class="wrap center">
  <img src="/assets/img/hibou.png" alt="" width="180" height="180" style="border-radius:50%">
  <h1>Bienvenue dans le nid !</h1>
  <p class="lead">Votre inscription est confirmée. Vous serez parmi les premiers prévenus de l'ouverture de l'application Houlou Débranché.</p>
  <p class="lead">En attendant, un jeu à essayer ce soir :</p>
  <div class="btns" style="justify-content:center"><a class="btn primary" href="/jeux/robot-tartine/">Le robot-tartine</a><a class="btn ghost" href="{YOUTUBE}" rel="noopener">Nos vidéos</a></div>
</div></section>
"""
html_merci = layout("/merci/", "Inscription confirmée – Houlou Débranché", "Votre inscription à la liste d'attente Houlou Débranché est confirmée.", merci)
write("/merci/", html_merci.replace('<meta name="theme-color"', '<meta name="robots" content="noindex"><meta name="theme-color"'))
PAGES.remove("/merci/")

# ---------------------------------------------------------------- Confidentialité
conf = f"""
<section><div class="wrap prose">
  <h1>Confidentialité et mentions légales</h1>
  <h2>Éditeur</h2>
  <p>Houlou Débranché est un projet de la société RLBX, SASU, SIREN 995 302 668, 4 rue Félix Ménétrier, 44300 Nantes, France. Directeur de la publication : Régis Lagos. Contact : <a href="mailto:{CONTACT}">{CONTACT}</a>.</p>
  <h2>Hébergement</h2>
  <p>Ce site est hébergé par GitHub Inc. (GitHub Pages), 88 Colin P. Kelly Jr. Street, San Francisco, CA 94107, États-Unis.</p>
  <h2>Données collectées</h2>
  <p>Lors de l'inscription à la liste d'attente, nous collectons : votre adresse e-mail, les tranches d'âge de vos enfants (si vous les indiquez) et la provenance de votre visite (par exemple, la chaîne vidéo qui vous a amené). Nous ne collectons aucune donnée sur vos enfants eux-mêmes (ni nom, ni date de naissance).</p>
  <h2>Pourquoi</h2>
  <p>Pour vous prévenir de l'ouverture de l'application Houlou Débranché, vous envoyer des nouvelles du projet et, éventuellement, vous demander votre avis pour la construire. La base légale est votre consentement, que vous donnez en cochant la case du formulaire puis en confirmant votre adresse.</p>
  <h2>Durée de conservation</h2>
  <p>Jusqu'au lancement de l'application plus 6 mois, ou jusqu'à votre désinscription si elle intervient avant.</p>
  <h2>Destinataires et sous-traitant</h2>
  <p>Vos données ne sont ni vendues ni cédées. Elles sont gérées pour notre compte par Brevo (Sendinblue SAS, France), notre prestataire d'envoi d'e-mails, qui agit selon nos instructions.</p>
  <h2>Vos droits</h2>
  <p>Vous pouvez vous désinscrire à tout moment grâce au lien présent dans chaque e-mail. Vous disposez aussi d'un droit d'accès, de rectification et d'effacement de vos données : écrivez-nous à <a href="mailto:{CONTACT}">{CONTACT}</a>. Vous pouvez également adresser une réclamation à la CNIL (cnil.fr).</p>
  <h2>Cookies et mesure d'audience</h2>
  <p>Ce site ne dépose aucun cookie et n'utilise aucun outil de mesure d'audience ou de publicité. Une information technique (la chaîne d'origine de votre visite) est conservée dans votre navigateur le temps de la visite seulement, pour l'associer à votre inscription.</p>
</div></section>
"""
write("/confidentialite/", layout("/confidentialite/", "Confidentialité et mentions légales – Houlou Débranché",
                                  "Mentions légales et politique de confidentialité du site Houlou Débranché.", conf))

# Ancienne adresse de la page de confidentialité
open(os.path.join(ROOT, "confidentialite.html"), "w", encoding="utf-8").write(
    '<!doctype html><meta charset="utf-8"><meta http-equiv="refresh" content="0; url=/confidentialite/"><link rel="canonical" href="/confidentialite/">')

# ---------------------------------------------------------------- 404, robots, sitemap
nf = layout("/404", "Page introuvable – Houlou Débranché", "Cette page n'existe pas.",
            '<section><div class="wrap center"><h1>Oups, le hibou s\'est perdu</h1><p class="lead">Cette page n\'existe pas ou plus.</p><div class="btns" style="justify-content:center"><a class="btn primary" href="/">Retour à l\'accueil</a></div></div></section>')
PAGES.remove("/404")
open(os.path.join(ROOT, "404.html"), "w", encoding="utf-8").write(nf)
open(os.path.join(ROOT, "robots.txt"), "w").write(f"User-agent: *\nAllow: /\nDisallow: /merci/\nSitemap: {SITE}/sitemap.xml\n")
today = datetime.date.today().isoformat()
sm = "".join(f"<url><loc>{SITE}{p}</loc><lastmod>{today}</lastmod></url>" for p in PAGES)
open(os.path.join(ROOT, "sitemap.xml"), "w").write(
    f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{sm}</urlset>\n')
print("Pages :", len(PAGES) + 2, "→", ", ".join(PAGES))
