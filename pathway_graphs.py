#client for working with ClueGO API
import requests
import json
import os
from pathlib import Path
from urllib.parse import quote
import py4cytoscape as cy


class ClueGoClient():
    def __init__(self,name = "CLUEGO client unnamed"):


        self.EXAMPLE_NAME = name
        self.SEP = "/"   
        self.HOME_FOLDER = str(Path.home())
        self.OUTPUT_FOLDER = self.HOME_FOLDER+self.SEP+self.EXAMPLE_NAME
        try:
            os.stat(self.OUTPUT_FOLDER)
        except:
            os.mkdir(self.OUTPUT_FOLDER)

        self.CLUEGO_HOME_FOLDER = self.HOME_FOLDER+self.SEP+"ClueGOConfiguration"+self.SEP+"v2.5.3"
        self.PORT_NUMBER = "1234"
        self.HOST_ADDRESS = "localhost"
        self.HEADERS = {'Content-Type': 'application/json'}
        # define base urls
        self.CYTOSCAPE_BASE_URL = "http://"+self.HOST_ADDRESS+":"+self.PORT_NUMBER+self.SEP+"v1"
        self.CLUEGO_BASE_URL = self.CYTOSCAPE_BASE_URL+self.SEP+"apps"+self.SEP+"cluego"+self.SEP+"cluego-manager"
        
        self.NUM_CLUSTERS = None
        self._ORGANISM = None

        self.__verify_cytoscape_connection()
        self.__verify_CLUEGO_installation()
        print("Client Connections verified")


    def __verify_cytoscape_connection(self):
        try:
            cy.cytoscape_ping(self.CYTOSCAPE_BASE_URL)
        except:
            exit()
    
    def __verify_CLUEGO_installation(self):
        dependencies = [app for app in cy.get_installed_apps(self.CYTOSCAPE_BASE_URL) if app['appName'] == "ClueGO" or app["appName"] == "CluePedia"]
        if len(dependencies) != 2:
            print(f"ClueGO and Cluepedia must be installed for use of this client. At least one is not.\ninstalled packages : {dependancies}")

    def set_organism(self, organism_name):
        """
        organism_name can be one of "Homo Sapiens" or "Mus Musculus" by default.
        Use get_all_organisms to view options; Uploading a new organism can be done with GUI.
        """
        try:
            url = self.CLUEGO_BASE_URL + self.SEP + "organisms" + self.SEP + "set-organism" + self.SEP + quote(organism_name)
            response = requests.put(url)
            print(f"[{response.status_code}] : set_organism")
            self.ORGANISM = organism_name
        except:
            pass

    
    def get_all_organisms(self):
        try:
            url = self.CLUEGO_BASE_URL + self.SEP + "organisms" + self.SEP + "get-all-installed-organisms"
            response = requests.get(url)
            print(f"[{response.status_code}] : get_all_organisms")
            return response.json()
        except:
            pass
        
    def set_analysis(
            self,
            input_panel_index = 1,
            node_shape = "Ellipse",
            cluster_color = "#ff0000",
            min_number_of_genes_per_term = 3,
            min_percentage_of_genes_mapped = 4,
            no_restrictions = False 
            ):
        response = requests.put(self.CLUEGO_BASE_URL+self.SEP+"cluster"+self.SEP+"set-analysis-properties"+self.SEP+str(input_panel_index)+self.SEP+node_shape+self.SEP+quote(cluster_color)+self.SEP+str(min_number_of_genes_per_term)+self.SEP+str(min_percentage_of_genes_mapped)+self.SEP+str(no_restrictions), headers=self.HEADERS)
        print(f"[{response.status_code}] : set_analysis ")

    def run_analysis(self, name):
        url = self.CLUEGO_BASE_URL + self.SEP + quote(name)
        response = requests.get(url, headers= self.HEADERS)
        print(url)
        print(response.status_code)

client = ClueGoClient("test client")
client.set_organism("Homo Sapiens")
client.set_analysis()
client.run_analysis("test")

