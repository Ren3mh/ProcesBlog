---
title: "Håndtering af filupload i både API og klient"
date: "2025-10-20"
---

**20-10 2025:**

Jeg skulle gemme uploadede billeder både i API’ens wwwroot og i Blazor-klientens wwwroot. Lokalt virkede det fint, men i Docker og CI/CD fandtes de relative paths ikke – eller var ikke delt mellem containere.

Det løste jeg ved at bruge Directory.CreateDirectory() og en delt memory stream, så filen kun læses én gang og derefter skrives to steder.

Til gengæld blev det tydeligt, at klienten også skal dockeriseres, hvis den skal håndtere filer konsistent i produktion. Læringen: filstier er aldrig “bare filer”, når containere er involveret.
