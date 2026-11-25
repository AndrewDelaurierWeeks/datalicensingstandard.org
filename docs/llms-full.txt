---
title: "The Data Licensing Standard for AI"
subtitle: "Requirements, evidence and scoring for AI training data vendors"
scope_line: "Licensed datasets, human data, synthetic data, sensor records, evaluation data and RL environments, and the brokers, marketplaces and vendors that supply them."
version: "Version 0.1 (v0.1), public draft for adoption"
author: "Andrew Delaurier Weeks"
credentials: "PCI DSS assessment work, Fortune 500 payment environments; ISO/IEC 27001:2022 Lead Auditor certification"
credentials_full: "PCI DSS assessment work, Fortune 500 payment environments; ISO/IEC 27001:2022 Lead Auditor certification (Mastermind Assurance, 2025); Certificate of Cloud Security Knowledge v5; CompTIA Security+; former security-operations analyst at a financial institution; business-continuity and disaster-recovery practitioner; systems developer in Rust."
capacity_cover: "Written in a personal capacity; not on behalf of, or reviewed by, any employer."
capacity: "Written and published by the author in a personal capacity. No employer or client of the author took part in it, reviewed it, or is bound by it, and no employer of the author has any role in the practice described in Part 6. Reading it forms no engagement and no professional relationship. It is a procurement standard; it contains no legal advice and is no audit, certification or assurance of any result."
title_display: "The Data Licensing Standard for AI"
short_name: "TDLS-AI"
serial: "TDLS-AI 0000 0002 A"
date: "2026-11-24"
license: "Text: Creative Commons Attribution 4.0 International. Schema, example, validator and crosswalk: MIT License."
---

## 0. How to use this document

The Data Licensing Standard for AI (TDLS-AI) v0.1 is written for the people at a laboratory or company who decide a purchase of training data or of a reinforcement-learning (RL) environment. Two of them usually decide it: counsel and the data-acquisition lead. Others use parts of it: the evaluation lead, the robot-learning and perception teams, and the engineers who run procurement systems.

**Counsel** reads Parts 1 to 3, Part 6 and Annex B. Those parts state the requirements, the evidence that satisfies each one, and the rules the requirements rest on, quoted from the source named in Annex B with the date each was opened.

**The data-acquisition lead** reads Part 4 (the vendor questionnaire) and Part 5 (the scoring sheet). Those two parts are the operational instrument: send the questionnaire to a vendor, score the answers, and keep the sheet where the buyer's counsel directs.

**The evaluation lead** reads Requirement 8, Requirement 12 where the buyer's agent or its traces leave the buyer's systems, and the sampling language in Requirement 3.

**Robot-learning and perception teams** read the sensor-record block in Annex A and the paragraphs on sensor records in Requirements 1 to 3.

**Engineering and procurement systems** use Annex A: a machine-readable schema for the vendor's declaration, with an example, a validator and a crosswalk from outside specifications, so the declaration can be requested, stored and checked by a tool rather than read from a PDF.

Nothing here is legal advice. The rules are quoted as they stood at the source named in Annex B, which for some is a republication; the requirements are written in the form of an assessment procedure: stated scope, stated sampling, evidence that someone outside the transaction can check.

This document is one author's work. No standards body, regulator, court, party or publisher named in it developed, reviewed, approved or endorsed it. Each such name identifies that body's own text or record or, in the author's credentials, the subject of his work and training.

**Conflict disclosure.** The author expects to perform attestation work of the kind Requirement 4 describes through a practice of his own, described in Part 6, and states its rules there; he is also building other businesses in this market, whose work Part 6, rule 3 bars the practice from attesting. Requirement 4 is met by any independent party, including existing audit and assurance firms; no attester receives preference under this document, and the author's own practice is subject to Part 5 like any other. Those other businesses may supply evidence of kinds this document names, among them logs and receipts of the form R9's M line names. Evidence is scored on the tier line it meets, whoever supplied it, and no source of evidence receives preference under this document.

## 1. Purpose and scope

**Purpose.** To give a buyer of training data or RL environments a fixed set of questions, a fixed evidence package and a scoring method that make the diligence on a vendor repeatable across vendors and checkable by someone who did not take part in the purchase.

**Scope.** Any acquisition of data or of an RL environment for training, fine-tuning, evaluation or environment construction from a party outside the buyer.

**The parties.** A data owner selling its own records; a broker or marketplace, including a marketplace or hub of RL environments; a de-identification or redaction provider delivering a processed corpus; a collector of recorded footage or calls; a collector of robot, teleoperation or wearable sensor records; a seller of human data made to order (demonstrations, preference labels, annotations and written reasoning produced by a contracted workforce); a generator of synthetic data; a seller of tasks and traces; an environment builder or host. Annex C defines the word this document uses for whichever of them supplies the delivery and signs the declaration, the vendor.

**The forms.** Text, images, documents, structured records, audio and video; synthetic and model-generated data; sensor records, which are time-series records from sensors on a robot, a person or a fixed rig (camera video in color and depth, lidar, inertial, force and torque, tactile, joint positions, velocities and torques, the actions or commands sent, and the audio and location recorded with them), including teleoperation and demonstration episodes and egocentric video; derived artifacts such as reinforcement-learning tasks; and RL environments, each made of the environment software, its task set, its graders or verifiers and the data inside, whether delivered to the buyer or run for the buyer by the vendor or another party, and whether bought directly or through a marketplace.

**Out of scope.** The buyer's own internal data; the buyer's model training practices; any statement about a particular vendor, buyer or dataset. The document says what a buyer should ask, what evidence should arrive, and how to score what arrived, and leaves the judgment about any given dataset to the buyer. The requirements are a part of a buyer's diligence and leave the rest to the buyer and its counsel. This edition sets no requirement specific to the following: data licensed for use without a delivered copy, other than the data inside an RL environment that the vendor or another party runs for the buyer; any measurement of whether an environment's graders score correctly; any rule of law this document does not quote or cite, in the jurisdictions it names and in every other; unlawful content; and children's data. A delivery that raises any of them is still subject to Requirements 1 to 12, and the questions they raise are for the buyer and its counsel.

**Why the questions are fixed.** A vendor answers the same questions for every buyer, so the answers can be compared; a buyer asks the same questions of every vendor, so a missing answer is visible as a missing answer rather than as a difference in style.

## 2. The record this rests on

The rules and standards numbered below are the record this document rests on: United States federal court rules, regulations and statutes, state statutes, a European regulation with an opinion of the European Data Protection Board, and the standards of ISO/IEC, the IETF and the PCI Security Standards Council; each is quoted or cited in Annex B, with the source and the date wherever the text was opened.

1. **Evidence rules.** Federal Rule of Evidence 902(13) and (14) make certain electronic records and copied data self-authenticating when a qualified person certifies them and the other side is given notice. A delivery that arrives with a hash manifest and a certification by a qualified person is in the form Rule 902(13) and (14) describe; whether the record is self-authenticating, whether it is admissible, and every other question remain for counsel and the court.
2. **De-identification rules.** 45 CFR 164.514 defines when health information is not individually identifiable, and offers two methods: an expert determination by a person with appropriate knowledge and experience who documents the methods and results, or the removal of a listed set of identifiers with no actual knowledge that the remainder could identify someone. The expert-determination structure, a named person applying stated methods and documenting the result, is the model this document uses for every de-identification claim, whether or not the data is health data.
3. **Independence rules.** 17 CFR 210.2-01 states the standard under which the Securities and Exchange Commission recognizes an accountant as independent, and treats a contingent fee, a fee that depends on a finding or result, as inconsistent with independence. ISO/IEC 17021-1:2015 requires a certification body to be impartial (clauses 5.2.1 and 5.3.2). These are rules that auditors of SEC registrants and management-system certification bodies work under, and they are the model for any attestation a vendor offers.
4. **Timestamp standards.** RFC 3161 defines a time-stamp token issued by a third-party authority that evidences, on trust in that authority, that a hash existed before the time stated. For context only, since no requirement in this edition depends on it: Certificate Transparency (RFC 6962, the version deployed on the public web, and RFC 9162, its Experimental successor) is the precedent for an append-only public log that anyone can audit.

5. **Financial-data rules.** PCI DSS v4.0.1 defines account data (the primary account number, cardholder name, expiration date and service code, and the sensitive authentication data: full track data, card verification code, PINs and PIN blocks), forbids storing sensitive authentication data after authorization even if encrypted (issuers excepted under 3.3.3), and names the four approaches that render a stored primary account number unreadable. 15 U.S.C. 6802 conditions a financial institution's disclosure of nonpublic personal information to a nonaffiliated third party on notice and an opportunity to opt out, with stated exceptions. 15 U.S.C. 1681b lists the circumstances under which a consumer reporting agency may furnish a consumer report "and no other". A delivery that contains or derives from any of these classes is answerable in their vocabulary: which class, what was removed or rendered unreadable and how, and under which notice, exception or purpose the data left the institution that held it.

6. **European data-protection rules.** Regulation (EU) 2016/679, with an opinion of the European Data Protection Board, is the source of three mechanisms this document borrows. Recital 26 judges whether a person is identifiable by "all the means reasonably likely to be used", by the controller or by another person. Article 19 has a controller communicate an erasure to each recipient to whom the personal data have been disclosed, "unless this proves impossible or involves disproportionate effort". The Board's Opinion 28/2024 says that supervisory authorities should take into account whether a controller deploying a model "conducted an appropriate assessment" to ascertain that the model was not developed by unlawfully processing personal data (paragraph 129, quoted in part), and its paragraph 58(c) speaks of "the specific measures for each source of training datasets" (quoted in part); the setting of each paragraph is in the Opinion. The three mechanisms are those of Recital 26, Article 19 and paragraph 58(c); paragraph 129 is quoted for context, and no requirement rests on it. The Regulation applies to controllers and processors within its material and territorial scope (Articles 2 and 3); whether a vendor or buyer is within it is for counsel. Where one is outside it, this document applies the three mechanisms as the model, as R6 applies 164.514; for one inside it, this document restates none of the Regulation's obligations. The text is quoted as it stood at the source on the date opened (Annex B.11); nothing here states that any delivery complies with the Regulation.

7. **Biometric-privacy rules.** 740 ILCS 14/15(b) forbids a private entity to "collect, capture, purchase, receive through trade, or otherwise obtain" a person's biometric identifier or biometric information unless it first gives written notice and receives a written release. Section 10 lists a "voiceprint" and a "scan of hand or face geometry" among biometric identifiers and says they "do not include" photographs (Annex B.12). Section 10 lists other identifiers too, among them a retina or iris scan and a fingerprint. Of the whole list, R2 and question 20 name two, face-geometry scans and voiceprints, and the rest of the list is for counsel. A delivery of sensor records that carries face-geometry scans or voiceprints is answerable in that vocabulary: whose, and under what notice and release; R2 and question 20 ask it. Section 15(b) is one provision of the Act, and its other provisions are not summarized here. Whether a recording of a face or a voice is reached before any scan or print is computed, and what the Act asks of a buyer that computes one, are questions for counsel. The Act is Illinois law; whether it reaches a vendor, a buyer or a delivery is for counsel, and this document uses its vocabulary as the model, as R6 applies 164.514. Nothing here states that any delivery complies with the Act.

