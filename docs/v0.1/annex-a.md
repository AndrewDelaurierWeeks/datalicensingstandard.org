## Annex A · The vendor declaration, machine-readable

The declaration is a JSON document validated against `tdls-ai-vendor-declaration.schema.json` (JSON Schema 2020-12), schema version 0.3.0. It carries the answers to Part 4 in fixed fields where a field exists, so that a procurement system can request it, a vendor can attach it to an offer, and a reviewer can validate it with one command. An answer with no field is given in the questionnaire response. The schema is free, permissively licensed and versioned by its `$id`; a published version is not changed, and a breaking change is a new version with a new `$id`, so a declaration that validated once validates against that version again; depending on it is a choice. Schema 0.3.0 is such a new version, published with this edition; a declaration written for schema 0.2.0 still validates against schema 0.2.0, which is archived, unchanged, at the address in Part 7.

The field names are the vocabulary of Part 3: `attacker_assumed`, `measured_on`, `residual`, `tier`, `health_data`, `financial_data`. The `financial_data` block carries R11: the classes present, and per class the sensitive-authentication-data statement, the 3.5.1 approach, the compliance evidence hash, the 6802 basis and agreement hash, or the 1681b circumstance and certification hash; `classes` empty requires `search_performed`. The attacker is stated on a fixed scale, this document's convention, so that two vendors' claims can be compared: `T0-public-only` (an attacker with public information only), `T1-public-plus-one-release` (public information plus one prior release from the same source), `T2-insider-without-keys` (access to the vendor's systems but not to any secret material used in de-identification), `T3-insider-with-other-releases` (an insider holding other releases), `T4-model-access-black-box` (query access to a model trained on the data), `T5-model-access-grey-box` (access to the model's weights or internals), or `none-stated`.

**New in schema 0.3.0.** `synthetic_data` (R1, R2, R3, R8) carries the share that is synthetic and its unit, each generator (kind, name, version, provider, terms reference), the seed data reference, and the answers on reproduction of seed records and on benchmark items. `human_data` (R2, R10) carries the agreement template reference, the counts of contributors and of signed agreements, and the intermediaries. `sensor_records` (R1 to R3) carries the block below. `rl_environment` (R1, R2, R3, R5, R8, R12) carries the provenance of the parts, the license of the code, whether personal data is inside, the build digest, the task count and the optional hash of the task list, the grader version, the form of delivery, the distribution and exclusivity answers and, where the environment is run for the buyer or the buyer's traces leave the buyer's systems, their handling. `delivery_form` takes one of two values; an environment that reaches the buyer in both forms is marked `hosted`, and the questionnaire response says which part is delivered. Each of these blocks is stated once in a declaration. A purchase with more than one RL environment, embodiment, hardware configuration or recording format is more than one delivery, and each delivery carries its own declaration. Where synthetic components differ in generator, method or seed data, `generation_method` and `seed_data_reference` name each component by its `component_id`. Four optional fields are added to the blocks schema 0.2.0 had: `expires_at` on the declaration (the date a new declaration is due under R7), `receipt_id` and `log_bound_to_manifest` in `deletion_propagation` (R9), the second recording the last answer to question 11, and `certificate_id` in `attestation` (R4). Each identifier is a free string, so the identifier of any issuer fits; `certificate_id` is the attester's own reference for its attestation and implies no certification by an accreditation or licensing body. The time-stamp token hash in `delivery` is required where `evidence_package` lists a token and refused where it lists none.

**The sensor-record block.** Required (R) for every delivery with sensor records; conditional (C) where the stream or practice exists. A conditional field marked `not-present` means the stream does not exist in the delivery. Where the stream exists and the practice was not carried out (a camera never calibrated, people recorded and nothing removed, a home entered with no permission recorded), the field is marked `not-done`. A measured field the vendor did not measure is marked `not-measured` (the maximum offset, the gap count, the count of episodes discarded, and dropped frames, a text field); label agreement is left out where it was not measured. The units are fixed so that declarations compare: rates in hertz, offsets in milliseconds, total duration in hours, gap lengths in seconds, image size as a pixel count, agreement in percent, dates in ISO 8601 (written YYYY-MM-DD). The action representation states its own units; where they are other than meters, radians and newtons, it names them. The last column names the buyer's team that uses the field.

