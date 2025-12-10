import numpy as np
import pandas as pd
import sys
import matplotlib.pyplot as plt
import seaborn as sb

"""
postive log2FC implies upregulation in the treated (4s) sample
"""

def get_diffy_expressed_genes(filepath, n = None):
    """
    Transforms the cuffdiff dataframe specified at file_path to a pd:Dataframe with columns
    -  gene_id
    - log2(fold_change)
    - z_norm_log2FC: Normalized FC based on rows from the input dataframe whose log2(fold_change) != -inf. I 
    - p_value
    - q_value
    Removes all rows with significance == no

    """
    D = pd.read_csv(filepath, delimiter="\t")
    #remove all rows whose log2FC is inf
    D = D.replace([float("inf"), float("-inf")], pd.NA).dropna(subset=["log2(fold_change)"])
    D["z_norm_log2FC"] = (D["log2(fold_change)"] - D["log2(fold_change)"].mean() ) / D["log2(fold_change)"].std()    
    D = D[D["significant"] == "yes"]

    D = D[ ["gene_id", "log2(fold_change)", "z_norm_log2FC", "p_value", "q_value"] ]
    
    D.sort_values(by="z_norm_log2FC", inplace=True, key = lambda x: abs(x), ascending=False)
    D["z_norm_log2FC"] = pd.to_numeric(D["z_norm_log2FC"], errors="coerce")

    if n is not None:
        return D.head(n)
    return D


def make_heatmaps(D,n):
    n = min(n, 30)

    D_abs = D.sort_values("z_norm_log2FC", key=lambda x: abs(x), ascending= False)
    sb.heatmap(
        D_abs[["z_norm_log2FC"]].head(n).sort_values("z_norm_log2FC", ascending=False),
        yticklabels=D["gene_id"].head(n),
        cmap = "Greens"
        )
    plt.title(f"Top {n} differentially regulated genes")
    plt.savefig("figs/heatmaps.png")
    plt.close()


def make_histogram(D):

    plt.hist(D["z_norm_log2FC"],bins=100)
    plt.title("Distrubution of Z-normalized Log2FC values")
    plt.savefig("figs/distribution of FC")


def main():
    file = "diff/5s_vs_4s.gene_exp.diff"
    assert len(sys.argv) == 2, "usage : python3 get_significant_genes [n] - must specify how many genes you want" 
    n = int(sys.argv[1])

    D = get_diffy_expressed_genes(file)
    make_histogram(D)
    make_heatmaps(D,n)

    print(D.head(n).to_string())
    print(list(D["gene_id"].head(n)))

if __name__ == "__main__":
    main()



