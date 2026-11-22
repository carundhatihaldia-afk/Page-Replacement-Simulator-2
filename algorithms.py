
def validate_input(pages, frame_count):
    if frame_count <= 0:
        raise ValueError("Number of frames must be positive.")

    if not pages:
        raise ValueError("Page reference string cannot be empty.")


# 1. FIFO - First In First Out
def fifo(pages, frame_count):
    validate_input(pages, frame_count)

    frames = []
    pointer = 0
    hits = 0
    faults = 0
    history = []

    for page in pages:

        if page in frames:
            hits += 1
            status = "Hit"

        else:
            faults += 1
            status = "Fault"

            if len(frames) < frame_count:
                frames.append(page)
            else:
                frames[pointer] = page

            pointer = (pointer + 1) % frame_count

        history.append({
            "page": page,
            "frames": frames.copy(),
            "status": status
        })

    return {
        "algorithm": "FIFO",
        "history": history,
        "hits": hits,
        "faults": faults
    }


# 2. LRU - Least Recently Used
def lru(pages, frame_count):
    validate_input(pages, frame_count)

    frames = []
    last_used = {}
    hits = 0
    faults = 0
    history = []

    for i, page in enumerate(pages):

        if page in frames:
            hits += 1
            status = "Hit"

        else:
            faults += 1
            status = "Fault"

            if len(frames) < frame_count:
                frames.append(page)
            else:
                least_recent = min(
                    frames,
                    key=lambda p: last_used[p]
                )

                index = frames.index(least_recent)
                frames[index] = page

        last_used[page] = i

        history.append({
            "page": page,
            "frames": frames.copy(),
            "status": status
        })

    return {
        "algorithm": "LRU",
        "history": history,
        "hits": hits,
        "faults": faults
    }


# 3. Optimal Page Replacement
def optimal(pages, frame_count):
    validate_input(pages, frame_count)

    frames = []
    hits = 0
    faults = 0
    history = []

    for i, page in enumerate(pages):

        if page in frames:
            hits += 1
            status = "Hit"

        else:
            faults += 1
            status = "Fault"

            if len(frames) < frame_count:
                frames.append(page)

            else:
                future_use = []

                for frame_page in frames:
                    if frame_page in pages[i + 1:]:
                        next_use = pages[i + 1:].index(frame_page)
                    else:
                        next_use = float("inf")

                    future_use.append(next_use)

                replace_index = future_use.index(
                    max(future_use)
                )

                frames[replace_index] = page

        history.append({
            "page": page,
            "frames": frames.copy(),
            "status": status
        })

    return {
        "algorithm": "Optimal",
        "history": history,
        "hits": hits,
        "faults": faults
    }
  
