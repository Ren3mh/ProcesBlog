---
title: "udvikle en full-stack applikation"
date: "2025-09-23"
---

### Kontekst

Projektet gik ud på at udvikle en full-stack applikation med et Blazor WebAssembly frontend og et .NET 9 Web API backend, der skulle deployes på en Hetzner VPS med PostgreSQL-database, Nginx som reverse proxy og automatisk CI/CD via GitHub Actions. Målet var at skabe en skalerbar, produktionsklar løsning med automatiseret deployment, sikkerhed (HTTPS) og databasehåndtering.

### Mål
Projektet dækker flere centrale kompetencer inden for moderne softwareudvikling:

Full-stack udvikling (frontend + backend).
DevOps og infrastruktur (VPS, Nginx, systemd, CI/CD).
Databaseintegration (Entity Framework Core + PostgreSQL).
Sikkerhed (HTTPS, CORS, autentificering).
Automatisering (GitHub Actions, migrations, deployment).
Det viser evnen til at designe, implementere og deploye en komplet løsning – fra kode til produktionsmiljø.

At mestre deployment af .NET-applikationer på en Linux-server (Hetzner VPS).
At integrere Blazor WebAssembly med et .NET API med korrekt CORS og autentificering.
At opsætte en robust CI/CD-pipeline med GitHub Actions til automatisk deployment.
At konfigurere Nginx som reverse proxy for både frontend og backend.
At håndtere database-migrationer automatisk via Entity Framework Core.

Hvad ville jeg gerne opnå?
Et fuldt funktionelt system, hvor:

Kodepush til main-branchen automatisk deployer til VPS’en.
Frontend og backend kommunikerer sikkert via HTTPS.
Databasen opdateres automatisk ved deployment.
Systemet er selvreparerende (f.eks. genstarter API ved crash via systemd).

### Handling / Erfaring (Doing)
Hvad gjorde jeg konkret?


1 Projektopsætning:

Oprettede Blazor WebAssembly- og .NET API-projekter i samme solution.
Konfigurerede Entity Framework Core med PostgreSQL og migrations:

// Automatiske migrationer ved startup (hvis flag sat)
if (applyMigrations) { db.Database.Migrate(); }


Opsatte CORS til lokal udvikling og produktion:
policy.WithOrigins("https://localhost:7220", "http://46.62.197.82")
      .AllowCredentials();


2 Serveropsætning (Hetzner VPS):

Installerede PostgreSQL, .NET 9, Nginx og Certbot.
Oprettede database (ExpertDb) og bruger (expertadmin).
Konfigurerede systemd-service til API’en:

[Service]
ExecStart=/usr/share/dotnet/dotnet /var/www/api/365EkspertAPI.dll
Restart=always  # Genstarter ved crash

Opsatte Nginx som reverse proxy:

/ → Blazor frontend.
/api → .NET API.
/scalar → API-dokumentation.
HTTP → HTTPS-redirect.


3 CI/CD med GitHub Actions:

Workflow, der:

Bygger og publiserer Blazor og API.
Kører database-migrationer på serveren.
Deployer via SCP + SSH:
- scp -r ./publish/api/* rene@46.62.197.82:/var/www/api
- ssh rene@46.62.197.82 "sudo systemctl restart 365EkspertAPI.service"

Trigger: Kør ved push til main.


4 Testing og debugging:

Verificerede CORS, HTTPS og API-endpoints.
Løste problemer med self-signed certifikater (midlertidigt).
Testede automatisk genstart af API’en via systemd.

### Refleksion (Reflecting)
Hvad gik godt?
✅ Automatiseringen virker: GitHub Actions deployer korrekt til VPS’en ved hver push.
✅ Nginx-konfigurationen håndterer routing mellem frontend/backend uden problemer.
✅ Database-migrationer kører automatisk via dotnet ef database update.
✅ systemd-service sikrer, at API’en altid kører (genstarter ved crash).
Hvad var udfordrende?
⚠ HTTPS/Certbot:

Midlertidigt self-signed certifikat var nødvendigt, indtil domænet (365.elbooking.dk) var korrekt peget.
Let’s Encrypt krævede korrekt DNS-opsætning før det virkede.
⚠ CORS i udviklingsmiljøet:
Skulle tillade både localhost og produktions-IP, hvilket krævede dynamisk konfiguration.
⚠ SCP/SSH i GitHub Actions:
Krævede nøje opsætning af secrets (SSH-nøgle, database-forbindelsesstreng).
Entity Framework Core-migrationer:
Første forsøg på automatiske migrationer fejlede pga. manglende adgangsrettigheder til PostgreSQL-brugeren.

Hvad lærte jeg?
🔹 Infrastruktur som kode: At skrive idempotente scripts (f.eks. Nginx-konfig, systemd) er afgørende for reproduktionsbarhed.
🔹 Sikkerhed i CI/CD: Aldrig at hårdkode hemmeligheder – altid brug GitHub Secrets.
🔹 Debugging på Linux: At bruge journalctl -u 365EkspertAPI.service til at fejlsøge systemd-services.
🔹 Reverse proxy-logik: Hvordan Nginx kan routere flere services (/, /api, /scalar) på samme domæne.
🔹 Blazor’s miljøvariabler: At skifte mellem localhost og produktions-URL’er kræver omhyggelig konfiguration.

### Kobling til teori (Thinking)
Hvordan hænger erfaringen sammen med teori?

DevOps og CI/CD:

Praktisk anvendelse af Continuous Integration/Deployment (fra undervisning om agile metoder).
GitHub Actions svarer til build pipelines (f.eks. Azure DevOps, Jenkins).


Microservices-arkitektur:

Adskillelse af frontend (Blazor) og backend (API) følger principper om loose coupling.


Reverse Proxy (Nginx):

Teorien om load balancing og routing blev konkretiseret via Nginx-konfiguration.


Database-migrationer:

EF Core’s Migrate() implementerer schema evolution (som beskrevet i databaseteori).


Sikkerhed:

HTTPS, CORS og AllowCredentials relaterer til OWASP Top 10 (f.eks. "Broken Access Control").

### Næste skridt (Planning)
Hvad vil jeg gøre anderledes næste gang?
🔸 Brug Docker til at containerisere API’en og databasen for nemmere deployment.
🔸 Implementer rigtige certifikater fra start (Let’s Encrypt med certbot --nginx).
🔸 Opsæt en staging-server før production for at teste deployment-workflow.
🔸 Brug feature flags til at aktivere/deaktivere migrationer i stedet for --migrate-argument.
Hvilke forbedringer planlægger jeg?
🛠 Automatisk backup af PostgreSQL-databasen via cron-jobs.
🛠 Monitorering (f.eks. Prometheus + Grafana) for at overvåge API’en.
🛠 Bedre fejlhåndtering i Blazor (f.eks. global exception handler).
🛠 Implementer API-versionering for at undgå breaking changes.

### Feedback
- Hvilken feedback fik jeg (fra vejleder/guild/gruppe)?
- Hvordan kan jeg bruge den?
