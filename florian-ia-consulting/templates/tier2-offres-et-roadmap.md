# TIER 2 — LES 4 BRIQUES & ROADMAP DE PRODUCTION
> Florian Dierckx — AI Revenue Partner
> Produit le 12/07/2026 · Complète consulting-ia-sales-system-v1.md

---

## 1. LES 4 OFFRES TIER 2 (2 500-6 000€)

Principe commun : chaque brique est un workflow n8n déployé et fonctionnel, pas une recommandation écrite. Le diagnostic (Tier 1) identifie laquelle est pertinente ; le Tier 2 la construit.

### Brique 1 — Qualification et routing automatique de leads

**Pain qu'elle résout :** le prospect passe 5-10 min par lead à évaluer manuellement qui mérite un rappel. Sur 20-30 leads/semaine, ça vaut une demi-journée.

**Ce qui est livré :**
- Webhook connecté au formulaire du site (ou LinkedIn/newsletter)
- Enrichissement automatique (profil, entreprise, secteur)
- Scoring 0-100 calibré sur l'ICP réel du client
- Routing automatique : chaud → CRM + alerte Slack immédiate, tiède → séquence email nurturing, froid → archivage silencieux
- Log complet dans Google Sheets pour audit mensuel

**Scope horaire réaliste :** 8-12h (calibration ICP + connexion outils existants + tests)
**Prix dans la fourchette :** 2 500-3 500€ (bas de fourchette, brique la plus templatisable)
**Pré-requis client :** un CRM ou minimum Notion/Airtable, un formulaire web

### Brique 2 — Relances et suivi de facturation automatisés

**Pain qu'elle résout :** "je dois penser à relancer Untel" — la charge mentale de facturation/relance qui traîne, et le cash qui rentre en retard.

