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

    def set_gene_ids(self, gene_ids=None, cluster_id="1"):
        """
        gene list must be a list, ex. ["NM_001482", "NM_005012", "NM_001033719", "ENST00000271277"]
        """

        if gene_ids is None:
            path = os.path.join(
                self.CLUEGO_HOME_FOLDER,
                "ClueGOExampleFiles",
                "GSE6887_Bcell_Healthy_top200UpRegulated.txt",
            )
            gene_list = self.__read_gene_list(path)

        gene_ids = json.dumps(gene_list)

        response = requests.put(
            url=self.SEP.join(
                [self.CLUEGO_BASE_URL, "cluster", "upload-ids-list", quote(cluster_id)]
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


client = ClueGoClient("test client")
client.set_organism("Homo Sapiens")
client.set_number_of_clusters()
client.set_ontologies("Nida")
client.run_analysis("test")