| Field | R or C | Unit or form | Used by |
|---|---|---|---|
| Embodiment: robot make and model, end effector, degrees of freedom; or the capture device for human capture | R | text; integer | robot learning |
| Each sensor: type, make and model, mounting, resolution, sampling rate | R | text; pixels for cameras; Hz | perception, world models |
| Camera calibration: intrinsics and extrinsics, date calibrated, file reference | C (cameras) | matrices; ISO 8601 | perception, world models |
| Time synchronization: method and clock source; maximum offset between streams, measured | R | text; ms or `not-measured` | perception, robot learning |
| Action representation: joint or end-effector space, frame of reference, absolute, delta or velocity, units | C (actions recorded) | text | robot learning |
| Control rate | C (actions recorded) | Hz | robot learning |
| Collection method: teleoperation and its device, scripted motion, an autonomous policy (which), or human demonstration | R | text | robot learning, evaluation |
| Episodes, total hours, tasks with their language instructions | R | integer; hours; text | robot learning |
| Success labels: method, who assigned them, and agreement between labelers where two labeled | C (labels present) | text; percent | robot learning, evaluation |
| Environments by kind (home, workplace, warehouse, laboratory, outdoor) and count | R | text; integer | robot learning, evaluation |
| Data quality: dropped frames per stream, gaps longer than a stated length, episodes failed, filtered or discarded and the rule used | R | count; rate; seconds | all |
| Format and its version | R | text | engineering |
| Hash manifest over every episode file | R | SHA-256 | counsel, engineering |
| Consent basis: operators, camera wearers, others recorded; withdrawal procedure | R | text | counsel |
| Private spaces: occupant or owner permission | C (homes, workplaces) | text | counsel |
| De-identification: what was removed (faces, number plates, screens and documents in view, voices, location traces), method, sample of frames, residual | C (people, places or location recorded) | text; count; percent | counsel, privacy |
| Physiological signals and their classification as health information | C (wearables) | text | counsel |

Validate with: `python3 validate.py tdls-ai-vendor-declaration.schema.json example-declaration.json`. A declaration that validates has the right fields; validation scores nothing.

**Crosswalk from outside specifications.** A buyer or vendor that already keeps a record in one of the forms below can see where each of its fields lands in this annex. The mapping runs one way, from the outside field into Annex A: completing the outside form does not complete a declaration. Each outside field is classed as carried (its value can be written into the Annex A field as it stands), stricter (the Annex A field asks for more on the part it covers) or not carried (Annex A has no field for it). A class may cover part of an outside field. The classes are the author's reading on the date opened. No publisher named below reviewed or endorsed this mapping, and the classes compare fields only: a declaration completes no outside form, and nothing in the mapping says that a declaration meets the specification, the template or the statute the outside form belongs to. Only field names, section headings and paragraph numbers are given, and this document claims no right in them; no other text of a specification is reproduced in this annex.

The specifications, each as opened on 2026-11-24:

1. OASIS Open, Data Provenance Metadata Version 1.0, Committee Specification Draft 01, 07 May 2026, opened in the committee's repository at the tag that carries that date: 24 elements in Source, Provenance and Use. The element names below are those of the property tables in its section 5; its JSON encoding in section 7 names some of them differently, and the converter reads the JSON names. A release candidate for a second draft, tagged in that repository on 4 November 2026 under the date 11 November 2026, was present when the repository was opened; it is not mapped. The mapping and the validator's conversion follow the first draft and no later one.
2. MLCommons Association, Croissant Format Specification, Version 1.1, published 2026-01-29 (copyright MLCommons Association and contributors, licensed under CC BY-ND 4.0; its property names are listed below to identify them, and no other part of it is reproduced), opened at docs.mlcommons.org.
3. European Commission, Template for the Public Summary of Training Content for general-purpose AI models, C(2025) 5235 final, 24 July 2025 (Article 53(1)(d) of Regulation (EU) 2024/1689), opened at the Commission's library page; the section headings were read from a copy of the Commission's document.
4. California Civil Code section 3111 (Assembly Bill 2013), paragraphs (a)(1) to (a)(12), opened at california.public.law, a republication.
5. National Institute of Standards and Technology, NIST AI 300-1, initial public draft (the file NIST.AI.300-1.ipd in NIST's publications library, as listed on 2026-11-24): named only; this edition does not map it.

**OASIS Data Provenance Metadata 1.0, CSD01 (section 5: Source 5.2, Provenance 5.3, Use 5.4)**

| Outside field | Annex A field | Class |
|---|---|---|
| Source: `title` | `components[].description` | carried |
| Source: `id` | `components[].component_id` | carried |
| Source: `location` | none | not carried |
| Source: `issuer` | `components[].source` | stricter |
| Source: `description` | `components[].description` | carried |
| Provenance: `source` | `components[].source` | stricter |
| Provenance: `origin` | `components[].custodians` | stricter |
| Provenance: `origin-geography` | none | not carried |
| Provenance: `date` | none | not carried |
| Provenance: `previous-date` | none | not carried |
| Provenance: `generation-period` | none | not carried |
| Provenance: `generation-method` | `components[].collection_method` | carried |
| Provenance: `format` | none | not carried |
| Provenance: `sub-provenance` | none | not carried |
| Use: `classification` | `health_data.present`; `financial_data.classes` | stricter |
| Use: `consent` | `components[].rights_basis.basis_detail` | stricter |
| Use: `data-risk-reducing` | `de_identification.method` | stricter |
| Use: `processing` | none | not carried |
| Use: `storage` | none | not carried |
| Use: `license` | `components[].rights_basis.terms_traveling` | carried |
| Use: `intended-purpose` | none | not carried |
| Use: `copyright` | `components[].rights_basis.basis_detail` | stricter |
| Use: `patent` | none | not carried |
| Use: `trademark` | none | not carried |

**MLCommons Croissant 1.1 (properties, by name)**

| Outside field | Annex A field | Class |
|---|---|---|
| `name` | `components[].component_id` | carried |
| `description` | `components[].description` | carried |
| `license` | `components[].rights_basis.terms_traveling` | stricter |
| `url` | none | not carried |
| `creator` | `components[].source` | stricter |
| `datePublished` | none | not carried |
| `dct:conformsTo` | none | not carried |
| `keywords` | none | not carried |
| `publisher` | `accountable_person.organization` | stricter |
| `version` | none | not carried |
| `dateCreated` | none | not carried |
| `dateModified` | none | not carried |
| `sameAs` | none | not carried |
| `sdLicense` | none | not carried |
| `inLanguage` | none | not carried |
| `distribution` | `delivery.manifest_hash` | stricter |
| `isLiveDataset` | `term.kind` | stricter |
| `citeAs` | none | not carried |
| `sdVersion` | none | not carried |
| `sha256` | `delivery.manifest_hash` | stricter |
| `recordSet` | none | not carried |
| `prov:wasDerivedFrom` | `components[].source` | stricter |
| `prov:wasGeneratedBy` | `components[].collection_method` | carried |
| `prov:wasAttributedTo` | `components[].custodians` | stricter |
| `usageInfo` | `components[].rights_basis.terms_traveling` | carried |

**European Commission template, C(2025) 5235 final (by section)**

| Outside field | Annex A field | Class |
|---|---|---|
| 1.1 Provider identification | none | not carried |
| 1.2 Model identification | none | not carried |
| 1.3 Modalities, overall training data size and other characteristics | none | not carried |
| 2.1 Publicly available datasets | `components[].source` | stricter |
| 2.2.1 Datasets commercially licensed by rightsholders or their representatives | `components[].rights_basis` | stricter |
| 2.2.2 Private datasets obtained from other third parties | `components[].collection_authority` | stricter |
| 2.3 Data crawled and scraped from online sources | `components[].collection_method`; `components[].collection_authority` | stricter |
| 2.4 User data | none | not carried |
| 2.5 Synthetic data | `synthetic_data.generators` | stricter |
| 2.6 Other sources of data | `components[]` | stricter |
| 3.1 Respect of reservation of rights from text and data mining exception or limitation | `components[].rights_basis.exclusion_mechanism` | stricter |
| 3.2 Removal of illegal content | none | not carried |
| 3.3 Other information (optional) | none | not carried |

**California Civil Code section 3111(a) (by paragraph)**

| Outside field | Annex A field | Class |
|---|---|---|
| (a)(1) | `components[].source`; `components[].custodians` | stricter |
| (a)(2) | none | not carried |
| (a)(3) | none | not carried |
| (a)(4) | `components[].description` | carried |
| (a)(5) | `components[].rights_basis.basis` | stricter |
| (a)(6) | `components[].rights_basis.basis` | stricter |
| (a)(7) | `de_identification`; `health_data`; `financial_data` | stricter |
| (a)(8) | none | not carried |
| (a)(9) | `de_identification.method` | stricter |
| (a)(10) | none | not carried |
| (a)(11) | none | not carried |
| (a)(12) | `synthetic_data.present` | stricter |

Row (a)(12) maps a statement about the developer's system to a statement about one delivery. The vendor's answer is an input to the developer's statement and does not make it.

**Fields of Annex A that none of the four carries.** Among them: `schema_version`, `declaration_id`, `declared_at` and `expires_at`; the time-stamp token hash in `delivery`; the measurement fields of `de_identification` (`attacker_assumed`, `measured_on`, `residual`, `tier`, `measurement_record_hash`); the whole of `attestation`, with the attester, the fee form and `certificate_id`; `evidence_package`; `evaluation_use`; `deletion_propagation`, with `receipt_id`; `relationship_disclosure`; `signature`; and the blocks `human_data`, `sensor_records` and `rl_environment`. The blocks `health_data`, `financial_data`, `term` and `synthetic_data` are reached by one outside field or two, as the tables show, and carry more than those fields ask.

**Conversion.** The same mapping is published as `crosswalk-0.3.0.json` beside the schema, and the validator converts an OASIS record into a partial declaration with `python3 validate.py convert record.json`. The conversion moves text only: it prints each field it wrote, with its class, writes the Use elements `consent` and `copyright` into `rights_basis.basis_detail`, and leaves the rest, among them the Use element `classification` (health and financial data) and the Provenance element `sub-provenance`, for the vendor to complete. A declaration produced by conversion is partial and unsigned and meets no tier. A requirement is at D once a named person at the vendor has completed its fields and signed the declaration (Part 3's definition of D), and at M or A only on the evidence those tiers require.

The schema, the example, the validator and the crosswalk file are published beside this document.