**Ce qui est livré :**
- Détection automatique des factures en attente (connecté à l'outil de facturation existant ou Google Sheets)
- Séquence de relance programmée (J+7, J+14, J+21 avec ton qui monte progressivement)
- Alerte avant échéance pour anticiper plutôt que subir
- Dashboard simple de trésorerie prévisionnelle

**Scope horaire réaliste :** 10-15h (dépend de l'outil de facturation déjà en place)
**Prix dans la fourchette :** 3 000-4 500€
**Pré-requis client :** un outil de facturation ou a minima un fichier structuré des factures émises

### Brique 3 — Triage email intelligent avec drafts automatiques

**Pain qu'elle résout :** 30-40 min par jour à trier la boîte mail, décider quoi traiter en premier, rédiger les réponses répétitives.

**Ce qui est livré :**
- Classification automatique quotidienne : urgent / à traiter / archiver
- Génération de brouillon de réponse pour les urgents (validation humaine avant envoi, jamais d'auto-envoi)
- Brief récapitulatif envoyé chaque matin (Slack, email ou WhatsApp selon préférence)

**Scope horaire réaliste :** 8-10h
**Prix dans la fourchette :** 2 500-3 000€ (brique la plus rapide à déployer, bon produit d'appel Tier 2)
**Pré-requis client :** Gmail ou Outlook, volume email suffisant pour justifier l'automatisation (min. 15-20 emails/jour)

### Brique 4 — Génération de contenu automatisée dans la voix du client

**Pain qu'elle résout :** le créatif solo sait qu'il doit publier régulièrement (captions, emails, descriptions produit) mais chaque post lui coûte 30-45 min de rédaction, et le résultat sonne générique s'il utilise ChatGPT tel quel.

**Ce qui est livré :**
- Pipeline qui prend un brief court (3-4 lignes) ou un calendrier de contenu
- Génère des drafts (captions, emails, descriptions) calibrés sur la voix réelle du client — c'est le prompt pack Angry Dollz, mais automatisé au lieu d'être un PDF statique
- File d'attente de validation avant publication (jamais de post automatique sans review humaine)

**Scope horaire réaliste :** 12-18h (la calibration de voix demande plus d'itération que les 3 autres briques)
**Prix dans la fourchette :** 4 000-6 000€ (haut de fourchette, différenciateur le plus fort vu ton positionnement créatif)
**Pré-requis client :** un minimum de contenu existant à analyser pour calibrer la voix (10-15 posts/emails passés)

---

## 2. MATRICE DIAGNOSTIC → BRIQUE

À utiliser en live pendant le discovery call, phase 4 (transition vers l'offre). Objectif : ne jamais improviser la réponse à "et concrètement ça donnerait quoi ?".

| Signal en discovery (verbatim probable du prospect) | Brique à proposer | Prix indicatif |
|---|---|---|
| "Je passe des heures à trier mes prospects avant de les rappeler" | Brique 1 — Qualification leads | 2 500-3 500€ |
| "Je relance mes factures à la main, ou je les relance pas" | Brique 2 — Facturation/relances | 3 000-4 500€ |
| "Ma boîte mail c'est le chaos, je rate des trucs importants" | Brique 3 — Triage email | 2 500-3 000€ |
| "Je sais que je devrais poster plus mais j'ai jamais le temps de rédiger" | Brique 4 — Contenu automatisé | 4 000-6 000€ |
| Plusieurs pains cités à la fois | 2 briques combinées, prix cumulé avec remise de bundle 10-15% | Variable |

**Règle de vente :** ne jamais proposer les 4 briques d'un coup à un client Tier 1. Une seule, celle qui correspond au pain le plus chiffré en phase 3 du discovery. Le reste devient la conversation du Tier 3 (retainer) ou d'un second projet.

---

## 3. WORKFLOWS N8N — CE QUI EST RÉELLEMENT LIVRÉ ICI

Important à comprendre : je ne peux pas déployer directement sur ton instance n8n locale (pas de tunnel public, pas d'accès réseau depuis mon environnement). Ce que j'ai construit, ce sont **les fichiers JSON complets, prêts à importer**, correspondant aux Briques 1 et 3 (les deux les plus rapides à templatiser et à vendre en premier).

### Fichiers produits :
- `workflow-1-lead-qualification.json` — Brique 1 complète : webhook → enrichissement → scoring → routing CRM/Slack/Sheets
- `workflow-2-email-triage.json` — Brique 3 complète : cron matinal → fetch Gmail → classification Claude → drafts → brief récapitulatif

### Pour les importer dans ton n8n local :
1. Ouvre ton interface n8n
2. Menu → Import from File
3. Sélectionne le fichier `.json`
4. Configure les credentials manquants (Notion API, Slack API, Gmail OAuth, clé API Anthropic selon le workflow) — ce sont les seules étapes qui nécessitent tes propres clés, je ne peux pas les pré-remplir
5. Teste avec un lead ou un email fictif avant de connecter en production chez un client

### Ce qu'il reste à faire avant de vendre ces briques :
- Calibrer les seuils de scoring (Brique 1) sur un vrai ICP client, pas les valeurs par défaut
- Connecter réellement à un CRM test (Notion suffit pour commencer)
- Chronométrer le temps de setup réel par brique pour valider ou ajuster les fourchettes horaires ci-dessus

---

## 4. LES 5 LIVRABLES À CONSTRUIRE EN PRIORITÉ (ensemble, prochaines sessions)

Classés par ordre d'impact sur ta capacité à vendre le Tier 2 concrètement — pas par facilité.

**1. Les 2 workflows n8n testés et calibrés en conditions réelles**
Prendre les JSON déjà produits, les importer, les faire tourner sur TES propres données (ta boîte mail, un CRM Notion test) pendant une semaine. Sans ce test, tu vends une promesse, pas une preuve.

**2. Une démo vidéo courte (2-3 min) par brique**
Capture d'écran du workflow qui tourne réellement — lead qui rentre, score qui s'affiche, alerte Slack qui part. C'est l'équivalent du cas BEVAC mais pour le Tier 2 : la preuve visuelle qui remplace le discours.

**3. Le template de contrat/proposition Tier 2**
Un document type (pas un PDF de 30 pages — 2-3 pages) : scope de la brique choisie, livrables précis, délai, prix, contreparties si tarif de lancement. Évite de rédiger une proposition from scratch à chaque deal.

**4. La brique 4 (contenu automatisé) prototypée sur ton propre cas FLOWA ou un cas BEVAC-like**
C'est la brique la plus différenciante (ton angle créatif + technique), mais aussi la moins testée des quatre. La prototyper sur un cas que tu contrôles avant de la vendre à un inconnu.

**5. Un mini-audit de rentabilité horaire post-mission**
Après chaque Tier 1 livré, un calcul simple : heures réellement passées vs prix facturé. C'est la donnée qui te dira si tu es à 30€/h ou 80€/h, et qui alimente directement le risque #2 du plan 90 jours (sur-livraison chronique).

---

*Fichiers à pusher : `tier2-offres-et-roadmap.md` + les deux `.json` dans `florian-ia-consulting/templates/n8n-workflows/`*
