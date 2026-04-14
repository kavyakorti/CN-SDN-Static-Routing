from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_3


class StaticRouting(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    def add_flow(self, datapath, priority, match, actions):
        parser = datapath.ofproto_parser
        ofproto = datapath.ofproto

        inst = [parser.OFPInstructionActions(
            ofproto.OFPIT_APPLY_ACTIONS, actions)]

        mod = parser.OFPFlowMod(
            datapath=datapath,
            priority=priority,
            match=match,
            instructions=inst
        )
        datapath.send_msg(mod)

    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def switch_features_handler(self, ev):
        datapath = ev.msg.datapath
        parser = datapath.ofproto_parser
        ofproto = datapath.ofproto
        dpid = datapath.id

        # Default rule: send unknown packets to controller
        match = parser.OFPMatch()
        actions = [parser.OFPActionOutput(ofproto.OFPP_CONTROLLER)]
        self.add_flow(datapath, 0, match, actions)

        # Static routing rules
        # Topology:
        # h1 -- s1 -- s2 -- s3 -- h2
        #
        # Port map:
        # s1: port1-h1, port2-s2
        # s2: port1-s1, port2-s3
        # s3: port1-s2, port2-h2

        if dpid == 1:
            # h1 -> h2
            self.add_flow(datapath, 10,
                parser.OFPMatch(eth_type=0x0800, ipv4_dst='10.0.0.2'),
                [parser.OFPActionOutput(2)])

            # h2 -> h1
            self.add_flow(datapath, 10,
                parser.OFPMatch(eth_type=0x0800, ipv4_dst='10.0.0.1'),
                [parser.OFPActionOutput(1)])

            # ARP
            self.add_flow(datapath, 10,
                parser.OFPMatch(eth_type=0x0806),
                [parser.OFPActionOutput(ofproto.OFPP_FLOOD)])

        elif dpid == 2:
            # h1 -> h2
            self.add_flow(datapath, 10,
                parser.OFPMatch(eth_type=0x0800, ipv4_dst='10.0.0.2'),
                [parser.OFPActionOutput(2)])

            # h2 -> h1
            self.add_flow(datapath, 10,
                parser.OFPMatch(eth_type=0x0800, ipv4_dst='10.0.0.1'),
                [parser.OFPActionOutput(1)])

            # ARP
            self.add_flow(datapath, 10,
                parser.OFPMatch(eth_type=0x0806),
                [parser.OFPActionOutput(ofproto.OFPP_FLOOD)])

        elif dpid == 3:
            # h1 -> h2
            self.add_flow(datapath, 10,
                parser.OFPMatch(eth_type=0x0800, ipv4_dst='10.0.0.2'),
                [parser.OFPActionOutput(2)])

            # h2 -> h1
            self.add_flow(datapath, 10,
                parser.OFPMatch(eth_type=0x0800, ipv4_dst='10.0.0.1'),
                [parser.OFPActionOutput(1)])

            # ARP
            self.add_flow(datapath, 10,
                parser.OFPMatch(eth_type=0x0806),
                [parser.OFPActionOutput(ofproto.OFPP_FLOOD)])

        print("Rules installed on switch", dpid)
