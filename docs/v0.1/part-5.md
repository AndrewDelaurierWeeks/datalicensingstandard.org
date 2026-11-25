## 5. The scoring sheet

One sheet per vendor per delivery. Score each requirement at the tier the evidence supports. The thresholds are the buyer's to set; two suggested thresholds are shown as a starting point.

| Requirement | Tier reached (D, M, A, none, met, not met, N/A) | Evidence present (yes or no) | Assertion recorded (yes or no) | Notes |
|---|---|---|---|---|
| R1 Provenance and custody | | | | |
| R2 Rights and consent basis | | | | |
| R3 De-identification as a measurement | | | | |
| R4 Independence of attestation | | | | |
| R5 Evidence package | | | | |
| R6 Health data | | | | |
| R7 Term and re-measurement | | | | |
| R8 Evaluation data | | | | |
| R9 Deletion propagation | | | | |
| R10 Disclosure of relationships | | | | |
| R11 Financial and payment data | | | | |
| R12 Hosted environments | | | | |
| Total and maximum (applicable requirements only) | | | | |
| Thresholds used | | | | |
| Scored by; date | | | | |

**Scoring.** None = 0, D = 1, M = 2, A = 3 per requirement. R4 and R10 are scored met (3) or not met (0). Where a requirement carries a second tier paragraph for one form of delivery (the sensor-record block under R1, contributor agreements under R2) and the delivery contains that form, the requirement is scored at the lower of the two tiers reached, and the Notes column records both. The consent and de-identification records named in the sensor-record block's A line count toward R1 only; R2 and R3 are scored on their own tier lines. A sentence in a tier line that names a form (an environment run for the buyer, an RL environment sold or licensed for training) replaces, for that form, only the tier it names; the other tiers of the general line apply to that form as written. A requirement that does not apply to the delivery is recorded as N/A with the reason and is excluded from the total: R3 when nothing is described as de-identified and none of its paragraphs on synthetic data, sensor records or RL environments applies, R4 when no attestation is offered, R6 when no component contains or is derived from health information, R7 when the delivery is one-time and none of its sentences on RL environments or sensor records applies, R8 when the delivery is not intended for evaluation and none of its paragraphs on synthetic data or RL environments applies, R11 when no component contains or derives from any of its three classes and the search that supports that answer is recorded, R12 when the delivery contains no RL environment, or the buyer's agent runs only on systems the buyer controls and no trace or output leaves them. An assertion recorded against any requirement caps that requirement at 0 until the vendor withdraws it or replaces it with a declared answer. The answer to the last part of question 11 is recorded in the Notes column and changes no score.

**Suggested thresholds.** For a purchase intended for training a released model: every applicable requirement at D or better, with no answer of "unknown" on R1 or R2; R1 and R5 at M or better; R3 at M or better where a de-identification claim is made, and at D or better where it applies without one; R4 met where it applies; R10 met; R11 at M or better where it applies. For a purchase used in evaluation: additionally R8 at M or better. A buyer may set its own thresholds; the sheet records the thresholds used beside the score.

**What the sheet is for.** Comparison across vendors on the same questions; a record, kept where the buyer's counsel directs, of what was asked, what arrived and what was missing; and a record of the diligence performed, in a form a later reader can check. The sheet records what a vendor supplied and how the buyer scored it under this document; what a completed sheet means in law is for the buyer's counsel and the court.

From The Data Licensing Standard for AI (TDLS-AI) v0.1 (Weeks, 2026), CC BY 4.0. The thresholds, and the judgment on any dataset, are the buyer's; the document contains no legal advice.

