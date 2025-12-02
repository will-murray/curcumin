import sys
from get_significant_genes import top_n_differentially_regulated_genes
import py4cytoscape as cyto
import requests
import pandas as pd
import time
if len(sys.argv) > 1:
    input_filepath = sys.argv[1]
else:
    input_filepath = "diff/5s_vs_4s.gene_exp.diff"
    print(f"using default file path: {input_filepath}")


"""
Creates a Protien to Protien graph in Cytoscape for the given .diff file
"""

def get_edge_data(nodes):
    genes = "%0d".join(nodes['id'])
   
    response = requests.get(
        url="https://string-db.org/api/json/network",
        params={
            "identifiers" : genes,
            "species" : 9606
        }
    )
    df = pd.DataFrame(response.json())
    df.rename(columns= {"preferredName_A" : "source", "preferredName_B": "target"},inplace=True)
    df = df[df['source'].isin(nodes["id"]) & df['target'].isin(nodes["id"])]

    return df


nodes = top_n_differentially_regulated_genes(input_filepath, 30)
nodes.rename(columns= {"gene_id" : "id"}, inplace= True)
edges = get_edge_data(nodes)


network_id = cyto.get_network_count()

cyto.create_network_from_data_frames(
    nodes=nodes,
    edges=edges,
    title = f"protien-to-protien network {network_id} | {input_filepath}"
)



cyto.set_node_shape_default('ellipse')

cyto.set_node_color_mapping(
    table_column='z_norm_log2FC',          # column in your node table
    table_column_values=[-3.0, 0.0, 3.0],  # min, mid, max values
    colors=['#0000FF', '#FFFFFF', '#FF0000'],  # blue → white → red
    mapping_type='c',                      # continuous mapping
    default_color='#CCCCCC',               # fallback color
)
