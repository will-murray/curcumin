import numpy as np
import pandas as pd
import sys

def top_n_differentially_regulated_genes(filepath, n = 30):
    """
    Determines the top n differentially expressed genes from Cufflinks differential expression test file (https://cole-trapnell-lab.github.io/cufflinks/cuffdiff/#fpkm-tracking-format)
    """

    D = pd.read_csv(filepath_or_buffer= filepath, delimiter="\t", header = 0)

    D = D[D["significant"] == "yes"].copy() #check that this matters
    D["log2(fold_change)"] = np.log2(D["value_1"] / D["value_2"]) # We want genes that are upregulated in treatment to have a positive FC
    D["FC"] = D["value_1"] / D["value_2"]
    D["z_norm_log2FC"] = (D["log2(fold_change)"] - D["log2(fold_change)"].mean() ) / D["log2(fold_change)"].std()    

    D = D.sort_values(by = "z_norm_log2FC",key = lambda fc: abs(fc), ascending= False)
    D = D.head(n).sort_values("z_norm_log2FC",ascending=False)

    return D


