
from algorithms import fifo, lru, optimal

# Sample input
pages = [1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5]
frame_count = 3

# Execute all algorithms
results = [
    fifo(pages, frame_count),
    lru(pages, frame_count),
    optimal(pages, frame_count)
]

# Display results
print("PAGE REPLACEMENT ALGORITHM COMPARISON")
print("------------------------------------")

for result in results:
    print("\nAlgorithm:", result["algorithm"])
    print("Total Page Hits:", result["hits"])
    print("Total Page Faults:", result["faults"])

    print("\nPage\tFrames\t\tStatus")

    for step in result["history"]:
        print(
            step["page"],
            "\t",
            step["frames"],
            "\t",
            step["status"]
        )
