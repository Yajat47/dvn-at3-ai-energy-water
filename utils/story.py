"""Shared story settings. Change the question, persona or team here and every page updates."""

QUESTION = "Is AI's energy and water footprint a global problem, or a local one?"

WHY_ARGUABLE = (
    "Measured against the world, data centres use a small slice of electricity. Measured against "
    "the grids and catchments they sit in, the slice can be large. The same data supports both answers."
)

PERSONA = {
    "name": "Daniel",
    "role": "Infrastructure planner, Western Sydney council",
    "note": "Fictional persona",
    "decision": (
        "Daniel is assessing data-centre development applications. He has to advise councillors on "
        "whether these sites are a real risk to local electricity and water supply, or a headline that "
        "looks bigger than it is."
    ),
    "needs": [
        "How big is AI's footprint, and how fast is it growing?",
        "Where does that load actually land?",
        "Will efficiency gains cancel out the growth?",
        "What does it mean for water, not just power?",
    ],
}

# Page owners, by first name. Must match the "Who" column in docs/AI_PROVENANCE.md.
TEAM = {
    "home": "Yajat",
    "global": "Yajat",
    "where": "Siddharth",
    "compute": "Niki",
    "water": "Akil",
    "sources": "Yajat",
}

# Owners update their own line when their page moves on.
STATUS = {
    "global": "Draft ready",
    "where": "In progress",
    "compute": "In progress",
    "water": "In progress",
}

# The three user stories (README lists the same three). Each must be walkable in the app.
USER_STORIES = [
    {
        "as_a": "infrastructure planner at a Western Sydney council",
        "i_want": "to see how much electricity data centres use worldwide and how fast that is growing",
        "so_that": "I can judge whether AI's footprint is a world-scale problem or a small share of global demand",
        "pages": ["views/global_scale.py"],
    },
    {
        "as_a": "infrastructure planner at a Western Sydney council",
        "i_want": "to compare the data-centre share of electricity and water in the places they cluster with the global share",
        "so_that": "I can judge how heavily a cluster like Western Sydney could load the local grid and catchment",
        "pages": ["views/where_it_lands.py", "views/water.py"],
    },
    {
        "as_a": "infrastructure planner at a Western Sydney council",
        "i_want": "to see whether efficiency gains are keeping pace with the growth in AI compute",
        "so_that": "I know whether to plan for data-centre demand that keeps rising or one that levels off",
        "pages": ["views/compute_vs_efficiency.py", "views/global_scale.py"],
    },
]

# What the data in this app cannot show. Page owners add their own limits here.
LIMITS = [
    "Most data-centre electricity figures here are IEA model estimates, not meter readings.",
    "The IEA publishes no data-centre estimates for 2021 or 2022, so trends between 2020 and 2023 are a straight join, not data.",
    "The 2030 figure is one IEA base-case projection, not a forecast range; other scenarios and other estimators give different numbers.",
    "Our files do not separate AI workloads from other data-centre work such as streaming and cloud storage.",
    "National totals hide the substation and catchment level where a council's decision actually sits.",
]
