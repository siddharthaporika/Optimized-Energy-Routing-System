# ============================================================
# ENERGY-EFFICIENT ROUTING IN WIRELESS SENSOR NETWORKS (WSN)
# ============================================================
#
# Project Type:
# Optimization-Based Energy Efficient Routing Simulation
#
# Features:
# ✔ Multi-Hop Routing
# ✔ Energy-Aware Routing
# ✔ Residual Energy Tracking
# ✔ Node Failure Simulation
# ✔ Dynamic Routing
# ✔ Network Lifetime Analysis
# ✔ Throughput Tracking
# ✔ LP-inspired Energy Optimization Logic
# ✔ Realistic Graphs
#
# ============================================================

import random
import math
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

# ============================================================
# PARAMETERS
# ============================================================

NUM_NODES = 50
AREA_SIZE = 100

INITIAL_ENERGY = 2.0        # Joules
PACKET_SIZE = 4000          # bits

E_ELEC = 50e-9              # Energy for transmitter/receiver
E_AMP = 100e-12             # Amplifier energy

MAX_ROUNDS = 1000

BASE_STATION = (50, 120)

TRANSMISSION_RANGE = 35

# ============================================================
# SENSOR NODE CLASS
# ============================================================

class SensorNode:

    def __init__(self, node_id, x, y):

        self.id = node_id
        self.x = x
        self.y = y

        self.energy = INITIAL_ENERGY

        self.alive = True

    def distance(self, other_x, other_y):

        return math.sqrt(
            (self.x - other_x) ** 2 +
            (self.y - other_y) ** 2
        )

# ============================================================
# CREATE SENSOR NODES
# ============================================================

nodes = []

for i in range(NUM_NODES):

    x = random.uniform(0, AREA_SIZE)
    y = random.uniform(0, AREA_SIZE)

    nodes.append(SensorNode(i, x, y))

# ============================================================
# ENERGY MODEL
# ============================================================

def transmission_energy(distance):

    return (
        (E_ELEC * PACKET_SIZE) +
        (E_AMP * PACKET_SIZE * (distance ** 2))
    )

# ============================================================
# FIND NEIGHBORS
# ============================================================

def get_neighbors(node):

    neighbors = []

    for other in nodes:

        if other.id != node.id and other.alive:

            d = node.distance(other.x, other.y)

            if d <= TRANSMISSION_RANGE:

                neighbors.append(other)

    return neighbors

# ============================================================
# ENERGY-AWARE ROUTING
# ============================================================

def choose_next_hop(current):

    neighbors = get_neighbors(current)

    if len(neighbors) == 0:
        return None

    best_neighbor = None
    best_score = float('inf')

    for neighbor in neighbors:

        # Distance to base station
        d_to_sink = neighbor.distance(
            BASE_STATION[0],
            BASE_STATION[1]
        )

        # Lower score is better
        score = (
            d_to_sink /
            (neighbor.energy + 0.0001)
        )

        if score < best_score:

            best_score = score
            best_neighbor = neighbor

    return best_neighbor

# ============================================================
# METRICS
# ============================================================

alive_nodes_history = []
energy_history = []
throughput_history = []

FND = None
HND = None
LND = None

packets_delivered = 0

# ============================================================
# MAIN SIMULATION
# ============================================================

