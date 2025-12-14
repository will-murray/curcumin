# client for working with ClueGO API
import requests
import json
import os
from pathlib import Path
from urllib.parse import quote
import py4cytoscape as cy
import csv


class ClueGoClient:
    def __init__(self, name="CLUEGO client unnamed"):

        self.EXAMPLE_NAME = name
        self.SEP = "/"
        self.HOME_FOLDER = str(Path.home())
        self.OUTPUT_FOLDER = self.HOME_FOLDER + self.SEP + self.EXAMPLE_NAME
        try:
            os.stat(self.OUTPUT_FOLDER)
        except:
            os.mkdir(self.OUTPUT_FOLDER)

        self.CLUEGO_HOME_FOLDER = (
            self.HOME_FOLDER + self.SEP + "ClueGOConfiguration" + self.SEP + "v2.5.10"
        )
        self.PORT_NUMBER = "1234"
        self.HOST_ADDRESS = "localhost"
        self.HEADERS = {"Content-Type": "application/json"}
        # define base urls
        self.CYTOSCAPE_BASE_URL = (
            "http://" + self.HOST_ADDRESS + ":" + self.PORT_NUMBER + self.SEP + "v1"
        )
        self.CLUEGO_BASE_URL = (
            self.CYTOSCAPE_BASE_URL
            + self.SEP
            + "apps"
            + self.SEP
            + "cluego"
            + self.SEP
            + "cluego-manager"
        )

        self.NUM_CLUSTERS = None
        self._ORGANISM = None

        self.__verify_cytoscape_connection()
        self.__verify_CLUEGO_installation()
        self.__verify_ClUEGO_is_active()
        print("client is online.....")

    def __verify_cytoscape_connection(self):
        try:
            cy.cytoscape_ping(self.CYTOSCAPE_BASE_URL)
        except Exception as e:
            print(e)

    def __verify_CLUEGO_installation(self):
        try:
            dependencies = [
                app
                for app in cy.get_installed_apps(self.CYTOSCAPE_BASE_URL)
                if app["appName"] == "ClueGO" or app["appName"] == "CluePedia"
            ]
            if len(dependencies) != 2:
                print(
                    f"ClueGO and Cluepedia must be installed for use of this client. At least one is not.\ninstalled packages : {dependancies}"
                )
        except Exception as e:
            print(e)

    def __verify_ClUEGO_is_active(self):
        try:
            url = (
                self.CLUEGO_BASE_URL
                + self.SEP
                + "organisms"
                + self.SEP
                + "set-organism"
                + self.SEP
                + quote("Homo Sapiens")
            )
            response = requests.put(url)
            if not str(response.status_code).startswith("2"):
                print("ClueGO/CluePedia needs to be started in Cytoscape")
                exit()

        except Exception as e:
            print(e)

    def __read_gene_list(self, data):
        gene_ids = []
        with open(data, "r") as f:
            reader = csv.reader(f, delimiter="\t")
            for row in reader:
                gene_ids.append(row[0])
        return gene_ids

    def set_organism(self, organism_name):
        """
        organism_name can be one of "Homo Sapiens" or "Mus Musculus" by default.
        Use get_all_organisms to view options; Uploading a new organism can be done with GUI.
        """
        try:
            url = (
                self.CLUEGO_BASE_URL
                + self.SEP
                + "organisms"
                + self.SEP
                + "set-organism"
                + self.SEP
                + quote(organism_name)
            )
            response = requests.put(url)
            print(f"set_organism\t{response.status_code}")
            if str(response.status_code).startswith("4"):
                print(f"\t{response.json()}")
            self.ORGANISM = organism_name
        except Exception as e:
            print(e)

    def get_all_organisms(self):
        try:
            url = (
                self.CLUEGO_BASE_URL
                + self.SEP
                + "organisms"
                + self.SEP
                + "get-all-installed-organisms"
            )
            response = requests.get(url)
            print(f"get_all_organisms\t{response.status_code}")
            if str(response.status_code).startswith("4"):
                print(f"\t{response.json()}")
            return response.json()
        except Exception as e:
            print(e)

    def set_analysis(
        self,
        input_panel_index=1,
        node_shape="Ellipse",
        cluster_color="#ff0000",
        min_number_of_genes_per_term=3,
        min_percentage_of_genes_mapped=4,
        no_restrictions=False,
    ):
        try:
            response = requests.put(
                self.CLUEGO_BASE_URL
                + self.SEP
                + "cluster"
                + self.SEP
                + "set-analysis-properties"
                + self.SEP
                + str(input_panel_index)
                + self.SEP
                + node_shape
                + self.SEP
                + quote(cluster_color)
                + self.SEP
                + str(min_number_of_genes_per_term)
                + self.SEP
                + str(min_percentage_of_genes_mapped)
                + self.SEP
                + str(no_restrictions),
                headers=self.HEADERS,
            )
            print(f"set_analysis\t{response.status_code}")
            if str(response.status_code).startswith("4"):
                print(f"\t{response.json()}")
        except Exception as e:
            print(e)

    def get_ontologies(self):
        try:
            url = (
                self.CLUEGO_BASE_URL
                + self.SEP
                + "ontologies"
                + self.SEP
                + "get-ontology-info"
            )
            response = requests.get(url)
            print(f"get_ontologies\t{response.status_code}")
            if str(response.status_code).startswith("4"):
                print(f"\t{response.json()}")
            return response.json()
        except Exception as e:
            print(e)

    def set_ontologies(self, ontologies=["3;Ellipse", "10;Triangle", "9;Rectangle"]):

        if ontologies == "Nida":
            ontologies = [
                "2;Ellipse",
                "3;Ellipse",
                "4;Ellipse",
                "5;Ellipse",
                "7;Octagon",
                "8;Rectangle",
                "9;Rectangle",
                "10;Triangle",
            ]

        try:
            url = self.SEP.join([self.CLUEGO_BASE_URL, "ontologies", "set-ontologies"])
            response = requests.put(
                url=url, json=ontologies, headers={"Content-Type": "application/json"}
            )
            print(f"set_ontologies\t{response.status_code}")
            if str(response.status_code).startswith("4"):
                print(f"\t{response.json()}")

        except Exception as e:
            print(e)

    def set_number_of_clusters(self, num_clusters=1):
        num_clusters = str(num_clusters)
        url = self.SEP.join(
            [self.CLUEGO_BASE_URL, "cluster", "max-input-panel", num_clusters]
        )
        response = requests.put(url)
        print(f"set_number_of_clusters\t{response.status_code}")

    def set_gene_ids(self, gene_ids=None, cluster_id=1):
        """
        gene list must be a list, ex. ["NM_001482", "NM_005012", "NM_001033719", "ENST00000271277"]
        """

        if gene_ids is None:
            path = os.path.join(
                self.CLUEGO_HOME_FOLDER,
                "ClueGOExampleFiles",
                "GSE6887_Bcell_Healthy_top200UpRegulated.txt",
            )
            gene_ids = self.__read_gene_list(path)

        gene_ids = json.dumps(gene_ids)

        response = requests.put(
            url=self.SEP.join(
                [
                    self.CLUEGO_BASE_URL,
                    "cluster",
                    "upload-ids-list",
                    quote(str(cluster_id)),
                ]
            ),
            data=gene_ids,
            headers=self.HEADERS,
        )
        print(f"set_gene_ids\t{response.status_code}")

        if str(response.status_code)[0] in ["4", "5"]:
            print("failed")
            try:
                print(f"\t{response.json}")
            except Exception as e:
                print(e)

    def get_network_ids(self):
        try:

            url = self.SEP.join([self.CLUEGO_BASE_URL, "get-all-cluego-networks"])
            response = requests.get(url, headers={"Content-Type": "application/json"})
            print(f"get_network_ids\t{response.status_code}")

            if str(response.status_code).startswith("4"):
                print(f"\t{response.json()}")

        except Exception as e:
            print(e)

    def set_analysis_properties_for_cluster(
        self,
        min_num_genes_per_GO_term: int = 3,
        pct_genes_mapped_per_term: float = 3,
        no_restrictions: bool = False,
        cluster_color: str = "#ff0000",
        preset: str = "Default",
        node_shape: str = "Ellipse",
        cluster_num: int = 1,
    ):

        if preset == "global":
            min_num_genes_per_GO_term = 50
            pct_genes_mapped_per_term = 0
        elif preset == "medium":
            min_num_genes_per_GO_term = 3
            pct_genes_mapped_per_term = 3
        elif preset == "detailed":
            min_num_genes_per_GO_term = 1
            pct_genes_mapped_per_term = 50

        url = self.SEP.join(
            [
                self.CLUEGO_BASE_URL,
                "cluster",
                "set-analysis-properties",
                str(cluster_num),
                node_shape,
                quote(cluster_color),
                str(min_num_genes_per_GO_term),
                str(pct_genes_mapped_per_term),
                str(no_restrictions),
            ]
        )
        print(url)
        response = requests.put(url)
        print(f"get_network_ids\t{response.status_code}")

    def set_min_max_GO_levels(self, min, max, all_levels=False):
        """
        :param min (int) - specifies the minimum GO level permitted
        :param min (int) - specifies the max GO level permitted
        :param all_levels (bool) - specifies if all levels are permitted
        """

        try:

            url = self.SEP.join(
                [
                    self.CLUEGO_BASE_URL,
                    "ontologies",
                    "set-min-max-levels",
                    str(min),
                    str(max),
                    str(all_levels),
                ]
            )
            response = requests.put(url, headers={"Content-Type": "application/json"})
            print(f"set_min_max_GO_levels\t{response.status_code}")

            if str(response.status_code).startswith("4"):
                print(f"\t{response.json()}")

        except Exception as e:
            print(e)

    def run_analysis(self, analysis_name):
        try:

            option = "Cancel and refine selection"
            url = self.SEP.join(
                [self.CLUEGO_BASE_URL, quote(analysis_name), quote(option)]
            )
            response = requests.get(url)
            print(f"run_analysis\t{response.status_code}")

            if str(response.status_code).startswith("4"):
                print(f"\t{response.json()}")

        except Exception as e:
            print(e)

    def set_network_specificity(self, specificity, cluster_num=1):
        """
        This function invokes set_min_max_GO_levels and analysis properties for cluster to define to specificity threshold for generating networks.
        """
        assert specificity in ["global", "medium", "detailed", "semi-detailed"]

        if specificity == "global":
            self.set_min_max_GO_levels(1, 4)
            self.set_analysis_properties_for_cluster(
                preset=specificity, cluster_num=cluster_num
            )
        elif specificity == "medium":
            self.set_min_max_GO_levels(3, 8)
            self.set_analysis_properties_for_cluster(
                preset=specificity, cluster_num=cluster_num
            )
        elif specificity == "detailed":
            self.set_min_max_GO_levels(7, 15)
            self.set_analysis_properties_for_cluster(
                preset=specificity, cluster_num=cluster_num
            )
        else:
            self.set_min_max_GO_levels(6, 12)
            self.set_analysis_properties_for_cluster(6, 12, cluster_num=cluster_num)


