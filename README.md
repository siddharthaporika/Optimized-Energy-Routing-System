# Energy-Efficient Multi-Hop Routing in Wireless Sensor Networks (WSN)

## Overview

This project presents a Python-based simulation of an **Energy-Efficient Multi-Hop Routing Protocol** for **Wireless Sensor Networks (WSNs)**. The simulation models a network of sensor nodes that communicate with a base station while minimizing energy consumption and extending the overall network lifetime.

The routing algorithm selects the next forwarding node based on **transmission energy cost** and **residual node energy**, enabling energy-aware communication and balanced energy utilization across the network.

The project also evaluates important WSN performance metrics such as network lifetime, residual energy, throughput, and node failures.

---

## Features

* Energy-aware multi-hop routing
* Dynamic next-hop selection
* Wireless sensor network simulation
* Realistic first-order radio energy model
* Residual energy tracking
* Node failure simulation
* Network lifetime analysis
* Throughput analysis
* Network topology visualization
* Performance graphs

---

## Technologies Used

* Python 3
* Matplotlib
* NetworkX
* Random
* Math

---

## Project Structure

```
Energy-Efficient-Routing-WSN/
│
├── wsn_simulation.py
├── README.md
├── requirements.txt
├── graphs/
│   ├── network_topology.png
│   ├── alive_nodes.png
│   ├── residual_energy.png
│   └── throughput.png
├── report.pdf
└── presentation.pptx
```

---

## Simulation Parameters

| Parameter              |           Value |
| ---------------------- | --------------: |
| Number of Sensor Nodes |              40 |
| Simulation Area        | 100 × 100 units |
| Initial Energy         |           3.0 J |
| Base Station           |        (50,120) |
| Maximum Rounds         |             500 |
| Transmission Range     |        40 units |
| Packet Size            |       4000 bits |

---

## Energy Model

The simulation uses the **First-Order Radio Energy Model**, where the transmission energy depends on the communication distance.

For short-distance communication:

```
Etx = Eelec × k + Eamp × k × d²
```

For long-distance communication:

```
Etx = Eelec × k + Eamp × k × d⁴
```

where:

* **Eelec** = Electronic energy
* **Eamp** = Amplifier energy
* **k** = Packet size
* **d** = Transmission distance

This model closely represents the energy consumption behavior of practical wireless sensor networks.

---

## Routing Algorithm

For every transmission:

1. Generate active sensor nodes.
2. Identify neighboring nodes within the transmission range.
3. Compute the transmission energy cost.
4. Evaluate the residual energy of neighboring nodes.
5. Select the next hop with the lowest routing score.
6. Forward the packet using multi-hop communication.
7. Update the energy of transmitting and receiving nodes.
8. Mark nodes as dead when their energy becomes zero.
9. Repeat for all simulation rounds.

---

## Performance Metrics

The simulator evaluates the following performance metrics:

### Network Lifetime

* **FND (First Node Dead)** – Round when the first sensor node dies.
* **HND (Half Nodes Dead)** – Round when half of the sensor nodes are dead.
* **LND (Last Node Dead)** – Round when all sensor nodes become inactive.

---

### Residual Energy

Tracks the total remaining energy of the network after every simulation round.

---

### Throughput

Measures the cumulative number of packets successfully delivered to the base station.

---

### Alive Nodes

Shows the number of active sensor nodes during the simulation and illustrates the degradation of the network over time.

---

## Output

The simulation generates:

* Wireless Sensor Network topology
* Alive Nodes vs Rounds graph
* Residual Energy vs Rounds graph
* Throughput vs Rounds graph
* Network lifetime statistics (FND, HND, LND)

---

## Results

The simulation demonstrates that:

* Multi-hop communication reduces transmission energy.
* Energy-aware routing balances energy consumption among sensor nodes.
* Network lifetime is improved by avoiding unnecessary long-distance transmissions.
* Throughput remains high until significant node failures occur.
* Residual energy decreases gradually as packets are transmitted.

---

## Future Improvements

Possible enhancements include:

* Cluster-based routing (LEACH)
* Particle Swarm Optimization (PSO)
* Genetic Algorithm (GA)
* Ant Colony Optimization (ACO)
* Reinforcement Learning-based routing
* Mobile sink implementation
* Heterogeneous sensor networks
* Security-aware routing protocols

---

## Installation

Clone the repository:

```bash
git clone https://github.com/your-username/Energy-Efficient-Routing-WSN.git
```

Install the required packages:

```bash
pip install matplotlib networkx numpy
```

Run the simulation:

```bash
python wsn_simulation.py
```

---

## Author

**Siddhartha Porika**

Electrical Engineering
Indian Institute of Technology Indore

---

## License

This project is intended for educational and research purposes.
