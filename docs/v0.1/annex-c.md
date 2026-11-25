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
