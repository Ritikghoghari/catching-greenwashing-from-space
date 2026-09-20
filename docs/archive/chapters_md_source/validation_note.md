# External Validation of Mismatch Scores

This note cross-checks the mismatch scores produced by the thesis's four-component
formula (forest_loss_score, specificity_score, sentiment_score, spatial_match_score;
weights 0.35 / 0.35 / 0.15 / 0.15, from `Results/master_scores.csv`) against evidence
published independently of this thesis: RSPO Complaints Panel records, Forest Peoples
Programme (FPP) press releases, Mongabay investigative reporting, and Chain Reaction
Research. Four companies were checked, spanning the top and bottom of the ranking:
Golden Agri-Resources (GAR, rank 2, score 63.1), IOI Corporation (rank 4, score 56.1),
SD Guthrie / Sime Darby Plantation (rank 5, score 55.2, chosen as the mid-ranking case),
and Astra Agro Lestari (rank 11, score 17.6, the lowest-scoring company). The goal is not
to reproduce the thesis's numeric score from these sources, which is not possible since
none of them publish a comparable mismatch metric, but to check whether the direction and
relative severity implied by each company's rank is consistent with what independent
observers have reported about that company's deforestation and grievance record.

## Golden Agri-Resources (GAR)

GAR's high mismatch score is directionally consistent with its external record. The RSPO
Complaints Panel has an active case (PT Kartika Prima Cipta vs. Forest Peoples Programme
and TuK Indonesia) in which FPP alleges GAR operates unlawfully inside Indonesia's
protected Forest Zone, with more than 75,000 hectares, over 15 percent of GAR's total
plantation area, identified as being under unlawful oil palm production (Forest Peoples
Programme, complaint accepted by RSPO in 2020, with bilateral engagement extended into
2024 per RSPO Complaints Panel minutes, October 2024). Separately, in March 2023 GAR
withdrew from the High Carbon Stock Approach (HCSA), the industry's shared no-deforestation
methodology, a move environmental groups characterized as weakening its zero-deforestation
commitments (Friends of the Earth, "Major palm oil company withdraws from anti-deforestation
initiative," 2023; FoodNavigator, March 13, 2023). A company with a large, still-unresolved
land-use complaint and a public exit from a shared no-deforestation standard, while
continuing to make zero-deforestation claims, matches the thesis's characterization of GAR
as a high-mismatch case (score 63.1, rank 2, and the second-highest raw forest loss score
of 50.2). This is one of the strongest external corroborations found in this check.

## IOI Corporation

IOI's rank 4 position (score 56.1, and notably the highest forest_loss_score component in
the dataset at 100.0) is broadly consistent with its documented record, though the clearest
independent evidence is older than the thesis's post-2020 loss window. In March 2016, RSPO
suspended IOI's certification after finding that IOI subsidiaries in Ketapang, West
Kalimantan had cleared rainforest, including operations on carbon-rich deep peat and land
clearing associated with fire use, without required permits (Mongabay, "Malaysian palm oil
giant IOI sues RSPO over suspension," May 2016). The suspension triggered contract
cancellations from Unilever, Kellogg's, and Nestle, and IOI subsequently sued RSPO before
withdrawing the suit in June 2016 and committing to NDPE (No Deforestation, No Peat, No
Exploitation) policies (Mongabay, 2016; Chain Reaction Research, "IOI Corporation: Customers
and Investors Want Sustainability"). This establishes IOI as a company with a substantiated,
RSPO-adjudicated history of forest clearing and a subsequent public commitment to stop, which
is exactly the pattern the thesis's mismatch score is designed to flag. The evidence located
in this check, however, centers on 2016, and no equivalent post-2020 RSPO ruling or NGO report
specific to IOI was found during this search, so the historical record supports the direction
of IOI's score without independently confirming the magnitude of IOI's post-2020 loss figure
in the master CSV (74,385 ha, 19.04 percent of forest, the highest loss percentage in the
dataset).

## SD Guthrie (Sime Darby Plantation)

SD Guthrie sits at rank 5 (score 55.2) with the highest raw sentiment_mean and specificity
figures pulled down by a mid-range forest_loss_score, and the external record for this
company is more mixed than for GAR or IOI. SD Guthrie is the company behind Crosscheck, a
public supply-chain traceability tool, and has co-financed Global Forest Watch's RADD
deforestation alerts, positioning it as comparatively transparent among the large Malaysian
groups (SPOTT.org profile; Sime Darby Plantation press materials). Against that, Mongabay
reported in November 2025 that Indigenous groups in Sarawak secured a pause in forest
clearing tied to SD Guthrie's supply chain after a campaign targeting a Glenealy/Samling
mill purchase (Mongabay, "Cautious win for Indigenous groups in Malaysia as palm oil firm
pauses forest clearing," November 2025), indicating that supplier-linked clearing remains an
active, current issue rather than a purely historical one. No RSPO Complaints Panel ruling
specific to SD Guthrie/Sime Darby was located comparable in scale to the GAR or IOI cases.
This mixed picture, meaningful transparency infrastructure alongside an ongoing,
unresolved supplier grievance, is directionally consistent with a mid-table rather than
top- or bottom-ranked mismatch score, though it does not strongly confirm the specific
rank-5 position versus, say, rank 3 or 6.

## Astra Agro Lestari

Astra Agro Lestari's position as the lowest-scoring company (rank 11, score 17.6) is the
one result in this check that sits in clear tension with the independent record. Mongabay
reported in July 2024 that a Genesis Bengkulu geospatial investigation found roughly 17,664
hectares of Astra Agro subsidiary concessions overlapping forest zones, including about
1,100 hectares inside protected or conservation forest where plantations are prohibited
under Indonesian law, and that three subsidiaries (PT Agro Nusa Abadi, PT Sawit Jaya Abadi,
PT Rimbunan Alam Sentosa) lacked the land-use permits required to operate legally (Mongabay,
"Allegations widen against Indonesian palm oil giant Astra Agro Lestari," July 9, 2024). The
same reporting documents a long-running land dispute affecting more than 6,700 hectares
without free, prior and informed consent from local communities, and alleged intimidation of
community members who had demanded land restitution as recently as December 2023. Civil
society groups (Friends of the Earth and allied Indonesian NGOs) publicly opposed Astra
Agro's 2024 application for RSPO membership on the grounds that it would amount to
greenwashing given this record. This is a substantiated, current, and fairly severe
grievance profile, which does not obviously match a mismatch score near the bottom of an
11-company ranking. The thesis's master CSV does show meaningful post-2020 loss for Astra
Agro (87,199 ha, the third-highest absolute loss figure in the dataset) but the company's
low mismatch score is driven by its low specificity_score (13.8, second-lowest) and a
sentiment_score of 0.0 (the lowest in the dataset), meaning the formula is picking up on
vague, low-conviction public claims rather than on the strength of any pledge that the loss
then contradicts. In other words, Astra Agro's low score in this formula plausibly reflects
that the company makes few specific, strongly-worded zero-deforestation claims to
contradict, not that its environmental record is clean. This is worth flagging explicitly in
the thesis: a company that avoids concrete public commitments can register a low mismatch
score under this formula even when independent, contemporaneous evidence documents
significant illegal clearing and unresolved community harm. This is a structural limitation
of a claims-contradiction framing, not an error in the arithmetic, but it should be stated
plainly rather than left implicit.

## Overall external consistency

Of the four companies checked, two (GAR and IOI) show good directional agreement between
the thesis's mismatch score and independently published RSPO, FPP, and Mongabay/Chain
Reaction Research evidence: both carry substantiated, large-scale forest clearing findings
and both currently make or have made public no-deforestation commitments that a
claims-contradiction score is designed to catch. One (SD Guthrie) shows a plausible but not
strongly confirming mid-table match, reflecting a genuinely mixed record of both
transparency investment and an unresolved 2025 supplier grievance. One (Astra Agro) shows a
clear mismatch between the low score this formula assigns and the seriousness of the
independent record, and the likely mechanism, low measured specificity of the company's
public claims rather than a clean environmental record, is identified above and should be
carried into the thesis's limitations section rather than treated as a validated result.
No fabricated statistics or invented sources are used in this note; where independent
corroboration could not be found for a specific claim (for example, a post-2020,
company-specific RSPO ruling against IOI), that gap is stated directly above rather than
filled in.

## Sources

- Forest Peoples Programme, complaint accepted by RSPO against Golden Agri-Resources /
  PT Kartika Prima Cipta, ongoing as of RSPO Complaints Panel minutes, October 2024:
  https://rspo.org/wp-content/uploads/Minutes-of-the-Complaints-Panel-meeting-No.102024.pdf
- Friends of the Earth, "Major palm oil company withdraws from anti-deforestation
  initiative," 2023: https://foe.org/news/gar-withdrawal-statement/
- FoodNavigator, "Why Golden Agri-Resources quit no deforestation initiative HCSA,"
  March 13, 2023: https://www.foodnavigator.com/Article/2023/03/13/Why-Golden-Agri-Resources-quit-no-deforestation-initiative-HCSA/
- Mongabay, "Malaysian palm oil giant IOI sues RSPO over suspension," May 2016:
  https://news.mongabay.com/2016/05/malaysian-palm-oil-giant-ioi-sues-rspo-suspension/
- Chain Reaction Research, "IOI Corporation: Customers and Investors Want Sustainability":
  https://chainreactionresearch.com/report/ioi-corporation-customers-and-investors-want-sustainability/
- SPOTT.org, "SD Guthrie Bhd (previously assessed as Sime Darby Plantation Sdn Bhd)":
  https://www.spott.org/palm-oil/sd-guthrie-bhd-previously-assessed-as-sime-darby-plantation-sdn-bhd/date/november-2021/
- Mongabay, "Cautious win for Indigenous groups in Malaysia as palm oil firm pauses forest
  clearing," November 2025: https://news.mongabay.com/2025/11/cautious-win-for-indigenous-groups-in-malaysia-as-palm-oil-firm-pauses-forest-clearing/
- Mongabay, "Allegations widen against Indonesian palm oil giant Astra Agro Lestari,"
  July 9, 2024: https://news.mongabay.com/2024/07/allegations-widen-against-indonesian-palm-oil-giant-astra-agro-lestari/
- Friends of the Earth, "Civil society groups demand sustainable palm oil body reject
  Indonesian palm oil giant Astra Agro Lestari's membership":
  https://foe.org/news/sustainable-palm-oil-astra-agro/
