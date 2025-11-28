import numpy as np
import pandas as pd
import sys
import matplotlib.pyplot as plt
import seaborn as sns
from gprofiler import GProfiler

def top_n_differentially_regulated_genes(filepath, n = 30):
    """
    - Determines the top n differentially expressed genes from cufflinks output. 
    - filepath must specify a file of with the format described here https://cole-trapnell-lab.github.io/cufflinks/cuffdiff/#fpkm-tracking-format
    """

    D = pd.read_csv(filepath_or_buffer= filepath, delimiter="\t", header = 0)

    D = D[D["significant"] == "yes"].copy() #check that this matters
    D["log2(fold_change)"] = np.log2(D["value_1"] / D["value_2"]) # We want genes that are upregulated in treatment to have a positive FC
    D["FC"] = D["value_1"] / D["value_2"]
    D["log2(fold_change)"] = (D["log2(fold_change)"] - D["log2(fold_change)"].mean() ) / D["log2(fold_change)"].std()    

    D = D.sort_values(by = "log2(fold_change)",key = lambda fc: abs(fc), ascending= False)
    D = D.head(n).sort_values("log2(fold_change)",ascending=False)

    return D
    
def invoke_g_profiler(D):
    """
    calls g_profiler on a data frame of genes
    """
    gp = GProfiler(return_dataframe=True)
    response = gp.profile(organism="hsapiens", query= list(D["gene_id"]),no_evidences=False)
    return response


def plotting_my_downfall(D):

    sns.heatmap(D[["log2(fold_change)"]],annot=False, cmap="plasma",yticklabels=D["gene_id"], xticklabels=False,square = True)
    # plt.title(type)
    # plt.savefig(f"{}/{type}.png")
    # plt.close()



# for type in ["cds_exp", "gene_exp", "isoform_exp"]:

D = top_n_differentially_regulated_genes("diff/5s_vs_4s.gene_exp.diff")
print(D.shape)
res = invoke_g_profiler(D)
print(res.shape)
print(res[["name","intersections"]].sort_values("intersections"))
