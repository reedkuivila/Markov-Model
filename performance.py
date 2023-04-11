import sys
from markov import identify_speaker
import pandas
import time
import seaborn as sns
import matplotlib.pyplot as plt




if __name__ == "__main__":
    if len(sys.argv) != 6:
        print(
            f"Usage: python3 {sys.argv[0]} <filenameA> <filenameB> <filenameC> <max-k> <runs>"
        )
        sys.exit(1)

    # extract parameters from command line & convert types
    filenameA, filenameB, filenameC, max_k, runs = sys.argv[1:]
    max_k = int(max_k)
    runs = int(runs)

    # TODO: add code here to open files & read text
    f = open(filenameA, "r")
    textA = f.read()
    
    f = open(filenameB, "r")
    textB = f.read()
    
    f = open(filenameC, "r")
    textC = f.read()
    
    # TODO: run performance tests as outlined in README.md
    start = time.perf_counter()
    tup = identify_speaker(textA, textB, textC, max_k, use_hashtable=True)
    elapsed = start - time.perf_counter()
    
    data_frame = {"implementation": [], "k": [], "time": []} 
    data_frame = pandas.DataFrame(data_frame)

    for i in range(max_k+1):
        avg_time = 0
        for r in range(runs + 1):
            # add items to the hash table
            start_timer = time.perf_counter()
            speaker_table = identify_speaker(textA, textB, textC, i, True)
            end_timer = time.perf_counter() - start_timer
            avg_time += end_timer

        avg_time = avg_time/runs
        df = {"implementation": ["hash"], "k": [f"{i}"], "time": [avg_time]} 
        df = pandas.DataFrame(df)
        data_frame = pandas.concat([data_frame, df], ignore_index=True)
        

    for i in range(max_k+1):
        avg_time = 0
        for r in range(runs + 1):
            # add items to the hash table
            start_timer = time.perf_counter()
            speaker_table = identify_speaker(textA, textB, textC, i, False)
            end_timer = time.perf_counter() - start_timer
            avg_time += end_timer

        avg_time = avg_time/runs # same thign for dictionary
        df = {"implementation": ["dictionary"], "k": [f"{i}"], "time": [avg_time]} 
        df = pandas.DataFrame(df)
        data_frame = pandas.concat([data_frame, df], ignore_index=True)
        
    # TODO: write execution_graph.png
    #data_file = pandas.DataFrame(data_frame)
    #data_dict = data_file.groupby(by = ['k', 'implementation'].mean())

    performance_graph = sns.lineplot(linestyle='-', marker='o', x = "k", y = "time", data = data_frame, hue="implementation")
    plt.savefig('perf.png')
    print("something")