def color_with_FC(n):
    """
    Assumes that the network to be colored is the one currently in cytoscape. Could extend this to work wiht a ID (SUID?)
    """

    node_table = cy.get_table_columns("node")

    D = get_diffy_expressed_genes(
        "diff/5s_vs_4s.gene_exp.diff",
    )[["gene_id", "z_norm_log2FC"]]

    node_table = node_table.merge(D, how="left", left_on="ID", right_on="gene_id")

    node_table["z_norm_log2FC"] = node_table["z_norm_log2FC"].fillna(0)

    D = {row["gene_id"]: row["z_norm_log2FC"] for _, row in D.iterrows()}

    for idx, row in node_table.iterrows():
        genes = row.get("Associated Genes Found")
        if pd.notna(genes):
            # ClueGO stores genes as a string like "[COX7A2, RPS29]"
            genes = genes.strip("[]")
            gene_list = [g.strip() for g in genes.split(",")]

            gene_list = [g for g in gene_list if g in D.keys()]
            if gene_list:
                avg_fc = sum(D[g] for g in gene_list) / len(gene_list)
                print(avg_fc)
                node_table.at[idx, "z_norm_log2FC"] = avg_fc

    node_table["z_norm_log2FC"] = pd.to_numeric(
        node_table["z_norm_log2FC"], errors="coerce"
    )

    cy.load_table_data(node_table, data_key_column="name")

    z_norm_color_mapping = cy.map_visual_property("node fill color", "z_norm_log2FC", "c")
    cy.update_style_mapping("ClueGoVisualStyleForGroups_0", z_norm_color_mapping)


####################################################################
import pandas as pd
from get_significant_genes import get_diffy_expressed_genes


n = 150
gene_list = list(
    get_diffy_expressed_genes("diff/5s_vs_4s.gene_exp.diff")["gene_id"].head(n)
)


# global stuff
client = ClueGoClient("test client")
client.set_organism("Homo Sapiens")
client.set_number_of_clusters(1)
client.set_ontologies("Nida")  # default

# cluster 1
client.set_gene_ids(gene_list)
# client.set_network_specificity("detailed")
client.set_min_max_GO_levels(7,10)
client.set_analysis_properties_for_cluster(1, 50)

client.run_analysis("Domer custom - low res")

color_with_FC(n)
