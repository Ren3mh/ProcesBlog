---
title: "Problemer med EF Core migrations i CI/CD"
date: "2025-10-15"
---

**15-10 2025:**

Jeg rendte ind i et problem, hvor EF Core migrations i min CI/CD-pipeline ikke blev anvendt korrekt på produktionsserveren. GitHub Actions genererede migrations-scripts, uploadede dem og kørte dem via psql. Alligevel manglede der tabeller.

Fejlen var en kombination af timing og miljølogik. Ved kun at køre SQL-scripts bliver EF’s egen migrationslogik og seeding logik bypasset.

Løsningen blev at kombinere migrations-scripts med et Database.Migrate() kald ved API-start. På den måde er databasen altid korrekt – uanset om migrationerne kommer fra CI/CD eller API’en selv.