8. **Training-data disclosure rules.** California Civil Code section 3111 has the developer of a generative artificial intelligence system or service post documentation of the data used to train it; paragraph (a)(12), on synthetic data generation, is quoted in Annex B.10 and cited in R1. Whether the section applies to a buyer is a question for counsel.

**Why now.** In 2026 a federal court granted final approval of a class settlement over books downloaded from two shadow libraries for use as training data, with the figures on the docket (Annex B.6). Final judgment has been entered in the district court; appeals were pending when the docket was opened (Annex B.6). Whatever the outcome on appeal, the questions this document fixes are ones a buyer can answer before a purchase.

## 3. Requirements

Each requirement states what the buyer requires, the evidence that satisfies it, the rule it rests on, and the tiers at which a vendor can meet it. The tiers are the heart of the method:

- **Declared (D):** the vendor states the answer in writing, in the declaration (Annex A), and the statement is attributable to a named person at the vendor.
- **Measured (M):** the answer is backed by a measurement, made by the vendor or verified by the buyer: method, sample, date, who ran it, and what was left over.
- **Independently attested (A):** a party independent of the vendor, of any de-identification or redaction provider, and of any broker or marketplace in the transaction, under a fee fixed before the result was known, attests the measurement and signs it.

"Not measured" and "unknown" are admissible answers at tier D. A vendor that discloses what it did not do has met the declared tier for that requirement; a vendor that asserts what it did not measure has met no tier. The scoring sheet rewards disclosure and penalizes assertion.

Requirements 1 to 11 keep the numbers they had in the edition of 2026-11-16; Requirement 12 is new. Where a requirement asks something more of one form of delivery (synthetic data, human data made to order, sensor records, an RL environment), a paragraph headed with that form, or a sentence that names it, says so, and a delivery without that form skips it. Where one delivery is several forms at once (an environment whose records a model wrote, or whose tasks a contracted workforce wrote), each paragraph applies to the part it names, and a share is stated for data components only.

Each requirement ends with guidance: its purpose, what the buyer checks, good practice, illustrative examples, and where a check fails. Guidance explains the requirement. It adds to no requirement, changes no tier and changes no score. Part 0's conflict disclosure applies to the guidance as to the rest of this document.

### R1 · Provenance and chain of custody

**Requirement.** The vendor states where each component of the delivery came from, how it was collected, who held it between collection and delivery, and under what authority. The delivery is identified by a hash manifest: a cryptographic hash of every file delivered and of the manifest itself, with the hash algorithm named.

**Synthetic and model-generated data.** For each synthetic component, the vendor states the generator (its name, its version or build, its provider, and whether it is another party's model, the vendor's own model or a program that is no model), the generation method in outline, the seed data with its own provenance under this requirement, and the component's share of the delivery in a named unit (records, tokens, files, bytes or hours). Where the buyer supplied the seed data, the vendor says so, and the provenance of that data is the buyer's to state.

**Sensor records.** The vendor completes the sensor-record block in Annex A: the embodiment, each sensor, calibration, time synchronization, action representation, control rate, collection method, episodes and tasks, success labels, environments, data quality, format, and a hash manifest over every episode file. Each value is declared in the unit the block fixes. This document sets no tolerance: the vendor declares the measured value, or marks the field "not-measured", and the buyer sets the threshold, as Part 5 leaves every threshold to the buyer.

