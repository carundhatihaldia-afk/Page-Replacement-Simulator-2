
# Comparative Analysis of Page Replacement Algorithms

Operating Systems CO4 mini project implementing FIFO, LRU and Optimal page replacement algorithms.

## Features
- Accepts a page reference string and number of memory frames.
- Simulates FIFO, LRU and Optimal algorithms.
- Calculates page hits, page faults, hit rate and fault rate.
- Displays a page-fault comparison chart.
- Shows an interactive step-by-step memory-frame simulation.
- Highlights page hits and page faults in the execution tables.
- Exports the comparison summary as CSV.

## Requirements
- Python 3.11 or later
- Packages listed in `requirements.txt`

## Setup on Windows PowerShell
Open PowerShell in this project folder and run:

```powershell
py -3.11 -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

If PowerShell blocks activation, run this in the same terminal and activate again:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.venv\Scripts\Activate.ps1
```

## Run the algorithm test

```powershell
python test_algorithms.py
```

For the sample reference string `1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5` with 3 frames, expected page faults are:

| Algorithm | Page hits | Page faults |
|---|---:|---:|
| FIFO | 3 | 9 |
| LRU | 2 | 10 |
| Optimal | 5 | 7 |

## Run the Streamlit application

Use Python to launch Streamlit (this can avoid issues with the `streamlit.exe` launcher on some Windows systems):

```powershell
python -m streamlit run app.py
```

Then open `http://localhost:8501` in your browser.
