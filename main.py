# main.py
import argparse
import random
import cProfile
import pstats
from originator import Originator
from recipient import Recipient
from network import Network
from locations import *
import config  # Import the config module

# Parse command line arguments
parser = argparse.ArgumentParser(description='Simulation setup')
parser.add_argument('--recipients', type=int, default=1000, help='Number of recipients')
parser.add_argument('--symbols', type=int, default=100, help='Number of symbols')
parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose output')
args = parser.parse_args()

# Set the global verbose flag
config.VERBOSE = args.verbose

def random_city():
    return cities[random.randint(0, len(cities) - 1)]

# Example setup
originator = Originator(random_city(), args.symbols)
recipients = [Recipient(random_city(), i+1, args.symbols) for i in range(args.recipients)]

network = Network(originator, recipients)
network.initialize()

# Simulation loop
def run_simulation():
    while network.active():
        network.tick()

        if network.tick_count % 1000 == 0:
            print(f"Tick {network.tick_count}")
        
        if network.tick_count > 30000:
            break   

cProfile.run('run_simulation()', 'output.prof')

with open('output_stats.txt', 'w') as stream:
    stats = pstats.Stats('output.prof', stream=stream)
    stats.sort_stats('cumulative')
    stats.print_stats()

# Log the number of nodes that received all symbols
completed_recipients = sum(1 for recipient in recipients if recipient.completed)
print(f"Simulation complete after {network.tick_count}ms. {completed_recipients}/{len(recipients)} recipients received all symbols.")
print(f"Total packets sent: {network.total_packets}, required: {args.recipients * args.symbols}, ratio: {network.total_packets / (args.recipients * args.symbols):.2f}")