for round_num in range(MAX_ROUNDS):

    round_packets = 0

    # --------------------------------------------------------
    # EACH NODE SENDS DATA
    # --------------------------------------------------------

    for node in nodes:

        if not node.alive:
            continue

        current = node

        visited = set()

        while True:

            if current.id in visited:
                break

            visited.add(current.id)

            # Direct distance to sink
            d_sink = current.distance(
                BASE_STATION[0],
                BASE_STATION[1]
            )

            # If close enough, send directly
            if d_sink <= TRANSMISSION_RANGE:

                energy_needed = transmission_energy(d_sink)

                current.energy -= energy_needed

                if current.energy <= 0:

                    current.energy = 0
                    current.alive = False

                else:
                    packets_delivered += 1
                    round_packets += 1

                break

            # Otherwise use multi-hop routing
            next_hop = choose_next_hop(current)

            if next_hop is None:
                break

            d = current.distance(
                next_hop.x,
                next_hop.y
            )

            energy_needed = transmission_energy(d)

            current.energy -= energy_needed

            # Receiver energy
            next_hop.energy -= (E_ELEC * PACKET_SIZE)

            # Node death checks
            if current.energy <= 0:

                current.energy = 0
                current.alive = False
                break

            if next_hop.energy <= 0:

                next_hop.energy = 0
                next_hop.alive = False
                break

            current = next_hop

    # --------------------------------------------------------
    # TRACK METRICS
    # --------------------------------------------------------

    alive_nodes = sum(
        1 for n in nodes if n.alive
    )

    total_energy = sum(
        n.energy for n in nodes
    )

    alive_nodes_history.append(alive_nodes)

    energy_history.append(total_energy)

    throughput_history.append(packets_delivered)

    # --------------------------------------------------------
    # LIFETIME METRICS
    # --------------------------------------------------------

    if FND is None and alive_nodes < NUM_NODES:
        FND = round_num

    if HND is None and alive_nodes <= NUM_NODES / 2:
        HND = round_num

    if alive_nodes == 0:
        LND = round_num
        print("\nAll nodes dead.")
        break

    # --------------------------------------------------------
    # PRINT STATUS
    # --------------------------------------------------------

    if round_num % 50 == 0:

        print(
            f"Round {round_num} | "
            f"Alive Nodes: {alive_nodes} | "
            f"Energy: {total_energy:.2f}"
        )

# ============================================================
# PRINT FINAL RESULTS
# ============================================================

print("\n==============================")
print("SIMULATION RESULTS")
print("==============================")

print(f"First Node Dead (FND): {FND}")
print(f"Half Nodes Dead (HND): {HND}")
print(f"Last Node Dead (LND): {LND}")

print(f"Packets Delivered: {packets_delivered}")

# ============================================================
# NETWORK VISUALIZATION
# ============================================================

G = nx.Graph()

for node in nodes:

    color = 'green' if node.alive else 'red'

    G.add_node(
        node.id,
        pos=(node.x, node.y),
        color=color
    )

# Add edges
for node in nodes:

    if node.alive:

        neighbors = get_neighbors(node)

        for neighbor in neighbors:

            G.add_edge(node.id, neighbor.id)

pos = nx.get_node_attributes(G, 'pos')

colors = [
    G.nodes[n]['color']
    for n in G.nodes()
]

plt.figure(figsize=(10, 8))

nx.draw(
    G,
    pos,
    node_color=colors,
    with_labels=True,
    node_size=500
)

# Base station
plt.scatter(
    BASE_STATION[0],
    BASE_STATION[1],
    color='blue',
    s=500,
    marker='s',
    label='Base Station'
)

plt.title("Wireless Sensor Network Topology")
plt.legend()
plt.grid(True)

plt.show()

# ============================================================
# GRAPH 1: ALIVE NODES
# ============================================================

plt.figure(figsize=(10, 5))

plt.plot(
    alive_nodes_history,
    linewidth=2
)

plt.xlabel("Rounds")
plt.ylabel("Alive Nodes")

plt.title("Network Lifetime Analysis")

plt.grid(True)

plt.show()

# ============================================================
# GRAPH 2: RESIDUAL ENERGY
# ============================================================

plt.figure(figsize=(10, 5))

plt.plot(
    energy_history,
    linewidth=2
)

plt.xlabel("Rounds")
plt.ylabel("Residual Energy (J)")

plt.title("Residual Energy Analysis")

plt.grid(True)

plt.show()

# ============================================================
# GRAPH 3: THROUGHPUT
# ============================================================

plt.figure(figsize=(10, 5))

plt.plot(
    throughput_history,
    linewidth=2
)

plt.xlabel("Rounds")
plt.ylabel("Packets Delivered")

plt.title("Network Throughput")

plt.grid(True)

plt.show()