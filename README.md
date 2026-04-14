# CN Lab: Static Routing using SDN Controller

##  Description
This project demonstrates static routing using a Software Defined Network (SDN) controller.  
Mininet is used to create the network topology, and the Ryu controller installs static flow rules to forward packets between hosts.

---

##  Platform & Versions

- Operating System: Ubuntu 22.04
- Programming Language: Python 3.9
- SDN Controller: Ryu 4.34
- Network Emulator: Mininet 2.3
- OpenFlow Version: 1.3
- Switch: Open vSwitch

---

##  Network Topology
### IP Addresses
- h1 → 10.0.0.1/24  
- h2 → 10.0.0.2/24  

---

##  Project Files

- `topology.py` → Defines Mininet topology  
- `static_routing.py` → Ryu controller logic  
- `README.md` → Project documentation  

---

##  Terminal Usage

- Terminal 1 → Run Ryu Controller  
- Terminal 2 → Run Mininet  
- Terminal 3 → Flow table & testing  

---

##  Execution Steps

### Step 1: Start Controller (Terminal 1)

```bash
source ~/ryuenv39/bin/activate
cd ~/sdn_static_575
ryu-manager --ofp-tcp-listen-port 6633 static_routing.py

### Step 2: Start Mininet (Terminal 2)

cd ~/sdn_static_575
sudo mn -c
sudo mn --custom topology.py --topo staticroutetopo --controller remote,ip=127.0.0.1,port=6633 --switch ovsk,protocols=OpenFlow13

### Step 3: Verify Network (Terminal 2)

nodes
net

### Step 4: Connectivity Test
pingall

### Step 5: Direct Ping
h1 ping -c 4 h2

### Step 6: Throughput Test

h2 iperf -s &
h1 iperf -c 10.0.0.2

### Step 7: Flow Table Check (Terminal 3)

sudo ovs-ofctl -O OpenFlow13 dump-flows s1
sudo ovs-ofctl -O OpenFlow13 dump-flows s2
sudo ovs-ofctl -O OpenFlow13 dump-flows s3

### Step 8: Failure Test

sudo ovs-ofctl -O OpenFlow13 del-flows s1
sudo ovs-ofctl -O OpenFlow13 del-flows s2
sudo ovs-ofctl -O OpenFlow13 del-flows s3

### Then:
h1 ping -c 4 h2

### Step 9: Recovery Test
Ctrl + C

### Then:
ryu-manager --ofp-tcp-listen-port 6633 static_routing.py

### Then:
h1 ping -c 4 h2
