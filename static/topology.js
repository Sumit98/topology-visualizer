

var topologyData = {
    "links": [
        {
            "id": 0,
            "source": 0,
            "srcDevice": "2911-2",
            "srcIfName": "Gig 0/1",
            "target": 7,
            "tgtDevice": "4461-3",
            "tgtIfName": "Gig 0/0/1"
        },
        {
            "id": 1,
            "source": 0,
            "srcDevice": "2911-2",
            "srcIfName": "Gig 0/2/0",
            "target": 5,
            "tgtDevice": "A9K-1",
            "tgtIfName": "Gig 0/1/0/0"
        },
        {
            "id": 2,
            "source": 1,
            "srcDevice": "2911-1",
            "srcIfName": "Gig 0/1",
            "target": 6,
            "tgtDevice": "4461-2",
            "tgtIfName": "Gig 0/0/2"
        },
        {
            "id": 3,
            "source": 1,
            "srcDevice": "2911-1",
            "srcIfName": "Gig 0/2",
            "target": 7,
            "tgtDevice": "4461-3",
            "tgtIfName": "Gig 0/0/0"
        },
        {
            "id": 4,
            "source": 1,
            "srcDevice": "2911-1",
            "srcIfName": "Gig 0/2/0",
            "target": 3,
            "tgtDevice": "4461-1",
            "tgtIfName": "Gig 0/0/0"
        },
        {
            "id": 5,
            "source": 2,
            "srcDevice": "2911-3",
            "srcIfName": "Gig 0/2",
            "target": 6,
            "tgtDevice": "4461-2",
            "tgtIfName": "Gig 0/0/3"
        },
        {
            "id": 6,
            "source": 2,
            "srcDevice": "2911-3",
            "srcIfName": "Gig 0/1",
            "target": 7,
            "tgtDevice": "4461-3",
            "tgtIfName": "Gig 0/0/2"
        },
        {
            "id": 7,
            "source": 2,
            "srcDevice": "2911-3",
            "srcIfName": "Gig 0/2/0",
            "target": 4,
            "tgtDevice": "N9K-1",
            "tgtIfName": "Eth 1/36"
        },
        {
            "id": 8,
            "source": 3,
            "srcDevice": "4461-1",
            "srcIfName": "Gig 0/0/3",
            "target": 5,
            "tgtDevice": "A9K-1",
            "tgtIfName": "Gig 0/1/0/1"
        },
        {
            "id": 9,
            "source": 4,
            "srcDevice": "N9K-1",
            "srcIfName": "Eth1/18",
            "target": 6,
            "tgtDevice": "4461-2",
            "tgtIfName": "Gig0/0/1"
        }
    ],
    "nodes": [
        {
            "icon": "router",
            "id": 0,
            "model": "CISCO2911/K9",
            "name": "2911-2",
            "primaryIP": "10.106.69.22"
        },
        {
            "icon": "router",
            "id": 1,
            "model": "CISCO2911/K9",
            "name": "2911-1",
            "primaryIP": "10.106.68.134"
        },
        {
            "icon": "router",
            "id": 2,
            "model": "CISCO2911/K9",
            "name": "2911-3",
            "primaryIP": "10.106.71.192"
        },
        {
            "icon": "router",
            "id": 3,
            "model": "ISR4461/K9",
            "name": "4461-1",
            "primaryIP": "10.106.69.231"
        },
        {
            "icon": "switch",
            "id": 4,
            "model": "Nexus9000 C9336C-FX2-E Chassis",
            "name": "N9K-1",
            "primaryIP": "10.106.71.26"
        },
        {
            "icon": "router",
            "id": 5,
            "model": "ASR9K",
            "name": "A9K-1",
            "primaryIP": "10.106.49.6"
        },
        {
            "icon": "router",
            "id": 6,
            "model": "ISR4461/K9",
            "name": "4461-2",
            "primaryIP": "10.106.69.78"
        },
        {
            "icon": "router",
            "id": 7,
            "model": "ISR4461/K9",
            "name": "4461-3",
            "primaryIP": "10.106.68.135"
        }
    ]
};