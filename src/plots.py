import matplotlib.pyplot as plt

def muon_histogram_comp(df1, df2, bin_num=50):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4), sharey=False)

    ax1.hist(df1["decay_time"], bins=bin_num)
    ax1.set_xlabel("Muon decay time (µs)")
    ax1.set_ylabel("Frequency")
    ax1.set_title("Muon decay time (pre-aggregation)")

    ax2.hist(df2["decay_time"], bins=bin_num)
    ax2.set_xlabel("Muon decay time (µs)")
    ax2.set_title("Muon decay time (post-aggregation)")

    plt.show()

def log_cutoffs(df, x_line, bin_num=50):
    plt.hist(df["decay_time"], bins=bin_num)
    plt.yscale("log")
    plt.xlabel("Decay time (µs)")
    plt.ylabel("Counts (log)")
    plt.axvline(x=x_line, color='r', linestyle='--')
    plt.show()

def naive_bin_result(bin_list, tau_list, y_min, y_max):
    plt.bar(bin_list, tau_list)
    plt.title("Muon half-life and bin size relation")
    plt.xlabel("Bin size (count)")
    plt.ylabel("Muon half-life (μs)")
    plt.ylim((y_min, y_max))
    plt.show()