**RL environments.** The vendor states the provenance of each part of the environment: who wrote the tasks and who wrote the graders or verifiers, by kind (the vendor's staff, a contracted workforce, a model, another party), and where any data inside came from. Names of individuals are not required. The hash manifest covers the build: every file delivered, or the image digest of a container, with the task set and the grader files covered by it. For an environment run for the buyer, the manifest identifies the build the buyer's agent runs against.

**Evidence.** The hash manifest (SHA-256 or stronger); a provenance statement per source; for any component collected from a third party, the agreement or terms under which it was collected; a third-party time-stamp token (RFC 3161) over the manifest hash, which evidences, on trust in the authority that issued it, that the manifest existed in that form before the time stated. For synthetic data, the generator statement. For sensor records, the completed block. For an RL environment, the build digest, the task count, the task list or its SHA-256, and the grader version. The list itself is delivered where the tasks are delivered to the buyer; a held-out or hosted task set is named by its count and its hash.

**Rule basis.** FRE 902(14) (in summary; quoted in B.1): data copied from a device, medium or file is self-authenticating if authenticated by a process of digital identification, when a qualified person provides the certification Rule 902(11) or (12) describes and the notice requirement is met. The manifest is the process, and the certification the qualified person's certification, that the rule names; whether they satisfy it is for counsel and the court. For synthetic data, no rule is quoted for the generator, the seed data or the share. California Civil Code section 3111 (quoted in part in B.10) is the occasion: it has the developer of a generative artificial intelligence system or service post documentation that includes, at paragraph (a)(12), whether the system or service "used or continuously uses synthetic data generation in its development". Whether a buyer owes that documentation, and whether a delivery is synthetic data generation as the section uses the phrase, are questions for counsel; the vendor's answer is a fact counsel can use. For a statement made source by source, paragraph 58(c) of Opinion 28/2024 of the European Data Protection Board (quoted in part in B.11) is the model: its words concern measures stated for each source of training datasets, and this document borrows the per-source form.

**Tiers.** D: the statement and the manifest. M: the manifest verified by the buyer against the delivery, and the time-stamp token verified. A: the manifest, token and provenance statement attested by an independent party. For an environment run for the buyer, M: the time-stamp token verified; the environment reports its build digest at the start of each run, and the buyer records that the digest reported equals the digest declared. The digest reported is the environment's own report.

**Tiers for the sensor-record block.** D: every required field declared, each measured field declared or marked "not-measured" (label agreement is left out where it was not measured), and each conditional field declared or marked "not-present" or "not-done". M: the measured fields (synchronization offset, dropped frames, gaps, episodes discarded, and label agreement where it was measured) backed by the vendor's measurement on a stated sample of episodes, or recomputed by the buyer from the timestamps delivered; the calibration files, where cameras were used, delivered and checked on a sample. A: the measured fields and the consent and de-identification records attested by an independent party on a sample it drew.

::: guidance
[Guidance for R1]{.gt} [Adds to no requirement · changes no tier or score]{.gl}

Purpose
:   Provenance says where each part of the delivery came from and who held it. The hash manifest fixes what was delivered, so that every later question about the data is asked of the same files.

What the buyer checks
:   1. **Manifest matches.** Recompute, with the algorithm the manifest names, the hash of every file listed and of the manifest; every value matches.
    2. **Token verifies.** The time-stamp token verifies against the authority's certificate, and the hash it carries equals the manifest hash.
    3. **Sources named.** Each component names its source, collection method, custodians and authority.
    4. **Third-party terms present.** For each component collected from a third party, the agreement or terms are attached or cited by title and date.

    A buyer may record each result in the Notes column of Part 5, as its counsel directs, and may set any check as a threshold of its own.

Good practice
:   - Make the manifest from the files as delivered, at the moment of delivery, and time-stamp it the same day.
    - State custody as a chain: each holder, the dates held, and how the data moved between them.
    - For a synthetic component, name the generator by version or build, so that a later reader can identify it.
    - For an RL environment run for the buyer, have the environment report its build digest at the start of every run.

Examples, illustrative
:   - **M** · **A manifest and its token.** A manifest of 4,812 files with SHA-256 values and an RFC 3161 token dated the day of delivery; the buyer recomputed every hash and verified the token.
    - **D** · **A table and a manifest.** A provenance table per component and a manifest; the buyer has not yet recomputed the hashes.
    - **assertion** · **A claim with no table.** “All data ethically sourced from public sources.” No component table and no manifest; an assertion is recorded.

Where a check fails
:   - A hash that differs from the delivered file shows the file differs from the one the manifest lists; check 01 finds it.
    - A token over a hash other than the manifest's covers some other file; check 02 finds it.
    - A source given as a category, such as “web data”, with no collection method or authority; check 03 finds it.
:::

### R2 · Rights and consent basis

**Requirement.** For each component, the vendor states the right under which it may be licensed for training (ownership, license, consent, public-domain status, or a statutory basis), the terms that travel with it (field-of-use limits, attribution, sublicensing, term), and the mechanism by which an individual or rights holder can exclude their material.

**Synthetic and model-generated data.** For each generator another party provides, the vendor names the agreement or license under which it used the generator on the dates of generation (its title and date, and the channel through which the generator was used) and quotes any clause that limits the use of outputs to train models. Where the agreement is confidential, a named person states whether it holds such a clause and what the clause forbids. For the vendor's own generator, the vendor says so and, where it was built on another party's model, names that model's license. The vendor also states the rights in the seed data, and whether and how an exclusion request against the seed data changes the synthetic component. Whether a provider's terms bind the buyer is a question for counsel.

**Human data made to order.** Where the delivery was produced to order by a contracted workforce (demonstrations, preference labels, annotations, written reasoning), the vendor names the contributor agreements: the assignment or license of each contributor's work to the vendor, the contributor's consent to its use in training, and any limits. Where the work carries the contributor's own personal data (a voice, a face, a name), the vendor states the consent basis for it.

**Sensor records.** The vendor states the consent basis of operators, camera wearers and others recorded, with the procedure for withdrawal; for capture in a home, a workplace or another private space, the permission of the occupant or owner; and, for teleoperators, the contributor agreements above. Where the records carry face-geometry scans or voiceprints, the vendor states whose, by kind of person and count, and the written notice and release each was obtained under.

**RL environments.** The vendor states the license of the environment code, of each data component inside, and of any third-party software or copied interface inside that carries its own license; the terms that travel (field of use); and the exclusion mechanism for data inside. Exclusivity is stated once, under R8.

**Evidence.** The rights statement per component; copies of licenses or consent language; the exclusion mechanism and its service level; a log of exclusion requests received and honored, in aggregate. For human data made to order, the agreement template and the counts of contributors and of signed agreements.

**Rule basis.** No rule is quoted for the requirement as a whole; the occasion is the settlement record (Part 2 and Annex B.6). For the consent basis of people recorded in sensor records, the occasion is 740 ILCS 14/15(b) (lead-in quoted in B.12). This document requires that the basis be stated so that counsel can evaluate it, and takes no position on any copyright question.

**Tiers.** D: the statements. M: the exclusion log produced from the vendor's system, with counts and dates. A: the statements and the log attested by an independent party who sampled the records.

**Tiers for contributor agreements.** D: the agreement template, the count of contributors in the delivery and the count who signed it. M: the two counts produced from the vendor's system. A: the counts attested on a sample.

::: guidance
[Guidance for R2]{.gt} [Adds to no requirement · changes no tier or score]{.gl}

Purpose
:   R2 has the vendor state, for each component, the right under which it may be licensed for training, the terms that travel with it, and how a person or rights holder can exclude their material.

What the buyer checks
:   1. **A basis per component.** Each component names one basis from R2's list: ownership, license, consent, public-domain status or a statutory basis.
    2. **Terms stated.** Field-of-use limits, attribution, sublicensing and term are stated for each component.
    3. **Exclusion that works.** The exclusion mechanism can be reached by the public, and the log shows requests received and honored, with dates.
    4. **Agreements counted.** For human data made to order, the count of signed agreements equals the count of contributors in the delivery.

    A buyer may record each result in the Notes column of Part 5, as its counsel directs, and may set any check as a threshold of its own.

Good practice
:   - Quote the clause that grants training use, since a license title alone leaves its scope unknown.
    - For synthetic data, quote any clause of the generator's terms that limits training on its outputs.
    - Keep the exclusion log in the system that receives requests, so that its counts come from records.
    - For sensor records, record consent before capture, and keep the withdrawal procedure with each episode.

Examples, illustrative
:   - **M** · **Rights, licenses and a log.** Rights per component, the license texts, and an exclusion log exported from the intake system: 212 requests received in 12 months, 209 honored and 3 refused, each with its date received, its date honored or refused, and its reason.
    - **D** · **Rights stated.** Rights per component and the exclusion mechanism stated; no log attached.
    - **assertion** · **A claim with no basis.** “Fully licensed for any AI use.” No component, basis or license text; an assertion is recorded.

Where a check fails
:   - A basis given as “publicly available” is none of the bases R2 lists; check 01 finds it.
    - Fewer signed agreements than contributors; check 04 finds it.
    - An exclusion address that returns no reply and keeps no record; check 03 finds it.
:::

### R3 · De-identification, stated as a measurement

**Requirement.** Where the delivery is described as de-identified, anonymized, redacted or scrubbed, the vendor states the claim as a measurement: the attacker the de-identification assumes (what outside information and what access the attacker is taken to have), the method, the sample it was measured on and how the sample was chosen, the date, the person who ran it, and what was left over (the residual: records or fields that the method does not cover or did not clear). A claim of complete anonymization, or of a zero residual, is scored as an assertion at every tier; a determination of very small risk under 164.514(b)(1) states a residual and is scored on its documentation.

**Synthetic data.** Where the seed data held personal data, the vendor states, on a sample: the match rule (exact match on all fields, or a stated measure of closeness with its cutoff), the size of the sample and how it was drawn, the count of generated records that match a seed record under the rule, and what the test did not cover. A count of zero in a stated sample under a stated rule is a measured result for that sample and is scored as a measured result. The part of the delivery outside the sample, and any match rule not tested, are the residual. Where the vendor relies on a formal privacy bound that the generator was built to meet, it states the bound and its parameters beside the count.

**Sensor records.** Where people, places or location were recorded, the vendor completes the de-identification fields of the sensor-record block: what was removed (faces, number plates, screens and documents in view, voices, location traces), the method, the sample of frames, and the residual. Where nothing was removed, the vendor marks the fields "not-done", and the residual is everything recorded.

**RL environments.** This requirement applies where the environment contains personal data, such as records placed in it or recorded interactions, whether or not the vendor describes it as de-identified.

Where one of these paragraphs applies and the vendor claims no de-identification, the vendor says that nothing was removed and states what personal data remains and whose, by kind of person (names of individuals are not required); that statement is D. M and A are reached on a measurement the paragraph asks for (the match count for synthetic data) or on a removal or de-identification that is claimed.

**Evidence.** The declaration fields in Annex A (attacker assumed, method, sample, residual); the measurement record; for health data, the expert-determination documentation or the safe-harbor identifier list and the actual-knowledge statement.

**Rule basis.** 45 CFR 164.514(b)(1) (in summary; quoted in B.2): a person with appropriate knowledge and experience applies generally accepted principles and methods, determines that the risk is very small that the information could be used, alone or in combination with other reasonably available information, by an anticipated recipient to identify an individual, and documents the methods and results. The document uses this structure for all data: a named person, a stated method, a stated recipient or attacker, and documented results. Recital 26 of Regulation (EU) 2016/679 (quoted in B.11) judges identifiability by "all the means reasonably likely to be used", by the controller or by another person; the attacker assumed records which means the vendor considered, and whether those are all the means the Recital has in view is for counsel.

**Sampling language for the evaluation lead.** A measurement on a sample the vendor chose after seeing the buyer's questions is weaker than a measurement on a sample drawn by a procedure the vendor could not predict. The declaration records who drew the sample and when relative to the buyer's questions.

**Tiers.** D: the declaration fields stated (attacker assumed, method, sample, date, person, residual), with "not measured" and "unknown" permitted. M: the measurement record attached, or the measurement verified by the buyer. A: the measurement reproduced or verified by an independent party on a sample that party drew.

::: guidance
[Guidance for R3]{.gt} [Adds to no requirement · changes no tier or score]{.gl}

Purpose
:   Stated as a measurement, a de-identification claim names one attacker, one method, one sample and one residual. A buyer can then compare the claims of several vendors on the same terms, and a later reader can test each part.

What the buyer checks
:   1. **Attacker named.** The attacker is stated on the T0 to T5 scale of Annex A; an answer of none-stated is recorded in the Notes column.
    2. **Sample timing recorded.** The declaration records who drew the sample, how, and when relative to the buyer's questions.
    3. **Residual stated.** The residual is stated as R3 defines it for the form, or as not measured, and is other than zero or complete anonymization.
    4. **Record attached.** The measurement record is attached, or the buyer has reproduced the measurement.

    A buyer may record each result in the Notes column of Part 5, as its counsel directs, and may set any check as a threshold of its own.

Good practice
:   - Fix the sampling procedure before the buyer's questions arrive, and record who drew the sample and when.
    - State the attacker in the declaration. Which attacker fits the buyer's use is the buyer's judgment; Annex A gives T4 and T5 for attackers with access to a trained model.
    - Report the residual as a count and as a share of the sample, and name the fields the method does not cover.
    - Attach the measurement record to the declaration, so that the buyer can verify M without a second request.

Examples, illustrative
:   - **M** · **A measurement with its record.** Attacker T1; method: direct identifiers removed and dates generalized to the month; sample: 2,000 records drawn by a seeded random procedure fixed before the questionnaire arrived; residual: 14 records (0.7 percent) whose free-text fields the method does not cover; the measurement record attached.
    - **D** · **Fields stated.** Attacker, method, sample, date and person stated; the residual given as “not measured”.
    - **assertion** · **A claim with no measurement.** “Fully anonymized; zero re-identification risk.” An assertion is recorded, and R3 is capped at 0 until the vendor withdraws the claim or replaces it with a declared answer.

Where a check fails
:   - A residual of zero, or “fully anonymized”, is scored as an assertion; check 03 finds it.
    - A declaration that does not say who drew the sample or when; check 02 finds it.
    - An attacker given as none-stated cannot be compared with another vendor's; check 01 records it.
:::

### R4 · Independence of any attestation offered

**Requirement.** Any attestation, audit, certification or verification that the vendor offers in support of any requirement must come from a party that is independent of the vendor, of any de-identification or redaction provider in the transaction, and of any broker or marketplace that sells or lists the data; and that party's fee must be fixed before the result is known and must not depend on the finding, the sale or the price. A vendor's own check of its graders, generators or sensors is the vendor's evidence at D or M under the requirement the check supports, and R4 does not apply to it. The documents R6 and R11 name (an expert determination, an attestation of compliance, a report on compliance) are evidence under those requirements; R4 applies to an attestation of them offered at tier A.

**Evidence.** The attester's identity and its disclosed relationships with every party in the transaction; the fee arrangement in a form that shows it was fixed before the result was known and is independent of the result; prior engagements between the attester and any party, disclosed.

**Rule basis.** 17 CFR 210.2-01(b) (in summary; quoted in B.3): an accountant is not independent if a reasonable investor with knowledge of all the facts would conclude that the accountant is not capable of exercising objective and impartial judgment; 210.2-01(c)(5): an accountant is not independent if it provides any service for a contingent fee or receives one from the client; 210.2-01(f)(10): a contingent fee is any fee whose amount depends on the finding or result. ISO/IEC 17021-1:2015, clauses 5.2.1 and 5.3.2: impartiality is required of a certification body. These rules are quoted or cited in Annex B.

**Tiers.** Met or not met. When no attestation is offered, R4 is not applicable and is excluded from the total. When an attestation is offered and is independent under the rule above, R4 is met. When it is offered and is not independent, R4 is not met and the attestation is disregarded, and the requirements it supported are scored on the vendor's own evidence.

::: guidance
[Guidance for R4]{.gt} [Adds to no requirement · changes no tier or score]{.gl}

Purpose
:   An attestation is worth what the attester's independence is worth. R4 asks who the attester is, what ties it has to each party, and how it was paid, so that the buyer can judge the attestation before relying on it.

What the buyer checks
:   1. **Relationships disclosed.** The attester lists its relationships with the vendor, any de-identification or redaction provider, and any broker or marketplace.
    2. **Fee fixed in advance.** The engagement letter shows a fee fixed before the result was known.
    3. **Fee apart from the outcome.** No part of the fee depends on the finding, the sale or the price.
    4. **Prior engagements listed.** Prior engagements between the attester and any party are listed.
    5. **Independent.** No relationship disclosed ties the attester to the vendor, a de-identification or redaction provider, or a broker or marketplace in the transaction.

    A buyer may record each result in the Notes column of Part 5, as its counsel directs, and may set any check as a threshold of its own.

Good practice
:   - Ask for the engagement letter, dated before the work began, with the fee stated.
    - Ask the attester, as well as the vendor, to sign the relationship disclosure.
    - A commission depends on the sale and a success fee on the result, so R4 excludes both.

Examples, illustrative
:   - **met** · **A fixed fee and full disclosure.** An attestation from a firm with no ownership ties or prior engagements with any party, under a fixed fee stated in a letter dated before the work began.
    - **not met** · **A share of the price.** An attestation from a firm paid 2 percent of the sale price; the attestation is disregarded and the requirements it supported are scored on the vendor's own evidence.
    - **N/A** · **No attestation.** No attestation is offered; R4 is excluded from the total.

Where a check fails
:   - A fee payable only on a clean result; check 03 finds it.
    - An attester owned by the marketplace that lists the data; check 05 finds it.
:::

### R5 · The evidence package

**Requirement.** Every delivery arrives with a package that a person outside the transaction can check without asking the vendor: the hash manifest (R1), the time-stamp token (R1), the declaration (Annex A) completed and signed by a named person, the measurement records (R3), and a certification by a qualified person in the form Rule 902(11) or (12) describes, so that the buyer can later give the notice Rule 902(11) requires. For sensor records the package adds the calibration files where cameras were used, the record of the time-synchronization measurement and the file or reference that defines the format. For an RL environment it adds the build digest, the task count, the task list or its hash, and the grader version.

**Evidence.** The package itself, with each element present and the manifest covering the delivered files, the measurement records and, where there is one, the signed questionnaire response.

**Rule basis.** FRE 902(11) (in summary; quoted in B.1): before the trial or hearing, the proponent must give an adverse party reasonable written notice of the intent to offer the record and must make the record and certification available for inspection, so that the party has a fair opportunity to challenge them. A buyer that assembles the package at purchase holds the record and certification Rule 902(11) names.

**Tiers.** D: the package complete. M: the package verified by the buyer (hashes recomputed, token verified, declaration validated against the schema). A: the package attested by an independent party. For an environment run for the buyer, M: the buyer recomputes the hashes of the files it received, verifies the token, validates the declaration against the schema and checks the reported build digest as in R1.

::: guidance
[Guidance for R5]{.gt} [Adds to no requirement · changes no tier or score]{.gl}

Purpose
:   The package lets someone outside the purchase check the delivery without asking the vendor. A buyer that keeps it holds a record and certification of the kind Rule 902(11) names; whether they meet the rule is for counsel and the court.

What the buyer checks
:   1. **Every element present.** Manifest, token, declaration, measurement records and the qualified person's certification are in the package.
    2. **Declaration validates.** The declaration validates with `python3 validate.py tdls-ai-vendor-declaration.schema.json <declaration>.json`.
    3. **Manifest covers the package.** The manifest lists the measurement records and, where there is one, the signed questionnaire response.
    4. **Certification signed.** The certification names a qualified person and is signed and dated.

    A buyer may record each result in the Notes column of Part 5, as its counsel directs, and may set any check as a threshold of its own.

Good practice
:   - Deliver the package with the data, in one folder that the manifest covers.
    - Name the certifying person by role and qualification.
    - For sensor records, include the calibration files and the time-synchronization record.

Examples, illustrative
:   - **M** · **A package the buyer verified.** Every element present; the buyer recomputed the hashes, verified the token and validated the declaration.
    - **D** · **A complete package.** Every element present; the buyer has not yet verified it.
    - **none** · **A partial package.** A declaration and data delivered with no manifest and no certification.

Where a check fails
:   - A declaration that fails the schema; check 02 finds it.
    - A certification that is unsigned or names no person; check 04 finds it.
:::

### R6 · Health data

**Requirement.** Where any component contains or is derived from health information, the vendor states which of the two methods in 45 CFR 164.514(b) was applied, and delivers the corresponding documentation: for an expert determination, the documented methods and results and the identity and qualifications of the person who made it; for the safe-harbor method, the list of identifiers removed and the statement that the vendor has no actual knowledge that the remainder could identify an individual. For sensor records, this requirement applies wherever the records contain health information, including physiological signals a wearable records; the vendor states its classification and the buyer's counsel judges it. It applies to data inside an RL environment as to any delivery. Health records that a person or a generator made up, with no real individual behind them, are stated as made up, with the method that made them. This document treats a synthetic component generated from real health information as derived from it, and this requirement applies. Whether a made-up record is health information is for the buyer's counsel; where counsel finds none, R6 is not applicable and the vendor's statement is kept in the Notes column.

**Evidence.** The documentation named above. A statement that data is "HIPAA compliant" with neither document is scored as an assertion.

**Rule basis.** 45 CFR 164.514(a), (b)(1) and (b)(2), quoted in Annex B. The rule binds covered entities and their business associates; where the vendor is neither, this document applies its two methods as the model.

**Tiers.** D: the method named and the documentation delivered. M: for an expert determination, its sample and results reproduced by the buyer; for safe harbor, identifier removal verified on a sample. A: the determination or the removal attested by an independent party. For data inside an environment run for the buyer, M: the vendor runs the check on a sample the buyer names and gives the buyer the record.

::: guidance
[Guidance for R6]{.gt} [Adds to no requirement · changes no tier or score]{.gl}

Purpose
:   45 CFR 164.514(b) gives covered entities two methods of de-identifying health information, and R6 applies them to every vendor as the model. R6 asks which method was used and for the documents that show it.

What the buyer checks
:   1. **Method named.** Expert determination or safe harbor, one of them named.
    2. **Documents fit the method.** For an expert determination, the methods, results and the expert's identity and qualifications; for safe harbor, the identifiers removed and the actual-knowledge statement.
    3. **Scope fits the delivery.** The determination names this data and the recipient it assumed.
    4. **Removal holds on a sample.** For safe harbor, a sample shows none of the listed identifiers.

    A buyer may record each result in the Notes column of Part 5, as its counsel directs, and may set any check as a threshold of its own.

Good practice
:   - Date the determination and name the recipient it assumed, since 164.514(b)(1) ties the determination to that recipient.
    - For wearables, state whether each physiological signal is classified as health information, and why.
    - Label made-up health records as made up, with the method that made them.

Examples, illustrative
:   - **M** · **A determination reproduced.** An expert determination for this delivery with its methods, results and the expert's qualifications; the buyer reproduced its sample results.
    - **D** · **Safe harbor documented.** Safe harbor named, the identifier list and the actual-knowledge statement delivered; not yet verified.
    - **assertion** · **A label with no documents.** “HIPAA compliant.” Neither document is delivered; an assertion is recorded.

Where a check fails
:   - A determination made for another dataset or another recipient; check 03 finds it.
    - An identifier on the rule's list found in the sample under safe harbor; check 04 finds it.
:::

### R7 · Term, renewal and re-measurement

**Requirement.** A declaration and its measurements describe the delivery they accompany. For a feed, a refresh or a license that renews, each delivery carries its own declaration, and the vendor states the interval at which de-identification and rights are re-measured. Each build of an RL environment that adds, removes or changes a task or a grader carries its own declaration. Its change log gives the counts of tasks added, removed and changed and names each grader that changed by file hash; it need not say how a grader works. For an environment that is updated continuously, the vendor states the interval at which it issues a declaration, and each declaration names the latest build by digest and lists in its change log the digests of the builds issued since the declaration before it. For sensor records, each recalibration or hardware change starts a new declaration, and the change log names it.

**Evidence.** The re-measurement interval in the declaration; a declaration per delivery; the change log between deliveries.

**Rule basis.** The structure of 164.514(b)(1), which ties the determination to the information and the anticipated recipient at the time it is made; a determination does not describe data it never covered.

**Tiers.** D: the interval stated. M: a declaration per delivery with the change log. A: the interval and the per-delivery declarations attested.

::: guidance
[Guidance for R7]{.gt} [Adds to no requirement · changes no tier or score]{.gl}

Purpose
:   A measurement describes the data it was made on. When the data changes, the declaration changes with it; R7 keeps each delivery tied to a declaration of its own.

What the buyer checks
:   1. **Interval stated.** The re-measurement interval is stated in the declaration.
    2. **A declaration per delivery.** Each delivery of a feed or renewal carries its own declaration and its own manifest hash.
    3. **Change log complete.** The change log counts what was added, removed and changed since the last declaration, and names each changed grader by file hash.
    4. **Next date.** The next declaration's due date follows from the interval, or from `expires_at` where given.

    A buyer may record each result in the Notes column of Part 5, as its counsel directs, and may set any check as a threshold of its own.

Good practice
:   - Set the interval by how fast the data changes, and state the reason.
    - For sensor records, start a new declaration at each recalibration or hardware change.
    - For an environment that is updated continuously, list in each declaration the digests of the builds issued since the last one.

Examples, illustrative
:   - **M** · **A declaration for each delivery.** A monthly feed with six declarations in six months, each with its manifest hash and a change log.
    - **D** · **An interval stated.** Quarterly re-measurement stated; no declaration yet for the monthly deliveries after the first.

Where a check fails
:   - One declaration reused across deliveries; check 02 finds it.
    - A grader changed with no file hash in the change log; check 03 finds it.
:::

### R8 · Evaluation data and contamination

**Requirement.** Where the delivery is intended for evaluation, benchmark construction or held-out testing, the vendor states whether any component has been published, sold or delivered to any other party, and in what form; whether it overlaps with public benchmarks the vendor checked; and how the vendor prevents the component from entering training sets it supplies.

**Synthetic data.** Whatever the intended use, the vendor states whether any benchmark item was used as seed data or placed in a prompt, and names the benchmark. Whether another party's generator learned benchmark items before the vendor used it is stated as unknown unless the vendor tested for it.

**Sensor records.** Where sensor records are intended for evaluation, the vendor states how held-out episodes, environments and robots are kept apart, and what overlap with public datasets it checked.

**RL environments.** The vendor states which tasks overlap public benchmarks and how held-out tasks are kept apart. The distribution statement also covers an RL environment sold or licensed for training. As of the date of the declaration, the vendor states whether any task or grader file in this build, or a version of one changed only in wording, values or format, has been sold, licensed or delivered to any other party, and in what form (the same build, a variant, or single tasks); the files of this build are identified by hash. The vendor also states the exclusivity terms it offers this buyer from that date: exclusive use (of what, and for how long), a first-buyer window (its length), or none (non-exclusive). The names of other parties and the terms of their contracts are not required.

**Evidence.** The distribution statement; the overlap check and its method; the vendor's separation procedure; for an RL environment sold or licensed for training, the exclusivity terms offered to this buyer.

**Rule basis.** None in law; this is the evaluation lead's requirement, and the document records it because a benchmark with an unstated distribution history measures nothing reliable. For an RL environment sold or licensed for training, the statement records the exclusivity terms the vendor declared.

**Tiers.** D: the statements. M: the overlap check attached. A: the distribution history and overlap check attested. For an RL environment sold or licensed for training, M: the signed offer or contract clause that states the exclusivity terms, attached, including terms of none. The statement of prior distribution is the vendor's own statement at D and at M, and R8 reaches A only when it is attested.

::: guidance
[Guidance for R8]{.gt} [Adds to no requirement · changes no tier or score]{.gl}

Purpose
:   An evaluation set measures a model only if the model has not seen it. R8 asks where the data has been, what it overlaps, and how the vendor keeps it out of the training sets it supplies.

What the buyer checks
:   1. **Distribution history.** The vendor states whether each component was published, sold or delivered elsewhere, and in what form.
    2. **Overlap method named.** The overlap check names the benchmarks checked and the matching method.
    3. **Separation stated.** The vendor states how the component is kept out of the training sets it supplies.
    4. **Exclusivity in writing.** For an RL environment sold for training, the exclusivity terms appear in the signed offer or contract.

    A buyer may record each result in the Notes column of Part 5, as its counsel directs, and may set any check as a threshold of its own.

Good practice
:   - Check overlap by a stated method (exact match, n-grams, or a distance with its cutoff) and report the count.
    - Keep held-out tasks in a store that the training pipeline cannot read, and say so.
    - For synthetic data, name any benchmark used as seed data or placed in a prompt.

Examples, illustrative
:   - **M** · **An overlap check attached.** A 13-gram overlap check against nine named public benchmarks: 0 matches in 50,000 items, with the method and script attached.
    - **M** · **Exclusivity signed.** For an environment sold for training, a contract clause granting exclusive use of the task set for 12 months, attached.
    - **D** · **History stated.** Distribution stated as “never sold”; no overlap check attached.

Where a check fails
:   - An overlap check that names no benchmark; check 02 finds it.
    - Exclusivity promised only in an email; check 04 finds it.
:::

### R9 · Deletion and downstream propagation

**Requirement.** The vendor states how a deletion or exclusion request received after delivery reaches the buyer, within what time, and in what form, and whether it has a mechanism to receive such requests from the individuals or rights holders concerned. For data inside an RL environment, the vendor states how a request changes the build and how the buyer learns of the new build. For sensor records, the vendor states how a participant's withdrawal reaches the buyer and within what time.

**Evidence.** The propagation procedure; the request-intake mechanism; an aggregate log of requests propagated, with the identifier of the delivery the log is bound to (the manifest hash of R1).

**Rule basis.** The buyer's own obligations under the deletion regimes that apply to it, which vary by jurisdiction and are for counsel to map; the requirement here is that the vendor's procedure exists and is stated, so that counsel can map it. Article 19 of Regulation (EU) 2016/679 (quoted in B.11) is the model for the vendor's side of the procedure: it has a controller communicate an erasure to each recipient to whom the data were disclosed, with the exception the Article states.

**Tiers.** D: the procedure stated. M: the log produced from the vendor's system; a suppression log or receipt for each delivery, time-stamped under RFC 3161 and verifiable without the vendor or any party acting for it, is such a log. A: the procedure and log attested. The time stamp on a log evidences that the log's content existed in that form before the time stated, on trust in the authority that issued it; whether the content is accurate is a separate question, which the time stamp leaves open. Whoever issued a log or receipt, it is the vendor's evidence at M, and it reaches A only when an attester that meets R4 attests it.

::: guidance
[Guidance for R9]{.gt} [Adds to no requirement · changes no tier or score]{.gl}

Purpose
:   A deletion request that reaches the vendor after delivery protects the person who made it only if it also reaches the buyer, who holds a copy. R9 asks the vendor to state that route and to give an aggregate log of the requests sent on, bound to the delivery it concerns, so that the buyer can later show how many requests reached it for that delivery. R9's M line names two forms of that log; checks 01 and 04 apply to either, and checks 02 and 03 apply only where the vendor offers the second form, time-stamped under RFC 3161 and verifiable without the vendor or any party acting for it.

What the buyer checks
:   1. **Bound to this delivery.** Every log: the identifier in the log equals the manifest hash in R1, and question 11 answers yes.
    2. **Time-stamped.** Second form: the token verifies against the authority's certificate with a published tool, and the buyer records the token's time beside the period the log covers.
    3. **Checkable without the vendor.** Second form: the check needs no account, portal or key of the vendor or of any party acting for it.
    4. **Counts reconcile.** Every log: where it covers the 12 months question 11 asks about, its count of requests sent on equals the answer to question 11; where it also counts requests received, refused and pending, those received equal the sum of the other three.

    A buyer may record each result in the Notes column of Part 5, as its counsel directs, and may set any check as a threshold of its own.

Good practice
:   - Bind each entry of the log to the manifest hash of the delivery it concerns (R1), so that one log cannot be presented for several deliveries.
    - Time-stamp the log for each delivery under RFC 3161 and keep the token with it. On trust in the authority that issued it, the token shows that the log existed in that form before the time stated; the counts are the vendor's statement of what reached the buyer.
    - Make the log checkable with published tools and the authority's certificate, with no account, portal or key held by the vendor or by any party acting for it.
    - Reconcile the counts for the period the declaration covers: requests received, requests sent on to the buyer, requests refused, each with its reason, and requests pending.

Examples, illustrative
:   - **M** · **A log from the vendor's system.** An export from the vendor's ticketing system for the quarter: 31 deletion requests, each with the date received, the date the buyer was told and the manifest hash of the delivery affected. It carries no time stamp, so checks 02 and 03 do not apply to it.
    - **M** · **A receipt for each delivery.** A receipt issued for the delivery, bound to its manifest hash and time-stamped under RFC 3161, giving the count of requests sent on for that delivery and the period covered; the buyer checks the token and the binding with published tools.
    - **D** · **A procedure with no log.** Requests reach the buyer by email within ten business days. No log is attached.
    - **assertion** · **A claim with no procedure.** “Deletion requests are honored across every downstream copy.” No procedure and no log; an assertion is recorded.

Where a check fails
:   - A log with no delivery identifier can be presented for any delivery; check 01 finds it.
    - A token that does not verify against the authority's certificate; check 02 finds it.
    - A token dated long after the period shows only that the log existed by the date of the token; check 02 records the gap.
    - A log called verifiable without the vendor, whose check runs on a page of the vendor or of a party acting for it, depends on the party being checked; check 03 finds it.
    - A log whose count of requests sent on differs from the answer to question 11 for the same 12 months, or whose requests received differ from the sum of those sent on, refused and pending; check 04 finds it.
:::

### R10 · Disclosure of relationships

**Requirement.** The vendor discloses every relationship among the parties to the transaction: ownership or control links between the vendor, any broker or marketplace, any de-identification or redaction provider, and any attester; referral fees, revenue shares or commissions among them; and prior engagements between the attester and any of them. For human data made to order, staffing firms and contributor marketplaces between the vendor and the contributors are disclosed as parties. A marketplace or hub of RL environments is a broker or marketplace under this requirement and under R4.

**Evidence.** The disclosure statement, signed by a named person.

**Rule basis.** 17 CFR 210.2-01(b) and (c)(5) (Annex B), and ISO/IEC 17021-1:2015 clauses 5.2.1 and 5.3.2, which require impartiality: a relationship that is not disclosed cannot be evaluated.

**Tiers.** One tier: the disclosure is either complete and signed, or the vendor has not met R10.

::: guidance
[Guidance for R10]{.gt} [Adds to no requirement · changes no tier or score]{.gl}

Purpose
:   R10 asks for every tie among the parties to the sale, so that the buyer can weigh each one before relying on what the parties say.

What the buyer checks
:   1. **Every party covered.** The statement covers the vendor, each broker or marketplace, each de-identification or redaction provider and each attester.
    2. **Money named.** Referral fees, revenue shares and commissions among them are named.
    3. **Intermediaries named.** For human data made to order, staffing firms and contributor marketplaces are named as parties.
    4. **Signed.** A named person signs the statement.

    A buyer may record each result in the Notes column of Part 5, as its counsel directs, and may set any check as a threshold of its own.

Good practice
:   - Write “none” for each kind of relationship that does not exist, so that a blank is never read as none.
    - Renew the statement with each declaration.

Examples, illustrative
:   - **met** · **A complete statement.** A signed statement listing the marketplace's 10 percent commission and the attester's prior engagement with the vendor in 2025.
    - **not met** · **A commission left out.** A statement that omits the marketplace's commission.

Where a check fails
:   - A blank where commissions belong; check 02 finds it.
    - An unsigned statement; check 04 finds it.
:::

### R11 · Financial and payment data

**Requirement.** Where any component contains or is derived from payment card account data, nonpublic personal information held by a financial institution, or consumer report information, the vendor states which of the three classes is present and, per class, delivers the following. For account data: a statement that no sensitive authentication data (full track data, card verification code, PINs or PIN blocks) is present in any form, including encrypted or hashed; the approach from PCI DSS 3.5.1 by which any primary account number present was rendered unreadable (one-way hash of the entire PAN, truncation, index token, or strong cryptography), and a statement that no two forms of the same PAN that could be correlated to reconstruct it are present in the delivery; and the attestation of compliance or report on compliance covering the environment the data left, whether the vendor's own or its processor's. For nonpublic personal information from a financial institution: the notice and opt-out basis under 15 U.S.C. 6802(a) and (b)(1), or the exception relied on under 6802(b)(2) or (e), and the institution's agreement that permits the disclosure and the onward use. For consumer report information: the circumstance in 15 U.S.C. 1681b(a) under which it was obtained, the user's certification, and the vendor's statement of how use in the delivery is within that circumstance. The buyer's counsel judges whether the stated basis covers the delivery; this document fixes the question and the evidence and leaves the answer to counsel. This requirement applies to data inside an RL environment as to any delivery. Where an environment or a synthetic component holds card numbers, account records or consumer report records that a person or a generator made up, the vendor says so, states how they were made (for card numbers, whether they are published test numbers or fall in ranges no issuer uses), and records the search hits they explain. The buyer judges whether a made-up value falls in a class.

**Evidence.** The documents named above. A statement that data is "PCI compliant", "tokenized" or "anonymized" that arrives without the documents R11 names for its class is scored as an assertion. A delivery described as free of card data with no search for PAN patterns on a sample is scored as an assertion.

**Rule basis.** PCI DSS v4.0.1 (PCI Security Standards Council, June 2024): Table 2 (account data), the sentence on page 5 that a cardholder data environment exists wherever PAN is stored, processed or transmitted, requirements 3.2.1, 3.3.1, 3.4.1 and 3.5.1, and by number and title requirement 4 (transmission over open, public networks) and 12.8 (third-party service provider relationships); quoted in Annex B.7. 15 U.S.C. 6802(a) and (b)(1), Annex B.8. 15 U.S.C. 1681(b) and 1681b(a), Annex B.9. PCI DSS binds the entities in the payment ecosystem through the card brands and the acquirers; where the vendor is not such an entity, this document applies its definitions and its 3.5.1 approaches as the model, as R6 applies 164.514.

**Tiers.** D: the classes present named and the documents delivered. M: the absence of sensitive authentication data and the unreadability of PAN verified on a sample by the buyer (pattern search for PAN formats with a Luhn check, for track-data and verification-code field names, and for correlatable forms of the same PAN); the 6802 and 1681b bases checked against the agreements and certifications delivered. A: the verification attested by an independent party under R4. For data inside an environment run for the buyer, M: the vendor runs the search on a sample the buyer names and gives the buyer the record, and the 6802 and 1681b bases are checked as the general line states.

::: guidance
[Guidance for R11]{.gt} [Adds to no requirement · changes no tier or score]{.gl}

Purpose
:   Payment card account data, nonpublic personal information held by a financial institution, and consumer report information each carry their own rules or standard. R11 asks which class is present and for the documents those rules call for.

What the buyer checks
:   1. **Class named.** Each class present is named, or the search that supports an answer of none is recorded.
    2. **No sensitive authentication data.** A pattern search on a sample finds no full track data, card verification codes, PINs or PIN blocks.
    3. **PAN unreadable.** Any PAN found on the sample is rendered unreadable by the approach the vendor named under 3.5.1, and no two forms of the same PAN can be correlated to reconstruct it.
    4. **Basis documented.** The 6802 basis and agreement, or the 1681b circumstance and certification, are delivered for their class.

    A buyer may record each result in the Notes column of Part 5, as its counsel directs, and may set any check as a threshold of its own.

Good practice
:   - Search for PAN with a Luhn check, and report the sample size and the hits.
    - For made-up card numbers, state whether they are published test numbers or fall in ranges no issuer uses.
    - Deliver the attestation of compliance or report on compliance for the environment the data left.

Examples, illustrative
:   - **M** · **A search the buyer ran.** Account data named; a Luhn search by the buyer over one million sampled fields found no valid PAN, no track-data or verification-code field and no correlatable forms of one PAN; the attestation of compliance delivered.
    - **N/A** · **No class present.** None of the three classes is present, and the search that supports the answer is recorded.
    - **assertion** · **A label with no documents.** “PCI compliant and tokenized.” No 3.5.1 approach and no attestation of compliance; an assertion is recorded.

Where a check fails
:   - Hashed and truncated forms of the same PAN in one delivery that could be correlated to reconstruct it; check 03 finds it.
    - An answer of no card data with no search behind it is scored as an assertion; check 01 finds it.
:::

### R12 · Hosted environments

**Requirement.** Where the buyer's agent runs on systems the buyer does not control, or its traces or other outputs are sent to such systems, the vendor names each party that receives them (the vendor, a marketplace, a host) and states for each: who holds them, for how long, each purpose they are used for other than running and scoring the buyer's runs (repair of tasks and graders, aggregate statistics, training of any model, sale or transfer), who else can access them, and how they are deleted on request. The statement also covers what the buyer sends in to run its agent: agent code, prompts, credentials and model access.

**Evidence.** The statement; the retention period; the list of parties with access; the deletion procedure; the record of what was kept and deleted.

**Rule basis.** No rule is quoted; this is the buyer's requirement for what its own agent produced. Part 1 leaves the buyer's model training practices out of scope, and this requirement asks only how the parties that receive the buyer's traces, outputs and inputs handle them.

**Tiers.** D: the statement. M: before the first run, the retention and deletion settings in force for the buyer's runs, exported from the system of each party that will hold the traces; after the first run, the record of what was kept and deleted for the buyer's own runs. No other customer's records are shown. A: the statement and the record attested by an independent party.

::: guidance
[Guidance for R12]{.gt} [Adds to no requirement · changes no tier or score]{.gl}

Purpose
:   When the buyer's agent runs on systems the buyer does not control, its traces, outputs and inputs leave the buyer's hands. R12 asks who holds them, for how long, for what use, and how they are deleted.

What the buyer checks
:   1. **Every holder named.** Each party that receives traces or outputs is named: the vendor, a marketplace, a host.
    2. **Uses listed.** Every use beyond running and scoring the buyer's runs is listed, training of any model included.
    3. **Settings exported.** Before the first run, the retention and deletion settings for the buyer's runs come from each holder's system.
    4. **Deletion recorded.** After the runs, the record shows what was kept and what was deleted, for the buyer's runs only.

    A buyer may record each result in the Notes column of Part 5, as its counsel directs, and may set any check as a threshold of its own.

Good practice
:   - Cover what the buyer sends in: agent code, prompts, credentials and model access.
    - State retention in days, for each party.
    - Show the buyer its own records only, with no other customer's records.

Examples, illustrative
:   - **M** · **Settings and a record.** Settings exported from the host's console before the first run: traces kept 30 days, no training use; after the runs, a deletion record for 412 runs.
    - **D** · **A statement.** Traces kept 90 days and used for aggregate statistics; no export attached.
    - **assertion** · **A claim with no statement.** “We never keep your data.” No parties, uses or retention stated; an assertion is recorded.

Where a check fails
:   - A marketplace that receives traces and is not named; check 01 finds it.
    - Settings described in prose with no export; check 03 finds it.
:::

## 4. The vendor questionnaire

Send to the vendor with the request for proposal or before contract. Questions 1 to 14 keep the numbers they had in the edition of 2026-11-16; questions 15 to 25 are new, and question 14 covers every answer. An answer that Annex A has no field for is given in the response to this questionnaire and counts as stated in the declaration when the person named in question 14 signs the response; where a delivery follows, the signed response is listed in its hash manifest. Each answer is attributable to a named person. "Not measured", "unknown" and "not applicable, because..." are admissible answers; an answer that asserts a result without the evidence the requirement names is recorded as an assertion.

| No. | Question | Req. | Answer format |
|---|---|---|---|
| 1 | List each component of the delivery with its source, collection method, custodians since collection, the authority under which it was collected, and, for any component collected from a third party, the agreement or terms under which it was collected. | R1 | Table per component |
| 2 | Provide the hash manifest for the delivery (algorithm named) and the time-stamp token over the manifest hash. | R1 | Files; manifest hash |
| 3 | For each component, state the right under which it may be licensed for training and the terms that travel with it. | R2 | Table per component |
| 4 | Describe the exclusion mechanism for individuals and rights holders, its service level, and the aggregate count of requests received and honored in the last 12 months. | R2 | Text; counts |
| 5 | Is any part of the delivery described as de-identified, anonymized, redacted or scrubbed? If yes: attacker assumed; method; sample (size, how drawn, by whom, when relative to the buyer's questions); date; person who ran it; residual. | R3 | Declaration fields (Annex A) |
| 6 | Does any attestation, audit or verification accompany the delivery? If yes: attester's identity; its relationships with every party; the fee arrangement and when it was fixed; prior engagements. | R4, R10 | Text; documents |
| 7 | List the elements of the evidence package delivered (manifest, token, declaration, measurement records, certification; for sensor records and RL environments, the elements R5 adds). | R5 | Checklist |
| 8 | Does any component contain or derive from health information? If yes: which 164.514(b) method; the documentation named in R6. | R6 | Documents |
| 9 | Is this a one-time delivery or a feed, refresh or renewing license? If the latter: the re-measurement interval, the per-delivery declaration practice, and the change log between deliveries. | R7 | Text; change log |
| 10 | If intended for evaluation: distribution history of each component; overlap checks performed and their method; separation procedure from training supplies. | R8 | Text; records |
| 11 | How does a deletion or exclusion request received after delivery reach the buyer, within what time, in what form? Does a mechanism exist for individuals or rights holders to submit such requests to you? Provide the aggregate count propagated in the last 12 months. Is the log bound to this delivery's manifest hash, yes or no? | R9 | Text; count; yes or no |
| 12 | Disclose every ownership, control, fee, revenue-share, commission or prior-engagement relationship among vendor, broker or marketplace, de-identification provider and attester. | R10 | Signed statement |
| 13 | Does any component contain or derive from payment card account data, nonpublic personal information held by a financial institution, or consumer report information? If yes, per class: the statements, the 3.5.1 approach, the attestation of compliance, the 6802 basis and agreement, the 1681b circumstance and certification named in R11. If no: the search performed to say so. | R11 | Documents; search record |
| 14 | Name the person accountable for these answers, their role, and the date. | all | Name; role; date |
| 15 | Does the delivery contain synthetic or model-generated data? If yes, per component: the generator (name, version or build, provider, and whether it is another party's model, your own model or a program); the generation method in outline; the seed data and its provenance; the component's share of the delivery, with the unit named. | R1 | Table per component |
| 16 | For each synthetic component: the agreement or license under which each generator was used, with any clause that limits the use of outputs to train models, or a statement that the generator is your own; the rights in the seed data; whether and how an exclusion request against the seed data changes the synthetic component. | R2 | Text; documents |
| 17 | Did the seed data hold personal data? If yes: whether generated records match seed records, under what match rule, on what sample, with what count and what residual. Was any benchmark item used as seed data or placed in a prompt, and from which benchmark? | R3, R8 | Declaration fields (Annex A) |
| 18 | Was any part of the delivery produced to order by a contracted workforce? If yes: the contributor agreement template; the counts of contributors and of signed agreements; the consent basis for any contributor's own personal data in the work; any staffing firm or contributor marketplace between you and the contributors. | R2, R10 | Template; counts; text |
| 19 | Does the delivery contain sensor records? If yes: complete the sensor-record block in Annex A, each required field declared, each measured field declared or marked "not-measured", and each conditional field declared or marked "not-present" or "not-done". | R1 | Declaration fields (Annex A) |
| 20 | For sensor records: the consent basis of operators, camera wearers and others recorded, and the withdrawal procedure; the permission for capture in private spaces; whether the records carry face-geometry scans or voiceprints and, if so, whose, by kind of person and count, and under what written notice and release; what was removed in de-identification, by what method, on what sample of frames, with what residual; any physiological signals recorded. | R2, R3, R6 | Declaration fields (Annex A) |
| 21 | Does the delivery contain an RL environment? If yes: who wrote the tasks and the graders or verifiers, by kind; where any data inside came from; the build digest; the task count, with the task list or its SHA-256; the grader version; whether it is delivered to the buyer or run for the buyer, and by whom. | R1, R5 | Declaration fields (Annex A) |
| 22 | For an RL environment: the license of the environment code, of each data component inside and of any third-party software or copied interface inside that carries its own license, and the terms that travel; whether it contains personal data and, if so, what and whose, by kind of person. | R2, R3 | Table per component |
| 23 | For an RL environment: which tasks overlap public benchmarks; how held-out tasks are kept apart; whether any task or grader file in this build, or a version of one changed only in wording, values or format, has reached any other party, and in what form; the exclusivity terms offered to this buyer, and for how long. | R8 | Text; records |
| 24 | Does the buyer's agent run on, or send traces or outputs to, systems the buyer does not control (yours, a marketplace's, a host's)? If yes, for each party that receives them: who holds them; for how long; each use other than running and scoring the buyer's runs; who else can access them; how they are deleted on request; and the same for the agent code, prompts, credentials and model access the buyer sends in. | R12 | Text; record |
| 25 | Attach the records the evidence lines and the measured tiers name: the license or consent language (R2), the exclusion log (R2), the measurement record (R3), the propagation log (R9), and, for sensor records, the record of the measured fields with its sample of episodes and the calibration files (R1). | R1, R2, R3, R9 | Files |

From The Data Licensing Standard for AI (TDLS-AI) v0.1 (Weeks, 2026), CC BY 4.0. The thresholds, and the judgment on any dataset, are the buyer's; the document contains no legal advice.

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

## 6. Statement of the author's practice

This section is the independence policy of the practice. In this section, the practice means the author and any entity under his control through which he performs the attestation work Part 0 describes. It is published so that a buyer can score that practice under Part 5 on the same terms as any other attester. Attestation here has the Annex C meaning.

**Rules.** The practice follows these rules on every attestation engagement it accepts:

1. it accepts no attestation engagement where the practice, its owners or its staff hold a financial interest in the sale, the price or the licensing of the delivery the attestation concerns;
2. it charges and accepts no fee that depends on the finding, the result, the sale or the price; every fee is fixed before the result is known;
3. it attests no work performed by a business under common ownership or control with the practice, and discloses any affiliated business;
4. it discloses, on every attestation, prior engagements with any party to the transaction;
5. it publishes the method under which each attestation is made, so that a reader can check the method against the result;
6. it states, on every attestation, the sample and how it was drawn, the date, the person who signed and the residual, recorded as found or as unknown, and, where the attestation concerns a de-identification measurement, the attacker assumed;
7. it accepts scoring under Part 5 whenever it supplies an attestation;
8. it accepts no engagement to attest anything R11 asks for account data, including the verification or search in R11's tier lines and an attestation of compliance or report on compliance; an attestation of the practice is no PCI DSS assessment.

**Scope.** The rules apply to attestation engagements the practice accepts under Requirement 4 of this document, from the date of the version in which they appear.

**Exclusions.** The practice is separate from any employer of the author. Nothing in this section describes, binds or is performed through any employer or client of the author, and nothing in it describes any dataset, vendor or buyer.

**Revision and remedy.** A departure from a rule is disclosed on the attestation it affects. A rule is changed, or this section withdrawn, only by a dated revision of this document logged in Part 7 with the reason; a revision applies to engagements accepted after its date.

**Status.** This section is policy. It creates no warranty, no assurance of any result, no legal advice, no promise to any reader, and no right in any third party.

## 7. Versioning, seal and citation

**Version.** v0.1, 2026-11-24, public draft for adoption. It supersedes the edition sealed on 2026-11-16. That edition's source has the SHA-256 `626b49613704368ae40b17d5cbbe20dfd3559961883d25cb8a1e9366dd21bf86`, and it is archived at <https://github.com/AndrewDelaurierWeeks/data-licensing-standard/commit/9ef537703d4ef6d2fe7114da85f2dd584f31ba78>. Later versions carry a change log here.

**Seal.** At publication, the SHA-256 of the published PDF and the SHA-256 of the Markdown source are time-stamped by a third-party time-stamp authority under RFC 3161, and the tokens are published beside the document, so that the document's content and date can be verified without the author. The band at the head of the body pages and the square mark on the cover are generated deterministically from the SHA-256 of the Markdown source.

**Change log.** v0.1, 2026-11-24. What changed from the edition of 2026-11-16, by kind:

1. Name and wording. The edition carries a new name. The seller is the vendor on every page. Annex C now defines the word as the party that supplies the delivery and signs the declaration; the edition of 2026-11-16 left its word undefined.
2. Scope. Part 1 names synthetic and model-generated data, human data made to order, sensor records and RL environments, and the parties that supply them.
3. Requirements extended. R1, R2, R3, R5, R6, R7, R8, R9, R10 and R11 state what they ask of those forms, and R4 says where a vendor's own checks and the documents R6 and R11 name stand. R8's distribution statement now also covers RL environments sold or licensed for training.
4. Requirement added. R12, hosted environments. It is scored on the D, M, A scale and is not applicable where the delivery contains no RL environment, or where the buyer's agent runs only on systems the buyer controls and no trace or output leaves them.
5. Evidence named, tier unchanged. R9's M line names a suppression log or receipt for each delivery as one form of the log it already asked for; any log produced from the vendor's system still meets M. R9's evidence line asks for the identifier of the delivery the log is bound to, question 11 asks whether the log is bound, and the answer changes no score. R9 also says what a time stamp on a log evidences and how a log reaches A, and R1's evidence line says the same of the token over the manifest.
6. Corrections. R4 covers an attestation offered in support of any requirement (it named R1 to R3), and its evidence line uses the requirement's own test, a fee fixed before the result was known. The M tiers of R6 and R11 are verified by the buyer (the words "or a reviewer" are removed). R11's D tier no longer scores an answer of "none", which Part 5 records as not applicable. R5's evidence line names what the manifest covers. R2's rule basis says that no rule is quoted for the requirement as a whole. Tier A's definition names a redaction provider, as R4 did. Part 1 says what the requirements leave out. Part 0 says the rules are quoted as they stood at the source named in Annex B, which for some is a republication (it said "in the original"), names the robot-learning and perception teams among its readers, says who usually decides a purchase (it said who signs), and says that no body named in the document developed, reviewed, approved or endorsed it.
7. The record. Part 2 and Annex B gain three mechanisms, two from Regulation (EU) 2016/679 and one from an opinion of the European Data Protection Board (B.11), the Illinois biometric-privacy statute (B.12) and California Civil Code section 3111 (B.10). The rule bases of R1, R2, R3 and R9 cite them. Part 2's opening sentence names the kinds of source without a count, and its "Why now" paragraph dates its statement on the appeals. Annex B's opening names the republications, and B.6 dates its statement on the appeals.
8. Questionnaire. Questions 1 to 14 keep their numbers; question 7 drops "notice material" and names what R5 adds; question 11 gains its last part; questions 15 to 25 are new. The opening paragraph says where an answer with no Annex A field is given, when it counts as stated in the declaration, and that the signed response is listed in the hash manifest of a delivery that follows.
9. Scoring. The scale is unchanged. The cap on assertions now ends "a declared answer" (it ended "a declaration"), with no change of meaning. The list of requirements that can be not applicable changed for R3, R6, R7 and R8 and gained R12. Sentences are added on a requirement with two tier paragraphs, on a tier sentence that names a form, and on the last part of question 11. In the suggested thresholds, R3 is asked at M where a de-identification claim is made and at D where it applies without one; the other thresholds are unchanged in wording. R12 adds one row, the sheet's header and total line name every score a row can take, and "every applicable requirement" includes R12 where it applies. The cover and Part 0 said the sheet is kept with the contract file, and Part 5 and the back page said with the contract; each now says where the buyer's counsel directs, and Part 5 says what the sheet records.
10. Part 6. The rules follow Requirement 4, which now covers an attestation offered in support of any requirement; the reason is that R5 to R9 and R11 carried attested tiers that R4 did not name. Rule 1 reads "the delivery the attestation concerns" (it read "the data attested"), so that it reaches an RL environment. Rule 6 asks for the attacker assumed only where the attestation concerns a de-identification measurement, the one kind of attestation that assumes an attacker. Rule 8 is new: the practice accepts no engagement to attest anything R11 asks for account data, and an attestation of the practice is no PCI DSS assessment. Rules 2 to 5 and 7 are unchanged in wording. The changes apply to engagements accepted after 2026-11-24.
11. Schema. 0.3.0 replaces 0.2.0 under a new `$id`: two values that named the seller say vendor, a tier value for "not applicable" is added, the length of the manifest hash follows the algorithm named, one compliance-evidence value that R11 never named is removed, blocks are added for the new forms, four optional fields are added (an expiry, a receipt identifier, a certificate identifier, and whether the propagation log is bound to the manifest), the time-stamp token hash is required where the package lists a token and refused where it lists none, the attested tier in `de_identification`, the one tier the schema records, requires an attestation offered under a fee fixed before the result and independent of the finding, the sale and the price, and the rule that set the R3 tier where nothing is described as de-identified is removed. A declaration written for schema 0.2.0 still validates against schema 0.2.0; it fails schema 0.3.0, which requires the four new blocks.
12. Annex A gains the sensor-record block, a crosswalk from four outside specifications, one of them a committee specification draft, and a conversion in the validator from that draft's record form; a fifth, an initial public draft, is named and not mapped.
13. Annex C gains entries for the new forms and for delivery, seed data and vendor; its entry for the hash manifest is extended, and its entry for the evidence package drops "notice material", as question 7 does, and names what R5 adds.
14. License. The exclusion from the Creative Commons grant reaches quoted material wherever it appears and the field names and section headings of the outside specifications; the crosswalk file is under the MIT License with the schema, the example and the validator. The cover engraving is described as created by the author, of a carved neoclassical anthropomorphic mascaron sculpted in high relief.
15. Disclosure. Part 0's conflict disclosure gains two sentences on evidence that other businesses of the author may supply, among them logs and receipts of the form R9's M line names.
16. Guidance. Each requirement ends with guidance: its purpose, what the buyer checks, good practice, illustrative examples and where a check fails. Part 0's conflict disclosure applies to it. Guidance adds to no requirement, changes no tier and changes no score.

The edition of 2026-11-16: first publication.

**Citation.** Weeks, A. D. (2026). The Data Licensing Standard for AI (TDLS-AI) v0.1. Sealed on the date in the published time-stamp token. A requirement is cited by short name, version and number, as in TDLS-AI v0.1 R8; a question, as in TDLS-AI v0.1 R8, question 10. The schema (Annex A) is cited by its `$id` and version.

**License.** Text under Creative Commons Attribution 4.0 International, excluding material quoted from the sources named in Annex B, wherever it appears, and the field names and section headings of the outside specifications in Annex A, in which this license grants nothing and any rights stay with their holders; the schema, example, validator and crosswalk file under the MIT License, which covers the author's own work in those files and no name, heading or text of an outside specification; the cover engraving, created by the author, of a carved neoclassical anthropomorphic mascaron sculpted in high relief, under the same CC BY 4.0 license as the text. A buyer may reproduce Parts 4 and 5 in its own procurement documents with attribution.

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

## Annex B · The rules, quoted

Each quotation is taken from the source named on the date shown. Where a rule is longer than the quoted part, the omission is marked. Quoted text is reproduced as it appeared at the source on the date opened, including the source's punctuation. The eCFR describes itself as authoritative but not an official legal edition; the Legal Information Institute republishes the Federal Rules of Evidence and the United States Code; california.public.law republishes the California codes; B.11 and B.12 were opened at the publishers' own sites.

### B.1 Federal Rule of Evidence 902 (Legal Information Institute, Cornell Law School; opened 2026-11-05)

Opening: "The following items of evidence are self-authenticating; they require no extrinsic evidence of authenticity in order to be admitted:"

902(11), notice requirement (part): "Before the trial or hearing, the proponent must give an adverse party reasonable written notice of the intent to offer the record — and must make the record and certification available for inspection — so that the party has a fair opportunity to challenge them."

902(13): "Certified Records Generated by an Electronic Process or System. A record generated by an electronic process or system that produces an accurate result, as shown by a certification of a qualified person that complies with the certification requirements of Rule 902(11) or (12). The proponent must also meet the notice requirements of Rule 902(11)."

902(14): "Certified Data Copied from an Electronic Device, Storage Medium, or File. Data copied from an electronic device, storage medium, or file, if authenticated by a process of digital identification, as shown by a certification of a qualified person that complies with the certification requirements of Rule (902(11) or (12) [sic]. The proponent also must meet the notice requirements of Rule 902 (11)."

### B.2 45 CFR 164.514 (eCFR, current to 2026-10-23; opened 2026-11-05)

164.514(a): "Health information that does not identify an individual and with respect to which there is no reasonable basis to believe that the information can be used to identify an individual is not individually identifiable health information."

164.514(b), introduction and (b)(1): "A covered entity may determine that health information is not individually identifiable health information only if: (1) A person with appropriate knowledge of and experience with generally accepted statistical and scientific principles and methods for rendering information not individually identifiable: (i) Applying such principles and methods, determines that the risk is very small that the information could be used, alone or in combination with other reasonably available information, by an anticipated recipient to identify an individual who is a subject of the information; and (ii) Documents the methods and results of the analysis that justify such determination; or"

164.514(b)(2)(i), introduction: "The following identifiers of the individual or of relatives, employers, or household members of the individual, are removed:" (the list of identifiers follows in the rule)

164.514(b)(2)(ii): "The covered entity does not have actual knowledge that the information could be used alone or in combination with other information to identify an individual who is a subject of the information."

### B.3 17 CFR 210.2-01 (eCFR, current to 2026-10-23; opened 2026-11-05)

210.2-01(b): "The Commission will not recognize an accountant as independent, with respect to an audit client, if the accountant is not, or a reasonable investor with knowledge of all relevant facts and circumstances would conclude that the accountant is not, capable of exercising objective and impartial judgment on all issues encompassed within the accountant's engagement."

210.2-01(c)(5), Contingent fees: "An accountant is not independent if, at any point during the audit and professional engagement period, the accountant provides any service or product to an audit client for a contingent fee or a commission, or receives a contingent fee or commission from an audit client."

210.2-01(f)(10): "Contingent fee means, except as stated in the next sentence, any fee established for the sale of a product or the performance of any service pursuant to an arrangement in which no fee will be charged unless a specified finding or result is attained, or in which the amount of the fee is otherwise dependent upon the finding or result of such product or service. Solely for the purposes of this section, a fee is not a “contingent fee” if it is fixed by courts or other public authorities, or, in tax matters, if determined based on the results of judicial proceedings or the findings of governmental agencies. Fees may vary depending, for example, on the complexity of services rendered."

### B.4 ISO/IEC 17021-1:2015

Conformity assessment. Requirements for bodies providing audit and certification of management systems. Part 1: Requirements. Clauses 5.2.1 and 5.3.2 require impartiality of a certification body. The standard's text is copyrighted by ISO and is not reproduced; the clauses are cited for counsel to read in the licensed copy.

### B.5 RFC 3161 and RFC 9162 (RFC Editor; opened 2026-11-05)

RFC 3161, Internet X.509 Public Key Infrastructure Time-Stamp Protocol (TSP), C. Adams, P. Cain, D. Pinkas, R. Zuccherato, August 2001, Proposed Standard, updated by RFC 5816. The document "describes the format of a request sent to a Time Stamping Authority (TSA) and of the response that is returned" and "establishes several security-relevant requirements for TSA operation".

RFC 6962, Certificate Transparency, is the version deployed on the public web. RFC 9162, Certificate Transparency Version 2.0, B. Laurie, E. Messeri, R. Stradling, December 2021, Experimental; obsoletes RFC 6962. It "describes version 2.0 of the Certificate Transparency (CT) protocol for publicly logging the existence of Transport Layer Security (TLS) server certificates as they are issued or observed, in a manner that allows anyone to audit certification authority (CA) activity". Logs are "network services that implement the protocol operations for submissions and queries".

### B.6 Bartz v. Anthropic PBC (N.D. Cal. No. 3:24-cv-05417; docket opened 2026-11-05)

Bartz v. Anthropic PBC, N.D. Cal. No. 3:24-cv-05417-AMO. Order Granting Final Approval of Class Action Settlement, Dkt. 680, filed July 20, 2026 (Martinez-Olguin, J.); the class comprises owners of the exclusive right to reproduce books in the versions of two shadow libraries downloaded by the defendant, as listed on the Works List: "The non-reversionary Settlement Fund of $1.5 billion provides meaningful relief to the Settlement Class" (part; the sentence continues); "The estimated per-work payment of approximately $3,000 is four times the minimum statutory damages amount for willful infringement"; as of April 16, 2026, "91.3 percent of the Works List had been claimed, for a total of 440,490 works of the 482,460 Works on the Works List." Notices of appeal to the Ninth Circuit include Dkt. 682 and 683 (August 2026; Ninth Circuit Nos. 26-5391 and 26-5455); the appeals were pending when the docket was opened.

### B.7 PCI DSS v4.0.1 (PCI Security Standards Council, June 2024; the standard as published, opened 2026-11-05)

Page 4, Table 2, Account Data: "Cardholder Data includes: Primary Account Number (PAN); Cardholder Name; Expiration Date; Service Code". "Sensitive Authentication Data includes: Full track data (magnetic-stripe data or equivalent on a chip); Card verification code; PINs/PIN blocks".

Page 5: "If an entity stores, processes, or transmits PAN, then a CDE exists to which PCI DSS requirements will apply."

Requirement 3.2.1, opening: "Account data storage is kept to a minimum through implementation of data retention and disposal policies, procedures, and processes".

Requirement 3.3.1: "SAD is not stored after authorization, even if encrypted. All sensitive authentication data received is rendered unrecoverable upon completion of the authorization process."

Requirement 3.4.1, opening: "PAN is masked when displayed (the BIN and last four digits are the maximum number of digits to be displayed), such that only personnel with a legitimate business need can see more than the BIN and last four digits of the PAN."

Requirement 3.5.1: "PAN is rendered unreadable anywhere it is stored by using any of the following approaches:" "One-way hashes based on strong cryptography of the entire PAN." "Truncation (hashing cannot be used to replace the truncated segment of PAN)." "If hashed and truncated versions of the same PAN, or different truncation formats of the same PAN, are present in an environment, additional controls are in place such that the different versions cannot be correlated to reconstruct the original PAN." "Index tokens." "Strong cryptography with associated key-management processes and procedures."

Requirement 4, titled "Protect Cardholder Data with Strong Cryptography During Transmission Over Open, Public Networks", and requirement 12.8, "Risk to information assets associated with third-party service provider (TPSP) relationships is managed.", are cited by number and title; their sub-requirements are not reproduced here.

### B.8 15 U.S.C. 6802 (Legal Information Institute, Cornell Law School; opened 2026-11-05)

6802(a): "Except as otherwise provided in this subchapter, a financial institution may not, directly or through any affiliate, disclose to a nonaffiliated third party any nonpublic personal information, unless such financial institution provides or has provided to the consumer a notice that complies with section 6803 of this title."

6802(b)(1): "A financial institution may not disclose nonpublic personal information to a nonaffiliated third party unless— (A) such financial institution clearly and conspicuously discloses to the consumer, in writing or in electronic form or other form permitted by the regulations prescribed under section 6804 of this title, that such information may be disclosed to such third party; (B) the consumer is given the opportunity, before the time that such information is initially disclosed, to direct that such information not be disclosed to such third party; and (C) the consumer is given an explanation of how the consumer can exercise that nondisclosure option."

6802(b)(2) (the service-provider exception) and 6802(e) (the general exceptions, including disclosure "with the consent or at the direction of the consumer") are cited by subsection; their text is not reproduced here.

### B.9 15 U.S.C. 1681 and 1681b (Legal Information Institute, Cornell Law School; opened 2026-11-05)

1681(b): "It is the purpose of this subchapter to require that consumer reporting agencies adopt reasonable procedures for meeting the needs of commerce for consumer credit, personnel, insurance, and other information in a manner which is fair and equitable to the consumer, with regard to the confidentiality, accuracy, relevancy, and proper utilization of such information in accordance with the requirements of this subchapter."

1681b(a), opening: "Subject to subsection (c), any consumer reporting agency may furnish a consumer report under the following circumstances and no other:"

1681b(a)(3), lead-in and (A): "To a person which it has reason to believe— (A) intends to use the information in connection with a credit transaction involving the consumer on whom the information is to be furnished and involving the extension of credit to, or review or collection of an account of, the consumer; or"

1681b(a)(3)(F): "otherwise has a legitimate business need for the information— (i) in connection with a business transaction that is initiated by the consumer; or (ii) to review an account to determine whether the consumer continues to meet the terms of the account."

### B.10 California Civil Code 3111 (california.public.law, a republication; opened 2026-11-24)

3111, opening (part): "the developer of the system or service shall post on the developer’s internet website documentation regarding the data used by the developer to train the generative artificial intelligence system or service, including, but not limited to, all of the following:"

3111(a)(12): "Whether the generative artificial intelligence system or service used or continuously uses synthetic data generation in its development. A developer may include a description of the functional need or desired purpose of the synthetic data in relation to the intended purpose of the system or service."

### B.11 Regulation (EU) 2016/679 and Opinion 28/2024 (EUR-Lex; European Data Protection Board; opened 2026-11-24)

Recital 26 (part): "To determine whether a natural person is identifiable, account should be taken of all the means reasonably likely to be used, such as singling out, either by the controller or by another person to identify the natural person directly or indirectly."

Article 19: "The controller shall communicate any rectification or erasure of personal data or restriction of processing carried out in accordance with Article 16, Article 17(1) and Article 18 to each recipient to whom the personal data have been disclosed, unless this proves impossible or involves disproportionate effort. The controller shall inform the data subject about those recipients if the data subject requests it."

Articles 2 (material scope) and 3 (territorial scope) are cited by number; their text is not reproduced here.

European Data Protection Board, Opinion 28/2024 on certain data protection aspects related to the processing of personal data in the context of AI models, adopted on 17 December 2024. Paragraph 129 (part): "SAs should take into account whether the controller deploying the model conducted an appropriate assessment, as part of its accountability obligations to demonstrate compliance with Article 5(1)(a) and Article 6 GDPR, to ascertain that the AI model was not developed by unlawfully processing personal data." (the footnote mark is omitted) Paragraph 58(c) (part): "This should include the specific measures for each source of training datasets, including relevant source URLs and descriptions of measures taken (or already taken by third-party dataset providers);"

### B.12 740 ILCS 14, Biometric Information Privacy Act (Illinois General Assembly, ilga.gov; opened 2026-11-24)

14/10, "Biometric identifier" (part): "a retina or iris scan, fingerprint, voiceprint, or scan of hand or face geometry." "Biometric identifiers do not include writing samples, written signatures, photographs, human biological samples used for valid scientific testing or screening, demographic data, tattoo descriptions, or physical descriptions such as height, weight, hair color, or eye color."

14/10, "Biometric information" (part): "any information, regardless of how it is captured, converted, stored, or shared, based on an individual's biometric identifier used to identify an individual."

14/15(b), lead-in: "No private entity may collect, capture, purchase, receive through trade, or otherwise obtain a person's or a customer's biometric identifier or biometric information, unless it first:" (three conditions follow in the statute: written notice of the collection or storage, written notice of its purpose and length of term, and a written release)

## Annex C · Glossary

**Assertion.** A claim of a result without the evidence the requirement names. Scored at zero.

**Attacker assumed.** The outside information and access a de-identification measurement takes the adversary to have, on the T0 to T5 scale in Annex A.

**Attestation.** A signed statement by a named person at an independent party that a measurement was made as described and produced the stated result. The word is used in this sense throughout. It does not refer to an attest engagement under any accountancy statute or AICPA standard; a PCI DSS attestation of compliance is named as such where it is meant.

**Declaration.** The vendor's own signed statement of the answers to Part 4, in the Annex A format.

**Delivery.** What the vendor supplies under one declaration: the files delivered, or, for an environment run for the buyer, the build the buyer's agent runs against, named by its build digest. For such an environment the hash manifest lists the build digest and the files the buyer receives.

**Evidence package.** The manifest, token, declaration, measurement records and the qualified person's certification that accompany a delivery, with what R5 adds for sensor records and for an RL environment (R5).

**Hash manifest.** A list of every delivered file with its cryptographic hash, and the hash of the list itself. For an RL environment delivered as a container, the manifest lists the image digest in place of the files inside the image (R1).

**Human data made to order.** Demonstrations, preference labels, annotations and written reasoning produced by a contracted workforce for a buyer's or a vendor's order.

**Independent.** Meeting the standard in R4: independent of the vendor, of any de-identification or redaction provider in the transaction, and of any broker or marketplace that sells or lists the data, under a fee fixed before the result is known.

**Measurement.** A method applied to a stated sample on a stated date by a named person, with a stated residual.

**Residual.** What a measurement found left over: records, fields or cases the method does not cover or did not clear.

**RL environment.** Software in which an AI agent acts and is scored, bought for reinforcement learning (RL) or for evaluation: the system the agent works in (simulated, sandboxed or live), a task set, the graders, verifiers or reward functions that score each attempt (code, a model or a person), and the data inside. It reaches the buyer as software delivered to the buyer, as a service that the vendor or another party runs, or as both, and is bought directly or through a marketplace.

**Seed data.** The records a generator was fitted to, conditioned on or prompted with to produce a synthetic component, including examples placed in a prompt. The data on which another party trained a generator before the vendor used it is outside the term. Records placed inside an RL environment are called the data inside.

**Sensor records.** Time-series records from sensors on a robot, a person or a fixed rig, with the actions or commands sent and the audio and location recorded with them.

**Synthetic data.** Records whose content a generative model or a generating program produced, including records produced from seed data. Model-generated data has the same meaning. A real record that a model only transcribed, translated, labeled or reformatted is outside the term; the vendor names that model under R1 as part of the collection method.

**Tier.** The level at which a requirement is met: none, declared, measured, independently attested; or not applicable.

**Time-stamp token.** A third-party authority's statement under RFC 3161 that a given hash existed before the time stated, on trust in that authority.

**Vendor.** The party that supplies the delivery to the buyer and signs the declaration, whatever its kind in Part 1: an owner, a collector, a de-identification or redaction provider delivering a processed corpus, a generator, a builder, a host, or a broker or marketplace selling in its own name. Where the delivery passed through more than one seller, R4 and R10 read each of them as a party to the transaction. The cover's scope line names brokers and marketplaces beside vendors because R4 and R10 treat a broker or marketplace that stands between the vendor and the buyer as a separate party to the transaction; a broker or marketplace is the vendor only where it is the party that signs.
