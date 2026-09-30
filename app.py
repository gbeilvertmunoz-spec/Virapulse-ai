"""ViralPulse AI - V1 (Streamlit). Lancer : streamlit run app.py"""
import html, json, re, time, random
from datetime import datetime, timedelta
import numpy as np
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

APP = "ViralPulse AI"
PAGES = ["📊 Dashboard", "🎯 Scanner de Niche", "💰 Tarifs", "⚖️ Légal & CGU"]
PLANS = {
    "Free Trial": {"price": "0€", "per": "7 jours", "color": "#9D4EDD",
                   "feats": ["3 scans inclus", "Accès limité", "Scripts basiques", "Support communautaire"]},
    "Creator Pro": {"price": "29€", "per": "/mois", "color": "#00F5D4",
                    "feats": ["Scans illimités", "IA de script avancée", "Support 24/7", "Historique complet"]},
    "Agency Elite": {"price": "79€", "per": "/mois", "color": "#FF007F",
                     "feats": ["Multi-comptes", "Exports CSV de masse", "Insights exclusifs", "Tout Creator Pro"]},
}

st.set_page_config(page_title=f"{APP} | Trends & Scripts viraux TikTok Reels Shorts",
                   page_icon="⚡", layout="wide", initial_sidebar_state="expanded")

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
:root{--bg:#0B0F17;--violet:#9D4EDD;--cyan:#00F5D4;--rose:#FF007F;--txt:#EAF0FF;--mut:#A9B4CC}
html,body,[class*="css"],.stApp{font-family:'Inter',sans-serif!important;color:var(--txt)}
.stApp{background:radial-gradient(circle at 15% 0%,#1a1033 0%,var(--bg) 45%)!important}
header[data-testid="stHeader"]{background:transparent}
#MainMenu,footer{visibility:hidden}
section[data-testid="stSidebar"]{background:rgba(15,20,32,.85)!important;backdrop-filter:blur(14px);
  border-right:1px solid rgba(157,78,221,.4)}
.logo{font-size:1.5rem;font-weight:800;color:var(--violet);text-shadow:0 0 12px var(--violet),0 0 28px rgba(157,78,221,.6);margin-bottom:.4rem}
.glass{background:rgba(255,255,255,.04);backdrop-filter:blur(12px);border-radius:16px;padding:1.2rem;
  border:1px solid transparent;background-clip:padding-box;position:relative;
  box-shadow:0 0 24px rgba(157,78,221,.25);margin-bottom:1rem}
.glass::before{content:"";position:absolute;inset:0;border-radius:16px;padding:1px;
  background:linear-gradient(135deg,var(--violet),var(--cyan),var(--rose));
  -webkit-mask:linear-gradient(#000 0 0) content-box,linear-gradient(#000 0 0);
  -webkit-mask-composite:xor;mask-composite:exclude;pointer-events:none}
.kpi-l{color:var(--mut);font-size:.85rem;text-transform:uppercase;letter-spacing:.06em}
.kpi-v{font-size:2.2rem;font-weight:800;color:var(--cyan);text-shadow:0 0 14px rgba(0,245,212,.6)}
.kpi-d{color:var(--mut);font-size:.8rem}
h1,h2,h3{color:var(--txt)!important;font-weight:800!important}
.stButton>button,.stDownloadButton>button{border-radius:16px;border:1px solid var(--violet);
  background:rgba(157,78,221,.12);color:var(--txt);font-weight:600;transition:.2s}
.stButton>button:hover,.stDownloadButton>button:hover{border-color:var(--cyan);box-shadow:0 0 18px rgba(0,245,212,.5);color:var(--cyan)}
.stButton>button[kind="primary"]{background:linear-gradient(135deg,var(--cyan),#00c4a7);color:#04110f;border:0;
  box-shadow:0 0 22px rgba(0,245,212,.55)}
.stProgress>div>div>div>div{background:linear-gradient(90deg,var(--violet),var(--cyan),var(--rose));box-shadow:0 0 14px var(--cyan)}
.stTextInput input,.stTextArea textarea,div[data-baseweb="select"]>div{border-radius:16px!important;
  background:rgba(255,255,255,.05)!important;border:1px solid rgba(157,78,221,.5)!important;color:var(--txt)!important}
.price{font-size:2.6rem;font-weight:800}
.badge{display:inline-block;border-radius:999px;padding:.15rem .8rem;font-size:.75rem;font-weight:700;
  border:1px solid var(--cyan);color:var(--cyan)}
.badge.r{border-color:var(--rose);color:var(--rose)}
.cookie{position:fixed;bottom:16px;right:16px;max-width:380px;z-index:999}
.e404{text-align:center;font-size:6rem;font-weight:800;color:var(--rose);text-shadow:0 0 30px var(--rose)}
ul.f{list-style:none;padding:0;color:var(--txt)} ul.f li:before{content:"✔ ";color:var(--cyan)}
.stMarkdown p,.stMarkdown li{line-height:1.75;font-size:1rem;color:#EAF0FF}
.stMarkdown table{width:100%;border-collapse:separate;border-spacing:0;border:1px solid rgba(157,78,221,.5);border-radius:16px;overflow:hidden;margin:1rem 0}
.stMarkdown th{background:rgba(157,78,221,.25);color:#00F5D4;padding:.7rem;text-align:left}
.stMarkdown td{padding:.7rem;border-top:1px solid rgba(255,255,255,.08)}
.stMarkdown a{color:#00F5D4}
.stMarkdown h3{color:#00F5D4!important;margin-top:1.4rem;font-size:1.15rem}
.stTabs [data-baseweb="tab"]{border-radius:16px 16px 0 0;padding:.6rem 1rem}
.stTabs [aria-selected="true"]{color:#00F5D4!important;border-bottom:2px solid #00F5D4}
@media(max-width:768px){.kpi-v{font-size:1.6rem}.price{font-size:2rem}.cookie{left:8px;right:8px;max-width:none}}
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

# ---------- État global ----------
def init_state():
    defaults = {"plan": "Free Trial", "trial_start": datetime.now(), "scans_used": 0,
                "history": [], "results": None, "niche": None, "cookies": None,
                "events": [], "cookies_ts": None, "contact_ts": 0.0, "page": PAGES[0]}
    for k, v in defaults.items():
        st.session_state.setdefault(k, v)

def track(event, **meta):
    """Analytics interne (remplaçable par Plausible/GA après consentement cookies)."""
    try:
        if st.session_state.get("cookies") == "all":
            st.session_state.events.append({"t": datetime.now().isoformat(timespec="seconds"), "e": event, **meta})
    except Exception:
        pass

def trial_left():
    return max(0, 7 - (datetime.now() - st.session_state.trial_start).days)

def scans_left():
    if st.session_state.plan != "Free Trial":
        return None
    return 0 if trial_left() == 0 else max(0, 3 - st.session_state.scans_used)

# ---------- Couche "API" (séparée du front, remplaçable par un vrai backend) ----------
class TrendAPI:
    DATA = {
        "Tech": [("Ce gadget à 20€ remplace ton iPhone ?!", "#techtok #gadgets #ia", "Original sound – techvibes", 94),
                 ("3 apps IA que personne ne t'a montrées", "#ia #productivité #apps", "Espresso – remix lofi", 91),
                 ("J'ai testé l'IA pendant 24h, voici le résultat", "#challenge #ia #test", "Oh No – Kreepa", 88),
                 ("Arrête de scroller : ton PC est 3x trop lent", "#pc #astuces #setup", "Sneaky Snitch", 85),
                 ("Setup bureau à moins de 300€", "#setup #desk #minimal", "Aesthetic – Tollan Kim", 82)],
        "Fitness": [("Tu fais tes abdos complètement FAUX", "#fitness #abs #coach", "Gym Phonk – Montagem", 96),
                    ("30 jours de marche : avant / après", "#walking #transformation", "Levitating – lofi", 92),
                    ("Le petit-déj à 40g de protéines en 5 min", "#protein #mealprep", "Original sound – fitfam", 89),
                    ("Ne fais JAMAIS cet exercice au squat", "#squat #technique", "Industry Baby (sped up)", 86),
                    ("Routine 10 min avant le boulot", "#routine #morning", "Energy – Drake", 80)],
        "Cuisine": [("La recette à 3 ingrédients qui cartonne", "#recette #facile #foodtok", "Cooking vibes – chill", 95),
                    ("Je reproduis le plat viral à 1M de vues", "#viral #cuisine", "Espresso – Sabrina C.", 90),
                    ("Ton riz est raté à cause de ça", "#astuce #cuisine", "Original sound – chef", 87),
                    ("Dîner healthy en 10 minutes chrono", "#healthy #quick", "Good Days – SZA", 84),
                    ("Budget 5€ : je cuisine pour 4", "#budget #etudiant", "Sunroof (slowed)", 81)],
        "Business": [("Comment j'ai fait 10k€ avec 0€ de départ", "#business #entrepreneur", "Money Trees – lofi", 97),
                     ("Le side-hustle que personne ne copie", "#sidehustle #argent", "Original sound – biz", 93),
                     ("Erreurs qui tuent ton e-commerce", "#ecommerce #dropshipping", "Mind Games – Sickick", 89),
                     ("Ce que mon comptable ne t'a jamais dit", "#freelance #fiscalité", "Sneaky Snitch", 86),
                     ("Je lance un SaaS en 7 jours", "#saas #buildinpublic", "Runaway – Kanye (lofi)", 83)],
    }

    @classmethod
    def scan(cls, niche):
        rows = cls.DATA.get(niche)
        if not rows:
            raise ValueError(f"Niche inconnue : {niche}")
        rnd = random.Random(f"{niche}{datetime.now().date()}")
        return pd.DataFrame([{"Tendance / Hook": h, "Mots-clés": k, "Audio du moment": a,
                              "Score viral": s, "Vues 24h": f"{rnd.randint(120, 2400)}K"}
                             for h, k, a, s in rows])

    @staticmethod
    def script(niche, trend, audio, tone="Punchy"):
        return (f"🎬 SCRIPT VIDÉO – {niche} ({tone})\n{'=' * 40}\n"
                f"HOOK (0-2s) : \"{trend}\"\n"
                f"VISUEL : gros plan, texte à l'écran en gras, coupe rapide.\n\n"
                f"DÉVELOPPEMENT (2-15s) :\n- Problème : annonce ce que le spectateur fait mal.\n"
                f"- Preuve : montre un résultat concret en 3 plans courts.\n"
                f"- Twist : révèle l'astuce inattendue.\n\n"
                f"CTA (15-20s) : \"Abonne-toi pour la partie 2 !\" (un seul appel à l'action)\n"
                f"AUDIO : {audio}\nDURÉE CIBLE : 20 s | FORMAT : 9:16\n")

# ---------- Composants UI ----------
def kpi(label, value, delta):
    st.markdown(f'<div class="glass"><div class="kpi-l">{html.escape(label)}</div>'
                f'<div class="kpi-v">{html.escape(str(value))}</div><div class="kpi-d">{html.escape(delta)}</div></div>',
                unsafe_allow_html=True)

def copy_button(text, key):
    payload = json.dumps(text).replace("</", "<\\/")
    components.html(f"""<button id="b{key}" style="width:100%;padding:10px;border-radius:16px;border:1px solid #00F5D4;
    background:rgba(0,245,212,.1);color:#00F5D4;font-weight:600;cursor:pointer;font-family:Inter,sans-serif">
    📋 Copier dans le presse-papier</button><script>
    document.getElementById('b{key}').onclick=async()=>{{try{{await navigator.clipboard.writeText({payload});
    document.getElementById('b{key}').innerText='✅ Copié !';}}catch(e){{document.getElementById('b{key}').innerText='❌ Copie refusée';}}}};
    </script>""", height=56)

# ---------- Pages ----------
def page_dashboard():
    st.title("📊 Dashboard de Tracking")
    st.caption("Données simulées à des fins de démonstration.")
    c = st.columns(3)
    with c[0]: kpi("Tendances actives scannées", 1248 + st.session_state.scans_used * 5, "▲ +12% vs semaine dernière")
    with c[1]: kpi("Score de virilité moyen", "87,4 / 100", "▲ +3,1 pts")
    with c[2]: kpi("Rétention estimée", "14,2 s", "▲ 71% de complétion")
    rng = np.random.default_rng(42)
    days = pd.date_range(end=datetime.now().date(), periods=30)
    views = pd.DataFrame({"Vues": np.cumsum(rng.integers(8_000, 40_000, 30))}, index=days)
    bars = pd.DataFrame({"TikTok": rng.integers(40, 100, 7), "Reels": rng.integers(30, 90, 7),
                         "Shorts": rng.integers(20, 80, 7)}, index=["Lun", "Mar", "Mer", "Jeu", "Ven", "Sam", "Dim"])
    a, b = st.columns(2)
    with a:
        st.subheader("Croissance des vues (30 j)")
        st.area_chart(views, color="#00F5D4")
    with b:
        st.subheader("Performance par plateforme")
        st.bar_chart(bars, color=["#9D4EDD", "#00F5D4", "#FF007F"])
    st.subheader("Historique des scripts")
    if st.session_state.history:
        st.dataframe(pd.DataFrame(st.session_state.history), use_container_width=True, hide_index=True)
    else:
        st.info("Aucun script généré pour le moment. Lance un scan !")

def page_scanner():
    st.title("🎯 Scanner de Niche & IA")
    left = scans_left()
    badge = "Scans illimités" if left is None else f"{left} scan(s) restant(s)"
    st.markdown(f'<span class="badge">Plan {st.session_state.plan}</span> <span class="badge r">{badge}</span>',
                unsafe_allow_html=True)
    niche = st.selectbox("Choisis ta niche", list(TrendAPI.DATA.keys()))
    # Un seul CTA principal par page
    if st.button("🚀 Lancer l'Analyse", type="primary"):
        if left == 0:
            st.error("Essai terminé ou scans épuisés : passe à un plan payant dans l'onglet Tarifs.")
        else:
            try:
                bar = st.progress(0, text="Analyse des tendances…")
                for i in range(30):
                    time.sleep(0.1)
                    bar.progress((i + 1) / 30, text=f"Analyse des tendances… {int((i + 1) / 30 * 100)}%")
                st.session_state.results = TrendAPI.scan(niche)
                st.session_state.niche = niche
                st.session_state.scans_used += 1
                track("scan", niche=niche)
                bar.empty()
            except Exception as e:
                st.error(f"Erreur pendant l'analyse : {e}")
    df = st.session_state.results
    if df is not None:
        st.subheader(f"Top 5 tendances – {st.session_state.niche}")
        st.dataframe(df, use_container_width=True, hide_index=True)
        for i, row in df.iterrows():
            with st.expander(f"#{i + 1} · {row['Tendance / Hook']}  (score {row['Score viral']})"):
                st.write(f"**Mots-clés :** {row['Mots-clés']}  \n**Audio :** {row['Audio du moment']}")
                if st.button("✨ Générer le Script", key=f"gen{i}"):
                    try:
                        txt = TrendAPI.script(st.session_state.niche, row["Tendance / Hook"], row["Audio du moment"])
                        st.session_state.history.insert(0, {"Date": datetime.now().strftime("%d/%m %H:%M"),
                                                            "Niche": st.session_state.niche, "Hook": row["Tendance / Hook"],
                                                            "Script": txt})
                        track("script", hook=row["Tendance / Hook"])
                        st.code(txt, language=None)
                        st.download_button("⬇️ Télécharger (.txt)", txt, f"script_{i + 1}.txt", key=f"dl{i}")
                        copy_button(txt, i)
                    except Exception as e:
                        st.error(f"Génération impossible : {e}")

def page_pricing():
    st.title("💰 Tarifs & Abonnements")
    st.caption(f"Statut actuel : **{st.session_state.plan}**"
               + (f" · {trial_left()} jour(s) d'essai restant(s)" if st.session_state.plan == "Free Trial" else ""))
    cols = st.columns(3)
    for col, (name, p) in zip(cols, PLANS.items()):
        with col:
            feats = "".join(f"<li>{html.escape(f)}</li>" for f in p["feats"])
            cur = " <span class='badge'>Actuel</span>" if st.session_state.plan == name else ""
            st.markdown(f'<div class="glass" style="box-shadow:0 0 30px {p["color"]}55"><h3 style="color:{p["color"]}!important">'
                        f'{name}{cur}</h3><div class="price" style="color:{p["color"]}">{p["price"]}'
                        f'<span class="kpi-d"> {p["per"]}</span></div><ul class="f">{feats}</ul></div>', unsafe_allow_html=True)
            if st.button(f"Choisir {name}", key=f"plan_{name}", disabled=st.session_state.plan == name):
                st.session_state.plan = name
                track("plan", plan=name)
                st.success(f"Plan **{name}** activé (simulation, aucun paiement réel).")
                st.rerun()

LEGAL_DATE = "30 septembre 2026"
LEGAL = {
"Mentions légales": """
### Éditeur du site
**ViralPulse AI** – [Raison sociale], [forme juridique] au capital de [X] €
RCS [ville] n° [numéro] · SIRET [numéro] · TVA intracommunautaire [numéro]
Siège social : [adresse complète] · Email : [contact@votre-domaine.com] · Tél. : [numéro]
**Directeur de la publication :** [Nom Prénom]

### Hébergement
[Nom de l'hébergeur], [adresse], [pays] · [site web] · [téléphone]

### Propriété intellectuelle
La marque, le logo, l'interface, les textes, les bases de données et le code de ViralPulse AI sont protégés par le Code de la propriété intellectuelle. Toute reproduction ou extraction, même partielle, sans autorisation écrite est interdite.

### Responsabilité et liens externes
L'Éditeur s'efforce de fournir des informations exactes mais ne garantit ni leur exhaustivité ni leurs performances sur les plateformes tierces (TikTok, Instagram, YouTube). Les liens externes sont fournis à titre informatif.

### Médiation et litiges
Droit français applicable. Avant toute action, une solution amiable est recherchée. Médiateur : [nom et coordonnées du médiateur compétent].

### Accessibilité
Le site vise un niveau de contraste AA. Signalez tout défaut à [contact@votre-domaine.com].

> ⚠️ Remplace tous les champs entre crochets avant la mise en ligne. Ces textes sont un modèle : fais-les valider par un juriste.
""",
"Confidentialité (RGPD)": """
### 1. Responsable de traitement
L'Éditeur (voir Mentions légales). Contact protection des données : **[dpo@votre-domaine.com]**.

### 2. Données collectées, finalités et bases légales
| Données | Finalité | Base légale | Durée |
|---|---|---|---|
| Email, nom, mot de passe (haché) | Création et gestion du compte | Contrat | Durée du compte + 3 ans |
| Plan, factures, moyen de paiement (via prestataire) | Facturation, obligations comptables | Contrat / obligation légale | 10 ans |
| Niches scannées, scripts générés | Fournir le service, historique | Contrat | Durée du compte |
| Mesure d'audience (pages vues, événements) | Améliorer le produit | **Consentement** | 13 mois max |
| Messages de support | Répondre aux demandes | Intérêt légitime | 3 ans |
| Journaux techniques, IP | Sécurité, lutte anti-fraude et anti-spam | Intérêt légitime | 12 mois |

### 3. Destinataires et sous-traitants
Hébergeur, prestataire de paiement, outil d'emailing, outil d'analytics. Vos données ne sont jamais vendues. Tout transfert hors Union européenne est encadré par des clauses contractuelles types ou une décision d'adéquation.

### 4. Vos droits
Accès, rectification, effacement, limitation, opposition, portabilité, retrait du consentement à tout moment, directives post-mortem. Exercez-les depuis l'onglet **Mes droits & données** ou par email : réponse sous **1 mois**. Réclamation possible auprès de la **CNIL** (cnil.fr).

### 5. Sécurité
Chiffrement en transit (HTTPS/TLS), mots de passe hachés, accès restreints, sauvegardes, journalisation. En cas de violation, notification à la CNIL sous 72 h et aux personnes concernées si nécessaire.

### 6. Mineurs et décisions automatisées
Service réservé aux personnes majeures. Aucune décision produisant des effets juridiques n'est prise uniquement par traitement automatisé ; les scripts IA sont des suggestions.

*Dernière mise à jour : {date}*
""",
"Politique de cookies": """
### Qu'est-ce qu'un cookie ?
Un petit fichier ou traceur stocké sur votre appareil pour faire fonctionner le service ou mesurer son usage.

### Nos catégories
| Catégorie | Exemples | Consentement | Durée |
|---|---|---|---|
| **Essentiels** | Session, préférences de navigation, choix cookies | Non requis | Session / 6 mois |
| **Mesure d'audience** | Pages vues, événements (scans, scripts) | **Oui** | 13 mois max |
| **Publicité / réseaux sociaux** | Aucun utilisé | — | — |

### Gérer vos choix
Vous pouvez accepter, refuser ou personnaliser dans la bannière, puis modifier votre choix à tout moment via le bouton « Modifier mon choix cookies » ci-dessous. Refuser est aussi simple qu'accepter. Votre choix est conservé 6 mois. Vous pouvez aussi configurer votre navigateur pour bloquer les cookies.
""",
"CGU": """
**1. Objet.** Les présentes CGU régissent l'utilisation de ViralPulse AI, outil d'analyse de tendances et de génération de scripts vidéo.
**2. Accès au service.** Réservé aux professionnels majeurs. L'utilisateur garantit l'exactitude de ses informations et protège ses identifiants.
**3. Usages interdits.** Scraping abusif, revente ou sous-licence non autorisée, contournement des quotas, contenus illicites, atteinte à la sécurité ou aux droits de tiers.
**4. Contenus générés.** Les scripts sont des suggestions. L'utilisateur reste seul responsable de leur publication et du respect des règles des plateformes et des droits d'auteur. Aucun résultat de performance n'est garanti.
**5. Disponibilité.** Accès 24/7 sans garantie d'absence d'interruption (maintenance, force majeure).
**6. Responsabilité.** Service fourni « en l'état ». La responsabilité de l'Éditeur est limitée aux dommages directs, plafonnée aux sommes versées sur les 12 derniers mois.
**7. Suspension.** Tout manquement peut entraîner suspension ou résiliation après mise en demeure.
**8. Évolution.** Les CGU peuvent évoluer ; les utilisateurs sont informés par email 30 jours avant l'entrée en vigueur.
**9. Droit applicable.** Droit français ; tribunaux du siège de l'Éditeur, sous réserve des règles impératives.

*Version du {date}*
""",
"Abonnement & remboursement (CGV)": """
### Offres et prix
| Plan | Prix | Contenu |
|---|---|---|
| Free Trial | 0 € | 7 jours, 3 scans, accès limité, sans carte bancaire |
| Creator Pro | 29 € /mois | Scans illimités, IA avancée, support 24/7 |
| Agency Elite | 79 € /mois | Multi-comptes, exports CSV de masse, insights exclusifs |

Prix affichés [HT/TTC – à préciser]. TVA applicable selon la réglementation.

### Paiement et renouvellement
Paiement mensuel à l'avance via un prestataire sécurisé. Reconduction tacite chaque mois ; rappel par email avant chaque renouvellement si requis.

### Résiliation
À tout moment depuis le compte, sans frais ; l'accès reste actif jusqu'à la fin de la période payée.

### Droit de rétractation et remboursement
Service destiné aux professionnels : le droit légal de rétractation des consommateurs ne s'applique pas de plein droit. Par geste commercial, **tout premier paiement est remboursable sur demande sous 14 jours** si aucun export massif n'a été utilisé. Aucun remboursement au prorata des périodes entamées ensuite. Remboursement sous 14 jours sur le moyen de paiement d'origine.

### Médiation
En cas de litige non résolu, recours au médiateur : [nom et coordonnées].

*Version du {date}*
""",
}
LEGAL = {k: v.replace("{date}", LEGAL_DATE) for k, v in LEGAL.items()}

def sitemap_robots():
    base = "https://viralpulse.example.com"
    sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(
        f"  <url><loc>{base}/?page={p}</loc></url>\n" for p in ["dashboard", "scanner", "tarifs", "legal"]) + "</urlset>"
    return sm, f"User-agent: *\nAllow: /\nSitemap: {base}/sitemap.xml\n"

def contact_form():
    with st.form("contact"):
        email = st.text_input("Votre email")
        msg = st.text_area("Message (10 à 1000 caractères)")
        trap = st.text_input("Laisser vide", key="hp", label_visibility="collapsed")  # honeypot anti-spam
        if st.form_submit_button("Envoyer"):
            try:
                if trap:
                    return  # bot détecté : on ignore silencieusement
                if time.time() - st.session_state.contact_ts < 30:
                    st.warning("Merci de patienter 30 s entre deux envois."); return
                if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[A-Za-z]{2,}", email.strip()):
                    st.error("Email invalide."); return
                if not 10 <= len(msg.strip()) <= 1000:
                    st.error("Le message doit faire entre 10 et 1000 caractères."); return
                st.session_state.contact_ts = time.time()
                track("contact")
                st.success("Message envoyé (simulation). Nous répondons sous 48 h.")
            except Exception as e:
                st.error(f"Erreur : {e}")

def cookie_banner():
    if st.session_state.cookies is not None:
        return
    st.markdown('<div class="glass"><b>🍪 Vos choix de confidentialité</b><br><span class="kpi-d">'
                'Nous utilisons des cookies essentiels et, avec votre accord, des cookies de mesure d\'audience. '
                'Aucune publicité. Vous pouvez changer d\'avis à tout moment. '
                '<a href="?page=legal" target="_self">Politique cookies</a></span></div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    if c1.button("Tout accepter", key="ck_all", type="primary"):
        st.session_state.cookies = "all"; st.session_state.cookies_ts = datetime.now().isoformat(); st.rerun()
    if c2.button("Tout refuser", key="ck_no"):
        st.session_state.cookies = "none"; st.session_state.cookies_ts = datetime.now().isoformat(); st.rerun()
    with st.expander("Personnaliser"):
        st.checkbox("Essentiels (obligatoires)", value=True, disabled=True)
        an = st.checkbox("Mesure d'audience (analytics)", value=False, key="ck_an")
        if st.button("Enregistrer mes choix", key="ck_save"):
            st.session_state.cookies = "all" if an else "essential"
            st.session_state.cookies_ts = datetime.now().isoformat(); st.rerun()

def footer():
    st.markdown(f'<div class="glass" style="text-align:center"><span class="kpi-d">© {datetime.now().year} ViralPulse AI · '
                '<a href="?page=legal" target="_self">Mentions légales</a> · <a href="?page=legal" target="_self">Confidentialité</a> · '
                '<a href="?page=legal" target="_self">Cookies</a> · <a href="?page=legal" target="_self">CGU / CGV</a></span></div>',
                unsafe_allow_html=True)

def rights_tab():
    st.markdown("### Exercer vos droits RGPD")
    st.markdown("Téléchargez vos données (portabilité/accès) ou supprimez-les (effacement) directement ici.")
    export = {"plan": st.session_state.plan, "scans_utilises": st.session_state.scans_used,
              "essai_debut": st.session_state.trial_start.isoformat(), "scripts": st.session_state.history,
              "cookies": st.session_state.cookies, "consentement_date": st.session_state.get("cookies_ts")}
    st.download_button("⬇️ Exporter mes données (JSON)", json.dumps(export, ensure_ascii=False, indent=2, default=str),
                       "mes_donnees_viralpulse.json", mime="application/json")
    st.markdown("**Consentement cookies :** " + {"all": "Tout accepté", "essential": "Essentiels seulement",
                "none": "Tout refusé", None: "Non défini"}[st.session_state.cookies])
    if st.button("🍪 Modifier mon choix cookies"):
        st.session_state.cookies = None; st.rerun()
    st.warning("La suppression efface l'historique, le plan et les préférences de cette session.")
    if st.checkbox("Je confirme vouloir supprimer toutes mes données"):
        if st.button("🗑️ Supprimer mes données"):
            for k in list(st.session_state.keys()):
                del st.session_state[k]
            st.rerun()

def page_legal():
    st.title("⚖️ Légal, Confidentialité & CGU")
    st.caption(f"Documents à jour au {LEGAL_DATE}. Conformes RGPD, loi Informatique et Libertés et ePrivacy (à faire valider).")
    names = list(LEGAL.keys()) + ["Mes droits & données", "Contact", "Technique & SEO"]
    tabs = st.tabs(names)
    for t, (_, body) in zip(tabs, LEGAL.items()):
        with t:
            st.markdown(body)
    n = len(LEGAL)
    with tabs[n]: rights_tab()
    with tabs[n + 1]: contact_form()
    with tabs[n + 2]:
        sm, rb = sitemap_robots()
        st.download_button("⬇️ sitemap.xml", sm, "sitemap.xml")
        st.download_button("⬇️ robots.txt", rb, "robots.txt")
        st.caption(f"Événements analytics enregistrés (session, avec consentement) : {len(st.session_state.events)}")

def page_404():
    st.markdown('<div class="e404">404</div>', unsafe_allow_html=True)
    st.markdown("<h3 style='text-align:center'>Cette page a disparu dans le néon.</h3>", unsafe_allow_html=True)
    if st.button("Retour au Dashboard", key="back"):
        st.query_params.clear(); st.session_state.page = PAGES[0]; st.rerun()

# ---------- Main ----------
ROUTES = {"dashboard": PAGES[0], "scanner": PAGES[1], "tarifs": PAGES[2], "legal": PAGES[3]}

def main():
    init_state()
    qp = st.query_params.get("page")
    if qp and qp not in ROUTES:
        page_404(); return
    if qp in ROUTES:
        st.session_state.page = ROUTES[qp]
    with st.sidebar:
        st.markdown('<div class="logo">⚡ VIRAL PULSE AI</div>', unsafe_allow_html=True)
        st.caption("Trends & scripts viraux")
        st.session_state.page = st.radio("Navigation", PAGES, index=PAGES.index(st.session_state.page),
                                         label_visibility="collapsed")
        st.markdown(f'<div class="glass"><span class="kpi-l">Compte</span><br><b>{st.session_state.plan}</b></div>',
                    unsafe_allow_html=True)
    try:
        {PAGES[0]: page_dashboard, PAGES[1]: page_scanner, PAGES[2]: page_pricing, PAGES[3]: page_legal}[st.session_state.page]()
    except Exception as e:
        st.error(f"Une erreur est survenue : {e}")
    footer()
    cookie_banner()

main()

