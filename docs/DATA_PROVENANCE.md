# Data provenance and verification policy

## Imported catalogue records

- Source: National Institutional Ranking Framework (NIRF), India Rankings 2025, Engineering category.
- Official source URL: https://www.nirfindia.org/Rankings/2025/EngineeringRanking.html
- Scope in initial seed: a curated set of named institutions and their Engineering rank values.
- Record status: `VERIFIED_INSTITUTION_RANKING`; rank status: `VERIFIED`.
- The source proves the listed institution's position in the stated NIRF category/year. It does not prove current programme availability, a specific campus's specialization, fees, NAAC grade, placement outcomes, or admission eligibility.
- The seed does not create programme, resource, or PYQ rows. Those must be imported separately from official university sources after checking their current academic year and campus.

## Official sources to verify before adding data

- NIRF: https://www.nirfindia.org/
- UGC: https://www.ugc.gov.in/
- AKTU: https://aktu.ac.in/
- HBTU: https://hbtu.ac.in/
- SRMCEM: https://www.srmcem.ac.in/
- BBD University: https://bbdu.ac.in/

## Required provenance fields

For each imported ranking, accreditation, programme, fee, placement, syllabus, or PYQ record, retain the source URL, source/record status, reporting or academic year, retrieval timestamp, and last verification timestamp. Do not infer unavailable values. A generated practice question must never be stored as an official PYQ.
