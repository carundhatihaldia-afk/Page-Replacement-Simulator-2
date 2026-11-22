
"""Streamlit dashboard for comparing page replacement algorithms."""

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

from algorithms import fifo, lru, optimal


# -------------------------------
# PAGE CONFIGURATION AND STYLING
# -------------------------------
st.set_page_config(
    page_title="Page Replacement Algorithm Simulator",
    page_icon="💻",
    layout="wide",
)

st.markdown(
    """
    <style>
    .main-title {font-size: 2.15rem; font-weight: 750; margin-bottom: 0.2rem;}
    .sub-title {color: #64748b; font-size: 1rem; margin-bottom: 1.2rem;}
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="main-title">Page Replacement Algorithm Simulator</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="sub-title">Comparative Analysis of FIFO, LRU and Optimal Algorithms | Operating Systems CO4 Mini Project</div>',
    unsafe_allow_html=True,
)
st.write(
    "Enter a page reference string and the number of memory frames. "
    "The simulator runs all three algorithms and compares their page hits and page faults."
)
st.divider()


# -------------------------------
# SIDEBAR INPUT FORM
# -------------------------------
st.sidebar.header("Simulation Settings")
st.sidebar.caption("Enter page numbers separated by commas or spaces.")

with st.sidebar.form("simulation_form"):
    reference_string = st.text_input(
        "Page reference string",
        value="1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5",
        help="Example: 1, 2, 3, 4, 1, 2",
    )
    frame_count = st.number_input(
        "Number of memory frames",
        min_value=1,
        max_value=20,
        value=3,
        step=1,
    )
    run_simulation = st.form_submit_button("Run Simulation", use_container_width=True)


# -------------------------------
# RUN AND STORE SIMULATION
# -------------------------------
if run_simulation:
    try:
        tokens = reference_string.replace(",", " ").split()
        if not tokens:
            raise ValueError("Please enter a page reference string.")

        pages = [int(token) for token in tokens]
        if any(page < 0 for page in pages):
            raise ValueError("Page numbers must be zero or positive integers.")

        frame_count_int = int(frame_count)
        results = [
            fifo(pages, frame_count_int),
            lru(pages, frame_count_int),
            optimal(pages, frame_count_int),
        ]

        st.session_state["pages"] = pages
        st.session_state["frame_count"] = frame_count_int
        st.session_state["results"] = results

    except ValueError as error:
        st.sidebar.error(f"Invalid input: {error}")
        st.session_state.pop("pages", None)
        st.session_state.pop("frame_count", None)
        st.session_state.pop("results", None)


# -------------------------------
# DISPLAY RESULTS
# -------------------------------
if "results" not in st.session_state:
    st.info("Set your inputs in the sidebar and click **Run Simulation** to begin.")
    st.markdown("#### What this simulator demonstrates")
    st.write(
        "- **FIFO:** replaces the page that entered memory first.\n"
        "- **LRU:** replaces the page that has not been used for the longest time.\n"
        "- **Optimal:** replaces the page whose next use is farthest in the future."
    )
else:
    pages = st.session_state["pages"]
    frame_count = st.session_state["frame_count"]
    results = st.session_state["results"]
    total_requests = len(pages)

    st.header("1. Simulation Summary")
    st.caption(f"Reference string: {', '.join(map(str, pages))}  |  Frames: {frame_count}  |  Requests: {total_requests}")

    summary_rows = []
    for result in results:
        summary_rows.append({
            "Algorithm": result["algorithm"],
            "Page Hits": result["hits"],
            "Page Faults": result["faults"],
            "Hit Rate (%)": round(result["hits"] / total_requests * 100, 2),
            "Fault Rate (%)": round(result["faults"] / total_requests * 100, 2),
        })

    summary_df = pd.DataFrame(summary_rows)

    metric_columns = st.columns(3)
    for column, result in zip(metric_columns, results):
        with column:
            st.metric(f"{result['algorithm']} — Page Faults", result["faults"])
            st.metric("Page Hits", result["hits"])

    st.subheader("Algorithm Comparison Table")
    st.dataframe(summary_df, use_container_width=True, hide_index=True)

    fewest_faults = min(result["faults"] for result in results)
    best_algorithms = [
        result["algorithm"] for result in results if result["faults"] == fewest_faults
    ]
    if len(best_algorithms) == 1:
        st.success(
            f"{best_algorithms[0]} has the fewest page faults ({fewest_faults}) "
            f"for this reference string."
        )
    else:
        st.info(
            f"Tie: {', '.join(best_algorithms)} have the fewest page faults ({fewest_faults})."
        )

    # -------------------------------
    # BAR CHART
    # -------------------------------
    st.header("2. Graphical Comparison")
    fig, ax = plt.subplots(figsize=(9, 4.5))
    bars = ax.bar(summary_df["Algorithm"], summary_df["Page Faults"])
    ax.set_title("Total Page Faults by Algorithm")
    ax.set_xlabel("Page Replacement Algorithm")
    ax.set_ylabel("Number of Page Faults")
    ax.set_ylim(0, max(summary_df["Page Faults"].max() + 2, 2))
    ax.bar_label(bars, padding=3)
    ax.grid(axis="y", linestyle="--", alpha=0.35)

# -------------------------------
# GRAPHICAL COMPARISON
# -------------------------------

st.header("2. Graphical Comparison")

st.subheader("Total Page Faults by Algorithm")

# Bar chart showing page faults
fault_chart = summary_df.set_index("Algorithm")[["Page Faults"]]

st.bar_chart(
    fault_chart,
    height=400
)

st.subheader("Comparison of Page Hits and Page Faults")

# Combined comparison chart
comparison_chart = summary_df.set_index("Algorithm")[
    ["Page Hits", "Page Faults"]
]

st.bar_chart(
    comparison_chart,
    height=400
)
