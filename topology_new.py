import content_signatures
from lmconsole.device import LMDeviceDict
import re
import logging
import webbrowser
from datetime import datetime
from graphviz import Graph
import urllib.parse
import threading


logging.basicConfig(format='%(asctime)s - %(levelname)s - %(name)s - %(message)s')
logger = logging.getLogger("L3_Topology")
logger.setLevel(logging.INFO)

class L3Topology:

    def __init__(self, devices: LMDeviceDict)->None:

        """
        Initialize the L3Topology Object

        :param devices: LMDeviceDict Object
        """

        self.devices = devices
        self.mac_add = dict()
        self.interfaces = dict()

        self._data_fetched = False

        return

    def __repr__(self):
        return "L3Topology Object"

    def fetch_in_background(self, vrfs: list=list()) -> None:
        """
        Fetch relevant outputs from devices and parse them in background.

        :param vrfs: (Optional) (Default: ["Global"]) List of VRFs to parse ("Global" for Global Routing Table" and "All"
        for All VRFs including Global Routing Table)

        :return: None
        """

        logger.info("Data fetch started. Use .data_fetched() to check status.")

        t = threading.Thread(target=self.fetch, args=(vrfs))
        t.start()

        return

    def data_fetched(self) -> bool:
        return self._data_fetched


    def fetch(self, vrfs: list=list()) -> None:

        """
        Fetch relevant outputs from devices and parse them.

        :param vrfs: (Optional) (Default: [ "Global"]) List of VRFs to parse ("Global" for Global Routing Table" and "All"
        for All VRFs including Global Routing Table)

        :return: None
        """

        self._data_fetched = False

        self.interfaces.clear()
        self.mac_add.clear()
        self.dev_version = list()
        self.dev_resp = list()
        #self.arp_regex={}
        nodes = list()
        edges = list()

        for device in self.devices:
            tmp_nodes_dict = dict()
            tmp_nodes_dict.update({device:[self.devices[device].attributes.internal['host']]})
            nodes.append(tmp_nodes_dict)
            self.interfaces[device] = {}



        dev_type=self.devices.exec("show version").wait().result

        for k,v in dev_type.items():
            
            taster = content_signatures.inspect_content(v.data)
            list_index = 0
            for list_ele in nodes :
                for i,j in list_ele.items() :
                    if i == k :
                        nodes[list_index].update({k:nodes[list_index][k] + [taster["hw"]]})
                list_index+=1
            ##logger.info(taster)
            self.devices[k]._update_internal_attrs({"device_type":taster["software"],"ssh_config":self.devices[k].attributes.internal.get("ssh_config"),"host":self.devices[k].attributes.internal.get("host"),"description":taster["hw"]})

        ###logger.info(self.devices)

        arp_regex={"ASA releases":'.*?(\w*)\s(\w{1,3}\.\w{1,3}\.\w{1,3}\.\w{1,3})\s*(\w{1,4}\.\w{1,4}\.\w{1,4})',"IOS-XE":'^(?P<device_id>\S+) +(?P<local_interface>[a-zA-Z]+[\s]*[\d\/\.]+) +(?P<hold_time>\d+) +(?P<capability>[RTBSsHIrPDCM\s]+)( +(?P<platform>\S+))?(\s+(?P<port_id>(Fa|Gi|GE|Et).\s*\d*\/*\d*\/*\d*\/*\d*))?$',"IOS":'^(?P<device_id>\S+) +(?P<local_interface>[a-zA-Z]+[\s]*[\d\/\.]+) +(?P<hold_time>\d+) +(?P<capability>[RTBSsHIrPDCM\s]+)( +(?P<platform>\S+))?(\s+(?P<port_id>(Fa|Gi|GE|Et).\s*\d*\/*\d*\/*\d*\/*\d*))?$',"IOS-XR":'^(?P<device_id>\S+) +(?P<local_interface>[a-zA-Z]+[\s]*[\d\/\.]+) +(?P<hold_time>\d+) +(?P<capability>[RTBSsHIrPDCM\s]+)( +(?P<platform>\S+))?(\s+(?P<port_id>(Fa|Gi|GE|Et).\s*\d*\/*\d*\/*\d*\/*\d*))?$',"NXOS":'^(?P<device_id>\S+) +(?P<local_interface>[a-zA-Z]+[\s]*[\d\/\.]+) +(?P<hold_time>\d+) +(?P<capability>[RTBSsHIrPDCM\s]+)( +(?P<platform>\S+))?(\s+(?P<port_id>(Fa|Gi|GE|Et).\s*\d*\/*\d*\/*\d*\/*\d*))?$'}

        ###logger.info(arp_regex)
        ###logger.info(self.devices)

        for device in self.devices:
            logger.info(self.devices[device].attributes.internal.get("device_type"))
            if self.devices[device].attributes.internal.get("device_type")=="ASA releases":

                ##logger.info("inside loop")
                nameif={}
                mac={}

                regex=re.compile(arp_regex['ASA releases'])
                nameif_regex=re.compile('(^\w*\d\/\d)\s*(\S*)\s*\d*')
                #mac_regex=re.compile('(\s*\w*)\s*(\d*\.\d*\.\w*)')
                mac_regex=re.compile('([0-9a-f]{4}\.[0-9a-f]{4}\.[0-9a-f]{4})|(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})')


                ##logger.info("ibefore for")

                for line in self.devices[device].exec("show nameif").wait().result.data.split("\n"):
                    match=nameif_regex.match(line)

                    if match:

                        nameif.update({match.group(2):match.group(1)})
                        intf_name=match.group(1)
                        ##logger.info(intf_name)
                        ##logger.info(nameif)



                for key,value in nameif.items():


                    mac=self.devices[device].exec('show int ' + value + ' | I MAC|IP').wait().result.data


                    match=mac_regex.findall(mac)

                    if match:


                        intf_mac=match[0][0]
                        intf_addr=match[1][1]
                        intf_name=value
                        ##logger.info(intf_mac)
                        ##logger.info(intf_addr)
                        ##logger.info(intf_name)
                        if intf_name not in self.interfaces[device]:
                            ##logger.info(intf_name)
                            ##logger.info(intf_mac)
                            ##logger.info(intf_addr)


                            self.interfaces[device][intf_name]={"vrf": "default",
                                                                "ip_add": intf_addr,
                                                                "mac_add": intf_mac,
                                                                "neighbors": []}

                ##logger.info(self.interfaces[device])




                for line in self.devices[device].exec("show arp").wait().result.data.split("\n"):
                    match=regex.match(line)
                    if match:
                        intf_name=match.group(1)
                        intf_addr=match.group(2)
                        intf_mac=match.group(3)
                        for key,value in nameif.items():
                            if intf_name==key:
                                intf_name=value

                                if intf_name in self.interfaces[device]:
                                    self.interfaces[device][intf_name]["neighbors"].append((intf_addr,intf_mac))
                ##logger.info(self.interfaces[device])

                #Data fetch complete for ASA


                '''
                for key,value in arp.items():
                    for key1,value1 in nameif.items():
                        if key1==value:

                            int_nameif.update({key:value1})
                '''

                ###logger.info(int_nameif)








            if self.devices[device].attributes.internal.get("device_type")=="IOS":
                regex=re.compile(arp_regex['IOS'])



                if vrfs == []:
                    vrfs = ["Global"]
                if "All" in vrfs:
                    vrfs.append("Global")

                    ##logger.info("Fetching VRF data")
                    show_vrf_1 = self.devices.exec("show vrf").wait()

                    show_vrf = dict()

                    for k, v in show_vrf_1.result.items():

                        show_vrf[k] = v["show vrf"]

                if "All" in vrfs:
                    start_parse = False

                    for line in show_vrf[device].data.split("\n"):
                        if "Name" in line:
                            start_parse = True
                            continue

                        if start_parse:
                            try:
                                vrfs.append(line.strip().split(" ")[0])
                            except:
                                continue

                        vrfs = list(set(vrfs))
                if ("Global" in vrfs) or ("All" in vrfs):
                    logger.debug("Fetching CDP for device " + str(device) + " for Global")
                    arp = self.devices[device].exec("show cdp neighbor").wait().result.data.split("\n")
                    start_parse = False
                    for line in arp:
                        if "Device ID" in line:
                            start_parse = True
                        if start_parse:
                            match = regex.match(line)
                            local_intf_name = ""
                            remote_intf_name = ""
                            local_host_name = ""
                            remote_host_name =""
                            if match:
                                #logger.info(line)
                                local_intf_name = match.group('local_interface')

                                remote_intf_name = match.group('port_id')
                                local_host_name = device
                                remote_host_name = match.group('device_id')[:len(match.group('device_id'))-10]
                                exist_flag = False
                                for ele in edges :
                                    if ((((ele['n1'] == device) and (ele['n2'] == remote_host_name)) and (ele['i1'].replace(" ","") == local_intf_name.replace(" ","")) and (ele['i2'].replace(" ","") == remote_intf_name).replace(" ","")) or (((ele['n1'] == remote_host_name) and (ele['n2'] == device)) and ((ele['i1'].replace(" ","") == remote_intf_name.replace(" ","")) and (ele['i2'].replace(" ","") == local_intf_name.replace(" ",""))))) :
                                        exist_flag = True
                                        break
                                
                                if exist_flag == False :    
                                    edges.append({"n1": device,
                                        "i1": local_intf_name,
                                        "n2": remote_host_name,
                                        "i2": remote_intf_name,})

                                if not (edges) :
                                    edges.append({"n1": device,
                                        "i1": local_intf_name,
                                        "n2": remote_host_name,
                                        "i2": remote_intf_name,})
                                logger.info("inside ios")
                                
                    logger.debug("Processing completed for: " + str(device))
                    ##logger.info("********************************VPVPVPVPVPVP")
                    ##logger.info(edges)

                    #logger.info(self.interfaces[device])


            if self.devices[device].attributes.internal.get("device_type")=="IOS-XE":
                ##logger.info("inisde IOS-XE")

                regex=re.compile(arp_regex['IOS-XE'])


                if vrfs == []:
                    vrfs = ["Global"]
                if "All" in vrfs:
                    vrfs.append("Global")

                    ##logger.info("Fetching VRF data")
                    show_vrf_1 = self.devices.exec("show vrf").wait()

                    show_vrf = dict()

                    for k, v in show_vrf_1.result.items():

                        show_vrf[k] = v["show vrf"]

                if "All" in vrfs:
                    start_parse = False

                    for line in show_vrf[device].data.split("\n"):
                        if "Name" in line:
                            start_parse = True
                            continue

                        if start_parse:
                            try:
                                vrfs.append(line.strip().split(" ")[0])
                            except:
                                continue

                        vrfs = list(set(vrfs))
                if ("Global" in vrfs) or ("All" in vrfs):
                    ##logger.debug("Fetching CDP for device " + str(device) + " for Global")
                    arp = self.devices[device].exec("show cdp neighbor").wait().result.data.split("\n")
                    start_parse = False
                    for line in arp:
                        if "Device ID" in line:
                            start_parse = True
                        if start_parse:
                            match = regex.match(line)
                            local_intf_name = ""
                            remote_intf_name = ""
                            local_host_name = ""
                            remote_host_name =""
                            if match:
                                #logger.info(line)
                                local_intf_name = match.group('local_interface')

                                remote_intf_name = match.group('port_id')
                                local_host_name = device
                                remote_host_name = match.group('device_id')[:len(match.group('device_id'))-10]
                                exist_flag = False
                                for ele in edges :
                                    if ((((ele['n1'] == device) and (ele['n2'] == remote_host_name)) and (ele['i1'].replace(" ","") == local_intf_name.replace(" ","")) and (ele['i2'].replace(" ","") == remote_intf_name).replace(" ","")) or (((ele['n1'] == remote_host_name) and (ele['n2'] == device)) and ((ele['i1'].replace(" ","") == remote_intf_name.replace(" ","")) and (ele['i2'].replace(" ","") == local_intf_name.replace(" ",""))))) :
                                        exist_flag = True
                                        break
                                
                                if exist_flag == False :
                                    edges.append({"n1": device,
                                        "i1": local_intf_name,
                                        "n2": remote_host_name,
                                        "i2": remote_intf_name,})

                                if not (edges) :
                                    edges.append({"n1": device,
                                        "i1": local_intf_name,
                                        "n2": remote_host_name,
                                        "i2": remote_intf_name,})
                    ##logger.info("********************************VP2VP2VP2VP2VP2VP2")
                    ##logger.info(edges)
                    ##logger.debug("Processing completed for: " + str(device))

                    ##logger.info(self.interfaces[device])






            if self.devices[device].attributes.internal.get("device_type")=="IOS-XR":
                regex=re.compile(arp_regex['IOS-XR'])


                ##logger.info("inisde IOS-XR")
                if vrfs == []:
                    vrfs = ["Global"]
                if "All" in vrfs:
                    vrfs.append("Global")

                    ##logger.info("Fetching VRF data")
                    show_vrf_1 = self.devices.exec("show vrf").wait()

                    show_vrf = dict()

                    for k, v in show_vrf_1.result.items():

                        show_vrf[k] = v["show vrf"]

                if "All" in vrfs:
                    start_parse = False

                    for line in show_vrf[device].data.split("\n"):
                        if "Name" in line:
                            start_parse = True
                            continue

                        if start_parse:
                            try:
                                vrfs.append(line.strip().split(" ")[0])
                            except:
                                continue

                        vrfs = list(set(vrfs))
                ##logger.info(vrfs)
                if ("Global" in vrfs) or ("All" in vrfs):
                    ##logger.info("Fetching CDP for device " + str(device) + " for Global")
                    arp = self.devices[device].exec("show cdp neighbor").wait().result.data.split("\n")
                    start_parse = False
                    for line in arp:
                        if "Device ID" in line:
                            start_parse = True
                        if start_parse:
                            match = regex.match(line)
                            local_intf_name = ""
                            remote_intf_name = ""
                            local_host_name = ""
                            remote_host_name =""
                            if match:
                                local_intf_name_tmp = match.group('local_interface')
                                local_intf_name = local_intf_name_tmp[:2] + "g" + local_intf_name_tmp[2:]

                                remote_intf_name_tmp = match.group('port_id')
                                remote_intf_name = remote_intf_name_tmp[:2] + "g" + remote_intf_name_tmp[2:]

                                local_host_name = device
                                remote_host_name = match.group('device_id')[:len(match.group('device_id'))-9]
                                exist_flag = False
                                for ele in edges :
                                    if ((((ele['n1'] == device) and (ele['n2'] == remote_host_name)) and (ele['i1'].replace(" ","") == local_intf_name.replace(" ","")) and (ele['i2'].replace(" ","") == remote_intf_name).replace(" ","")) or (((ele['n1'] == remote_host_name) and (ele['n2'] == device)) and ((ele['i1'].replace(" ","") == remote_intf_name.replace(" ","")) and (ele['i2'].replace(" ","") == local_intf_name.replace(" ",""))))) :
                                        exist_flag = True
                                        break
                                
                                if exist_flag == False :
                                    edges.append({"n1": device,
                                        "i1": local_intf_name,
                                        "n2": remote_host_name,
                                        "i2": remote_intf_name,})

                                if not (edges) :
                                    edges.append({"n1": device,
                                        "i1": local_intf_name,
                                        "n2": remote_host_name,
                                        "i2": remote_intf_name,})
                    ##logger.info(self.interfaces[device])
                    ##logger.debug("Processing completed for: " + str(device))

                    ##logger.info(self.interfaces[device])

            if self.devices[device].attributes.internal.get("device_type")=="NX-OS":
                ##logger.info('Inside nexus')
                regex=re.compile(arp_regex['NXOS'])
                n_arp=[]
                mac_regex=re.compile('([0-9a-f]{4}\.[0-9a-f]{4}\.[0-9a-f]{4})|(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})')

                if vrfs == []:

                    vrfs = ["Global"]
                if "All" in vrfs:
                    vrfs.append("Global")

                    ##logger.info("Fetching VRF data")
                    show_vrf_1 = self.devices.exec("show vrf").wait()

                    show_vrf = dict()

                    for k, v in show_vrf_1.result.items():

                        show_vrf[k] = v["show vrf"]

                if "All" in vrfs:
                    start_parse = False

                    for line in show_vrf[device].data.split("\n"):
                        if "Name" in line:
                            start_parse = True
                            continue

                        if start_parse:
                            try:
                                vrfs.append(line.strip().split(" ")[0])
                            except:
                                continue

                        vrfs = list(set(vrfs))

                if ("Global" in vrfs) or ("All" in vrfs):
                    ##logger.debug("Fetching CDP for device " + str(device) + " for Global")
                    arp = self.devices[device].exec("show cdp neighbor").wait().result.data.split("\n")
                    start_parse = False
                    for line in arp:
                        if "Device-ID" in line:
                            start_parse = True
                        if start_parse:
                            match = regex.match(line)
                            local_intf_name = ""
                            remote_intf_name = ""
                            local_host_name = ""
                            remote_host_name =""
                            if match:
                                #logger.info(line)
                                local_intf_name = match.group('local_interface')

                                remote_intf_name = match.group('port_id')
                                local_host_name = device
                                remote_host_name = match.group('device_id')[:len(match.group('device_id'))-10]
                                exist_flag = False
                                for ele in edges :
                                    if ((((ele['n1'] == device) and (ele['n2'] == remote_host_name)) and (ele['i1'].replace(" ","") == local_intf_name.replace(" ","")) and (ele['i2'].replace(" ","") == remote_intf_name).replace(" ","")) or (((ele['n1'] == remote_host_name) and (ele['n2'] == device)) and ((ele['i1'].replace(" ","") == remote_intf_name.replace(" ","")) and (ele['i2'].replace(" ","") == local_intf_name.replace(" ",""))))) :
                                        exist_flag = True
                                        break
                                
                                if exist_flag == False :
                                    edges.append({"n1": device,
                                        "i1": local_intf_name,
                                        "n2": remote_host_name,
                                        "i2": remote_intf_name,})

                                if not (edges) :
                                    edges.append({"n1": device,
                                        "i1": local_intf_name,
                                        "n2": remote_host_name,
                                        "i2": remote_intf_name,})
                    ##logger.info(n_arp)






                    ##logger.info(self.interfaces[device])

                    for line in arp:
                        if start_parse:
                            match=regex.match(line)
                            if match:

                                intf_name=match.group(4)
                                intf_mac=match.group(3)
                                intf_addr=match.group(1)
                                if intf_name in self.interfaces[device]:

                                    self.interfaces[device][intf_name]["neighbors"].append((intf_addr,intf_mac))
                    ##logger.info(self.interfaces[device])

        logger.info("Data Fetch Complete.")
        self._data_fetched = True
        logger.debug("*******************FINAL FINAL**********************")
        logger.debug("*******************FINAL FINAL**********************")
        logger.debug("*******************FINAL FINAL**********************")
        logger.debug("*******************FINAL FINAL**********************")
        logger.debug("*******************FINAL FINAL**********************")
        return {"nodes": nodes, "edges": edges}












    def draw_topology(self, render: bool=True, pdf: bool=False, filename: str="",  include_ip_address: bool=True, multiaccess: bool=True) -> dict:

        """
        Fetches the outputs, parses them and generates L3 topology.

        :param render: (Optional) (Default: True) True if topology needs to be rendered
        :param render: (Optional) (Default: False) False if topology needs to be rendered as a PDF
        :param filename: (Optional) (Default: Autogenerated) Manually specify PDF filename
        :param include_ip_address: (Optional) (Default: True) Include IP address as label on Links in rendered topology (only in PDF)
        :param multiaccess: (Optional) (Default: True) True if multicaccess networks are to be rendered

        :return: Dictionary object containg nodes and edges of the topology
        """

        if not self._data_fetched:
            ##logger.info("Data not yet fetched. Use 'fetch()' before calling 'draw_topology()'")
            return {"error": "Data not yet fetched. Use 'fetch()' before calling 'draw_topology()'"}

        nodes = list()
        edges = list()

        for device in self.devices:
            nodes.append(device)

        # Create Switches

        switches = dict()
        switch_rev = dict()

        switch_id = 0

        for device in self.devices:
            for intf_name, interface in self.interfaces[device].items():

                #Find if Switch has already been created or create a switch

                switch = ""

                if (interface["ip_add"], interface["mac_add"]) in switch_rev:
                    switch = switch_rev[(interface["ip_add"],interface["mac_add"])]
                else:
                    for neighbor in interface["neighbors"]:
                        if neighbor in switch_rev:
                            switch = switch_rev[neighbor]
                            break

                if switch == "":
                    switch_id += 1
                    switch = "switch" + str(switch_id)
                    switches[switch] = list()

                # Update Switch

                switch_rev[(interface["ip_add"], interface["mac_add"])] = switch

                for neighbor in interface["neighbors"]:
                    switch_rev[neighbor] = switch

                switches[switch].append({"n": device,
                                      "i": intf_name,
                                      "ip": interface["ip_add"],
                                      "mac": interface["mac_add"],
                                      "vrf": interface["vrf"]})


        #Add edges

        unknown_id = 0
        switch_id = 0

        for switch, links in switches.items():

            if len(links) == 0:
                continue

            elif len(links) == 1:
                unknown_id += 1
                nodes.append("Unknown_" + str(unknown_id))

                edges.append({"n1": links[0]["n"],
                              "i1": links[0]["i"],
                              "n2": "Unknown_" + str(unknown_id),
                              "i2": "",
                              })

            elif len(links) ==2:
                edges.append({"n1": links[0]["n"],
                              "i1": links[0]["i"],
                              "n2": links[1]["n"],
                              "i2": links[1]["i"],
                              })
            else:
                switch_id += 1
                nodes.append("Switch_" + str(switch_id))

                for link in links:
                    edges.append({"n1": link["n"],
                                  "i1": link["i"],
                                  "n2": "Switch_" + str(switch_id),
                                  "i2": "",
                                  })

        if render:

            if not pdf:

                topology = ""

                intf_regex = re.compile(r"([a-zA-Z]*)(\S+)")

                for edge in edges:

                    if not multiaccess:
                        if edge["n2"].startswith("Switch_"):
                            continue

                    match = intf_regex.match(edge["i1"])
                    if match:
                        i1 = match.group(1)[0:4] + match.group(2)
                    else:
                        i1 = edge["i1"][0:4]

                    match = intf_regex.match(edge["i2"])
                    if match:
                        i2 = match.group(1)[0:4] + match.group(2)
                    else:
                        i2 = edge["i2"][0:4]

                    if edge["n2"].startswith("Switch_"):
                        topology += "[Router {n1}]:{label1} --- {label2}:[mulitswitch_device {n2}]\n".format(
                            n1=edge["n1"], label1=i1, label2=i2, n2=edge["n2"])
                    else:
                        topology += "[Router {n1}]:{label1} --- {label2}:[Router {n2}]\n".format(
                            n1=edge["n1"], label1=i1, label2=i2, n2=edge["n2"])

                topology = urllib.parse.quote(topology)

                webbrowser.open("http://www-tac.cisco.com:81/archer/?txt={topology}".format(topology=topology))

            else:

                dot = Graph(comment='L3 Topology')

                for node in nodes:
                    if str(node).startswith("Switch_"):
                        if multiaccess:
                            dot.node(node, node, color='#AED6F1', shape="box", style="filled")
                    elif str(node).startswith("Unknown_"):
                        dot.node(node, "", color="#EC7063", shape="point")
                    else:
                        dot.node(node, node, color='#abebc6', style="filled")

                intf_regex = re.compile(r"([a-zA-Z]*)(\S+)")

                for edge in edges:

                    if not multiaccess:
                        if edge["n2"].startswith("Switch_"):
                            continue

                    i1 = ""
                    i2 = ""

                    match = intf_regex.match(edge["i1"])
                    if match:
                        i1 = match.group(1)[0:4] + match.group(2)
                    else:
                        i1 = edge["i1"][0:4]

                    match = intf_regex.match(edge["i2"])
                    if match:
                        i2 = match.group(1)[0:4] + match.group(2)
                    else:
                        i2 = edge["i2"][0:4]

                    if include_ip_address:
                        if i2.strip() != "":
                            label = edge["n1"] + "/" + i1 + "(" + edge["ip1"] + ")" + " <> " + edge["n2"] + "/" + i2 + "(" + edge["ip2"] + ")"
                        else:
                            label = edge["n1"] + "/" + i1 + "(" + edge["ip1"] + ")"
                    else:
                        if i2.strip() != "":
                            label = edge["n1"] + "/" + i1 + " <> " + edge["n2"] + "/" + i2
                        else:
                            label = edge["n1"] + "/" + i1

                    dot.edge(edge["n1"],
                             edge["n2"],
                             label=label,
                             color='#EB984E')

                if filename.strip() == "":
                    filename= 'l3_topology_' + str(datetime.now())

                dot.render(filename, view=True)


        return {"nodes": nodes, "edges": edges}
