
"""Page Replacement Algorithm Simulator"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from algorithms import fifo, lru, optimal


# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="Page Replacement Analysis",
    page_icon="💻",
    layout="wide"
)


# ==========================================
# CUSTOM CSS
# ==========================================

st.markdown("""
<style>
.main-title {
    font-size: 2rem;
    font-weight: 800;
    color: #2563eb;
    text-align: center;
}

.subtitle {
    text-align: center;
    color: #64748b;
    font-size: 1rem;
}

.input-heading {
    font-size: 1.3rem;
    font-weight: 700;
}

div.stButton > button {
    width: 100%;
    background-color: #2563eb;
    color: white;
    font-weight: bold;
    border-radius: 8px;
    min-height: 45px;
}

</style>
""", unsafe_allow_html=True)


# ==========================================
# MAIN TITLE
# ==========================================

st.markdown(
    '<div class="main-title">PAGE REPLACEMENT ANALYSIS</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Operating Systems | Page Replacement Algorithm Simulator</div>',
    unsafe_allow_html=True
)

st.write("")

st.write(
    "This application simulates and compares three "
    "page replacement algorithms: FIFO, LRU and Optimal."
)

st.divider()


# ==========================================
# INPUT SECTION - MAIN SCREEN
# ==========================================

st.markdown(
    '<div class="input-heading">Simulation Input</div>',
    unsafe_allow_html=True
)

st.write("Enter your own page reference string and memory frame count.")

with st.form("main_simulation_form"):

    reference_string = st.text_input(
        "Enter Page Reference String",
        value="1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5",
        placeholder="Example: 1, 2, 3, 4, 1, 2, 5",
        help="Separate page numbers using commas or spaces."
    )

    frame_count = st.number_input(
        "Enter Number of Memory Frames",
        min_value=1,
        max_value=20,
        value=3,
        step=1
    )

    submitted = st.form_submit_button(
        "RUN SIMULATION",
        use_container_width=True
    )


# ==========================================
# INPUT VALIDATION AND EXECUTION
# ==========================================

if submitted:

    try:

        tokens = reference_string.replace(",", " ").split()

        if not tokens:
            raise ValueError("Please enter a page reference string.")

        pages = [int(token) for token in tokens]

        if any(page < 0 for page in pages):
            raise ValueError("Page numbers cannot be negative.")

        if len(pages) > 200:
            raise ValueError("Maximum 200 page references allowed.")

        frame_count = int(frame_count)

        results = [
            fifo(pages, frame_count),
            lru(pages, frame_count),
            optimal(pages, frame_count)
        ]

        st.session_state["pages"] = pages
        st.session_state["frame_count"] = frame_count
        st.session_state["results"] = results

    except ValueError as error:

        st.error(str(error))

        st.session_state.pop("results", None)
        st.session_state.pop("pages", None)
        st.session_state.pop("frame_count", None)


# ==========================================
# SIMULATION RESULTS
# ==========================================

if "results" in st.session_state:

    pages = st.session_state["pages"]
    frame_count = st.session_state["frame_count"]
    results = st.session_state["results"]

    total_requests = len(pages)

    st.divider()

    st.header("1. Simulation Summary")

    st.write("**Page Reference String:**", pages)
    st.write("**Number of Frames:**", frame_count)
    st.write("**Total Page Requests:**", total_requests)


    # ======================================
    # SUMMARY TABLE
    # ======================================

    summary_rows = []

    for result in results:

        hits = result["hits"]
        faults = result["faults"]

        summary_rows.append({
            "Algorithm": result["algorithm"],
            "Page Hits": hits,
            "Page Faults": faults,
            "Hit Rate (%)": round(
                hits / total_requests * 100, 2
            ),
            "Fault Rate (%)": round(
                faults / total_requests * 100, 2
            )
        })

    summary_df = pd.DataFrame(summary_rows)

    st.subheader("Algorithm Performance")

    st.dataframe(
        summary_df,
        use_container_width=True,
        hide_index=True
    )


    # ======================================
    # METRICS
    # ======================================

    st.subheader("Performance Overview")

    columns = st.columns(3)

    for column, result in zip(columns, results):

        with column:

            st.metric(
                result["algorithm"] + " Faults",
                result["faults"]
            )

            st.metric(
                "Page Hits",
                result["hits"]
            )


    # ======================================
    # BEST ALGORITHM
    # ======================================

    minimum_faults = min(
        result["faults"] for result in results
    )

    best_algorithms = [
        result["algorithm"]
        for result in results
        if result["faults"] == minimum_faults
    ]

    st.subheader("Best Performing Algorithm")

    if len(best_algorithms) == 1:

        st.success(
            f"{best_algorithms[0]} performs best "
            f"with {minimum_faults} page faults."
        )

    else:

        st.info(
            f"{', '.join(best_algorithms)} have equal "
            f"minimum page faults: {minimum_faults}."
        )


    # ======================================
    # GRAPHICAL COMPARISON
    # ======================================

    st.divider()

    st.header("2. Graphical Comparison")

    fig, ax = plt.subplots(figsize=(9, 4.5))

    bars = ax.bar(
        summary_df["Algorithm"],
        summary_df["Page Faults"]
    )

    ax.set_title("Page Fault Comparison")
    ax.set_xlabel("Algorithms")
    ax.set_ylabel("Number of Page Faults")

    ax.bar_label(bars, padding=3)

    ax.grid(
        axis="y",
        linestyle="--",
        alpha=0.4
    )

    st.pyplot(fig)

    plt.close(fig)


    # ======================================
    # HIT AND FAULT CHART
    # ======================================

    st.subheader("Page Hits and Page Faults")

    comparison = summary_df.set_index("Algorithm")[
        ["Page Hits", "Page Faults"]
    ]

    st.bar_chart(
        comparison,
        height=350
    )


    # ======================================
    # STEP BY STEP SIMULATION
    # ======================================

    st.divider()

    st.header("3. Step-by-Step Memory Simulation")

    selected_algorithm = st.selectbox(
        "Choose an algorithm to view its execution",
        ["FIFO", "LRU", "Optimal"]
    )

    selected_result = next(
        result for result in results
        if result["algorithm"] == selected_algorithm
    )

    st.write(
        f"Showing the memory frame changes for {selected_algorithm}."
    )

    history_rows = []

    for index, step in enumerate(
        selected_result["history"], start=1
    ):

        row = {
            "Step": index,
            "Page Requested": step["page"]
        }

        for frame_index in range(frame_count):

            if frame_index < len(step["frames"]):
                row[f"Frame {frame_index + 1}"] = (
                    step["frames"][frame_index]
                )
            else:
                row[f"Frame {frame_index + 1}"] = "-"

        row["Status"] = step["status"]

        history_rows.append(row)

    history_df = pd.DataFrame(history_rows)

    st.dataframe(
        history_df,
        use_container_width=True,
        hide_index=True
    )


    # ======================================
    # CSV DOWNLOAD
    # ======================================

    st.divider()

    st.header("4. Download Results")

    csv_data = summary_df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="Download Comparison Report (CSV)",
        data=csv_data,
        file_name="page_replacement_analysis.csv",
        mime="text/csv",
        use_container_width=True
    )


    # ======================================
    # FINAL INFORMATION
    # ======================================

    st.divider()

    st.subheader("About the Algorithms")

    with st.expander("FIFO - First In First Out"):

        st.write(
            "FIFO replaces the page that entered memory first. "
            "It follows the queue principle."
        )

    with st.expander("LRU - Least Recently Used"):

        st.write(
            "LRU replaces the page that has not been used "
            "for the longest period of time."
        )

    with st.expander("Optimal Page Replacement"):

        st.write(
            "Optimal replaces the page whose next use is "
            "farthest in the future. It produces the minimum "
            "possible page faults when future references are known."
        )


# ==========================================
# INITIAL SCREEN
# ==========================================

else:

    st.divider()

    st.header("How to Use This Simulator")

    st.write("""
    1. Enter your page reference string.
    2. Enter the number of memory frames.
    3. Click RUN SIMULATION.
    4. Compare FIFO, LRU and Optimal.
    5. View the step-by-step memory allocation.
    6. Download the comparison report.
    """)

    st.info(
        "Your simulation results will appear here after "
        "you click RUN SIMULATION."
    )


# ==========================================
# FOOTER
# ==========================================

st.divider()

st.caption(
    "Page Replacement Analysis | Operating Systems CO4 Mini Project"
)
