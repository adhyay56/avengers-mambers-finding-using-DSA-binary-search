import math

import streamlit as st

st.set_page_config(page_title="Avengers Finder", page_icon="🛡️", layout="centered")

# ---------------------------------------------------------------- data
AVENGERS = [
    # Original / core Avengers
    "iron man", "tony stark",
    "captain america", "steve rogers",
    "thor", "thor odinson",
    "hulk", "bruce banner",
    "black widow", "natasha romanoff",
    "hawkeye", "clint barton",
    # Early comics members
    "ant-man", "hank pym", "scott lang",
    "wasp", "janet van dyne", "hope van dyne",
    "giant-man", "yellowjacket", "goliath",
    "quicksilver", "pietro maximoff",
    "scarlet witch", "wanda", "wanda maximoff",
    "vision",
    "wonder man", "hercules", "beast",
    "black knight", "mockingbird", "tigra",
    "moondragon", "photon", "monica rambeau",
    "sersi", "sentry", "us agent",
    # Modern / MCU members
    "black panther", "t'challa",
    "falcon", "sam wilson",
    "winter soldier", "bucky barnes",
    "war machine", "rhodey", "james rhodes",
    "doctor strange", "stephen strange",
    "spider-man", "peter parker", "miles morales",
    "captain marvel", "carol danvers",
    "ms. marvel", "kamala khan",
    "she-hulk", "jennifer walters",
    "okoye", "shuri", "nebula", "rocket",
    "kate bishop", "yelena belova",
    # Street-level / Avengers comics
    "luke cage", "jessica jones", "iron fist",
    "wolverine", "storm", "doctor voodoo",
]

# Binary search needs a sorted list
AVENGERS = sorted(set(AVENGERS))


# ---------------------------------------------------------------- logic
def justfind(names, target):
    """Binary search. Returns (index or -1, list of steps taken)."""
    steps = []
    left = 0
    right = len(names) - 1

    while left <= right:
        middle = (left + right) // 2
        value = names[middle]

        if value == target:
            action = "Match"
        elif value < target:
            action = "Target is after this, go right"
        else:
            action = "Target is before this, go left"

        steps.append(
            {
                "Step": len(steps) + 1,
                "Left": left,
                "Middle": middle,
                "Right": right,
                "Checking": value,
                "Decision": action,
            }
        )

        if value == target:
            return middle, steps
        elif value < target:
            left = middle + 1
        else:
            right = middle - 1

    return -1, steps


# ---------------------------------------------------------------- style
st.markdown(
    """
    <style>
    .block-container { max-width: 760px; padding-top: 3rem; }
    h1 { letter-spacing: -0.02em; }
    div[data-testid="stMetric"] {
        border-left: 3px solid #E23636;
        padding-left: 0.9rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------- sidebar
with st.sidebar:
    st.header("How it works")
    st.write(
        "Binary search checks the middle name of a sorted list. "
        "If your target comes earlier in the alphabet, it drops the right half. "
        "If later, it drops the left half. It repeats until it finds the name "
        "or runs out of names."
    )
    with st.expander(f"All {len(AVENGERS)} names in the list"):
        st.write(", ".join(name.title() for name in AVENGERS))

# ---------------------------------------------------------------- main
st.title("Avengers Finder")
st.write("Check whether a Marvel character has been an Avenger. Hero names and real names both work.")

with st.form("search_form"):
    query = st.text_input("Character name", placeholder="e.g. Iron Man, Wanda, Sam Wilson")
    submitted = st.form_submit_button("Search", type="primary")

if submitted:
    target = query.strip().lower()

    if not target:
        st.warning("Type a name to search.")
    else:
        index, steps = justfind(AVENGERS, target)

        if index != -1:
            st.success(f"{target.title()} is in the Avengers list (index {index}).")
        else:
            st.error(f"{target.title()} is not in the Avengers list. Check the spelling, or try the hero name or real name.")

        col1, col2, col3 = st.columns(3)
        col1.metric("Names in list", len(AVENGERS))
        col2.metric("Steps taken", len(steps))
        col3.metric("Worst case", math.ceil(math.log2(len(AVENGERS) + 1)))

        st.subheader("Search steps")
        st.dataframe(steps, hide_index=True, use_container_width=True)
