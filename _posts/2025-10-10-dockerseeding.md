---
title: "Udfordringen med automatisk database-seeding i Docke"
date: "2025-10-10"
---

**10-10 2025:**

En af de første udfordringer jeg stødte på, var at få min PostgreSQL-database til automatisk at blive seeded inde i Docker. Lokalt fungerede alt perfekt, når jeg kørte mit ResetDb-script. Men når API’en blev containeriseret, blev databasen oprettet, migrationerne kørt – men ingen seed-data dukkede op.

Det viste sig, at min seeding-logik indirekte var bundet til Development-miljøet, og i Production blev der slet ikke seedet. API’en startede bare op uden at røre databasen.

Løsningen blev at gøre seedingen idempotent og køre den ved startup – uanset miljø. API’en tjekker nu, om databasen er tom, og seeder kun hvis det er nødvendigt.

Læringen var klar: Automatisering skal fungere ens i alle miljøer, og kunne køres flere gange uden risiko.
