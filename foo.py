import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
D = pd.read_csv("fkpm/5s_vs_4s.cds.fpkm_tracking", delimiter='\t',header=0)
D["rank"] = D["5s_FPKM"] - D["4s_FPKM"]
D["rank"] = D["rank"] / D["rank"].abs().max()

top_n = 30
D = D.assign(abs_rank = D["rank"].abs()).sort_values(by=['abs_rank'],ascending=False)
D_ = D.head(top_n)


sns.heatmap(D_sub[["rank"]],annot=True, fmt=".2f", cmap="plasma",yticklabels=D_sub["gene_id"], xticklabels=False)
plt.savefig("z_standard_heatmap.png")

print(f"top {top_n} differentially expressed genes:\n{D_sub['gene_id']}")