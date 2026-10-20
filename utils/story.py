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

# Page owner names: replace "Member A/B/C" with real names.
TEAM = {
    "home": "Yajat",
    "global": "Yajat",
    "where": "Member A",
    "compute": "Member B",
    "water": "Member C",
    "sources": "Yajat",
}

# Owners update their own line when their page moves on.
STATUS = {
    "global": "Draft ready",
    "where": "In progress",
    "compute": "In progress",
    "water": "In progress",
}
