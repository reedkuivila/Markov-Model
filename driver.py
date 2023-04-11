import sys
from markov import identify_speaker

if __name__ == "__main__":
    if len(sys.argv) != 6:
        print(
            f"Usage: python3 {sys.argv[0]} <filenameA> <filenameB> <filenameC> <k> <hashtable-or-dict>"
        )
        sys.exit(1)

    # extract parameters from command line & convert types
    filenameA, filenameB, filenameC, k, hashtable_or_dict = sys.argv[1:]
    k = int(k)
    if hashtable_or_dict not in ("hashtable", "dict"):
        print("Final parameter must either be 'hashtable' or 'dict'")
        sys.exit(1)

    # code here to open files & read text
    f = open(filenameA, "r")
    textA = f.read()

    f = open(filenameB, "r")
    textB = f.read()

    f = open(filenameC, "r")
    textC = f.read()

    # code to call identify_speaker & print results
    if hashtable_or_dict == "hashtable":
        p1, p2, speaker = identify_speaker(textA, textB, textC, k, True)
        print(f"Speaker A:{p1}\n Speaker B: {p2}\n")
        print(f"Conclusion: {speaker} is most likely")
    else:
        p1, p2, speaker = identify_speaker(textA, textB, textC, k, True)
        print(f"Speaker A:{p1}\n Speaker B: {p2}\n")
        print(f"Conclusion: {speaker} is most likely")

    # Output should resemble (values will differ based on inputs):

    # Speaker A: -2.1670591295191572
    # Speaker B: -2.2363636778055525

    # Conclusion: Speaker A is most likely
