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

# Example setup
originator = Originator(get_random_location(), args.symbols)
recipients = [Recipient(get_random_location(), i+1, args.symbols) for i in range(args.recipients)]

network = Network(originator, recipients)
network.initialize()

# Simulation loop
def run_simulation():
    while network.active():
        network.tick()

        if network.tick_count % 1000 == 0:
            completed_recipients = sum(1 for recipient in recipients if recipient.completed)
            print(f"{network.tick_count/1000}s: {completed_recipients}/{len(recipients)} {len(network.codewords_in_transit)}")
        
# cProfile.run('run_simulation()', 'output.prof')

# with open('output_stats.txt', 'w') as stream:
#     stats = pstats.Stats('output.prof', stream=stream)
#     stats.sort_stats('cumulative')
#     stats.print_stats()

run_simulation()

# Log the number of nodes that received all symbols
completed_recipients = sum(1 for recipient in recipients if recipient.completed)
print(f"Simulation complete: {network.tick_count/1000}s. {completed_recipients}/{len(recipients)} recipients received all symbols.")
print(f"Total codewords sent: {network.total_codewords}, required: {args.recipients * args.symbols}, ratio: {network.total_codewords / (args.recipients * args.symbols):.2f}")
print(f"Codewords from originator: {originator.codeword_index}, ratio: {originator.codeword_index / args.symbols:.2f}")
