import fileinput
import sys
import re
import json
import argparse

parser = argparse.ArgumentParser()

parser.add_argument('--config', action='store', dest='config_file',
                    default='config.json',
                    help='Configuration filename. Format: json'
                    )
parser.add_argument('--source', action='store', dest='source',
					default='tmp',
                    help='Working folder containing the base coin source'
                    )
args = parser.parse_args()

json_data=open(args.config_file)
config = json.load(json_data)
json_data.close()

paths = {}

# Make changes in src/CMakeLists.txt
paths['CMakeLists'] = args.source + "/src/CMakeLists.txt"

daemon_name_re = re.compile(r"#(set_property\(TARGET daemon PROPERTY OUTPUT_NAME) \"\S+\"\)", re.IGNORECASE)
for line in fileinput.input([paths['CMakeLists']], inplace=True):
	line = daemon_name_re.sub("\\1 \"%s\")" % config['core']['daemon_name'], line)
	# sys.stdout is redirected to the file
	sys.stdout.write(line)


# Make changes in src/cryptonote_config.h
paths['cryptonote_config'] = args.source + "/src/cryptonote_config.h"

CRYPTONOTE_NAME_re = re.compile(r"(#define\s+CRYPTONOTE_NAME)", re.IGNORECASE)
P2P_DEFAULT_PORT_re = re.compile(r"(#define\s+P2P_DEFAULT_PORT)", re.IGNORECASE)
RPC_DEFAULT_PORT_re = re.compile(r"(#define\s+RPC_DEFAULT_PORT)", re.IGNORECASE)
P2P_STAT_TRUSTED_PUB_KEY_re = re.compile(r"(#define\s+P2P_STAT_TRUSTED_PUB_KEY)(\s+\"[a-f0-9]+\")?", re.IGNORECASE)
CRYPTONOTE_PUBLIC_ADDRESS_BASE58_PREFIX_re = re.compile(r"(#define\s+CRYPTONOTE_PUBLIC_ADDRESS_BASE58_PREFIX)", re.IGNORECASE)
#UPGRADE_HEIGHT_re = re.compile(r"(const uint64_t\s+UPGRADE_HEIGHT\s*)", re.IGNORECASE)
if 'MONEY_SUPPLY' in config['core']:
	MONEY_SUPPLY_re = re.compile(r"(#define\s+MONEY_SUPPLY)", re.IGNORECASE)
if 'EMISSION_SPEED_FACTOR' in config['core']:
	EMISSION_SPEED_FACTOR_re =re.compile(r"(#define\s+EMISSION_SPEED_FACTOR)\s+\(?\d+\)?", re.IGNORECASE)
if 'DIFFICULTY_TARGET' in config['core']:
	DIFFICULTY_TARGET_re = re.compile(r"(#define\s+DIFFICULTY_TARGET)\s+\(?\d+\)?", re.IGNORECASE)
if 'COIN' in config['core']:
	COIN_re = re.compile(r"(#define COIN)", re.IGNORECASE)
if 'CRYPTONOTE_DISPLAY_DECIMAL_POINT' in config['core']:
	CRYPTONOTE_DISPLAY_DECIMAL_POINT_re = re.compile(r"(#define\s+CRYPTONOTE_DISPLAY_DECIMAL_POINT)", re.IGNORECASE)
if 'DEFAULT_FEE' in config['core']:
	MINIMUM_FEE_re = re.compile(r"(#define\s+DEFAULT_FEE)", re.IGNORECASE)
if 'DEFAULT_DUST_THRESHOLD' in config['core']:
	DEFAULT_DUST_THRESHOLD_re = re.compile(r"(#define\s+DEFAULT_DUST_THRESHOLD)", re.IGNORECASE)
if 'CRYPTONOTE_MINED_MONEY_UNLOCK_WINDOW' in config['core']:
	CRYPTONOTE_MINED_MONEY_UNLOCK_WINDOW_re = re.compile(r"(#define\s+CRYPTONOTE_MINED_MONEY_UNLOCK_WINDOW)", re.IGNORECASE)
if 'CRYPTONOTE_BLOCK_GRANTED_FULL_REWARD_ZONE' in config['core']:
	CRYPTONOTE_BLOCK_GRANTED_FULL_REWARD_ZONE_re = re.compile(r"(#define\s+CRYPTONOTE_BLOCK_GRANTED_FULL_REWARD_ZONE)\s+\(?\d+\)?", re.IGNORECASE)
if 'CRYPTONOTE_BLOCK_GRANTED_FULL_REWARD_ZONE_V1' in config['core']:
	CRYPTONOTE_BLOCK_GRANTED_FULL_REWARD_ZONE_V1_re = re.compile(r"(#define\s+CRYPTONOTE_BLOCK_GRANTED_FULL_REWARD_ZONE_V1)", re.IGNORECASE)
if 'MAX_BLOCK_SIZE_INITIAL' in config['core']:
	MAX_BLOCK_SIZE_INITIAL_re = re.compile(r"(#define\s+MAX_BLOCK_SIZE_INITIAL)", re.IGNORECASE)
if 'genesisCoinbaseTxHex' in config['core']:
        genesisCoinbaseTxHex_re = re.compile(r"(#define\s+GENESIS_COINBASE_TX_HEX)\s+\"\"\s*", re.IGNORECASE)
else:
        genesisCoinbaseTxHex_re = re.compile(r"^(#define\s+GENESIS_COINBASE_TX_HEX.*)$", re.IGNORECASE)


for line in fileinput.input([paths['cryptonote_config']], inplace=True):
	line = CRYPTONOTE_NAME_re.sub("\\1 \"%s\"" % config['core']['CRYPTONOTE_NAME'], line)
	line = P2P_DEFAULT_PORT_re.sub("\\1 %s" % config['core']['P2P_DEFAULT_PORT'], line)
	line = RPC_DEFAULT_PORT_re.sub("\\1 %s" % config['core']['RPC_DEFAULT_PORT'], line)
	line = P2P_STAT_TRUSTED_PUB_KEY_re.sub("\\1 \"%s\"" % config['core']['P2P_STAT_TRUSTED_PUB_KEY'], line)
	line = CRYPTONOTE_PUBLIC_ADDRESS_BASE58_PREFIX_re.sub("\\1 %s" % config['core']['CRYPTONOTE_PUBLIC_ADDRESS_BASE58_PREFIX'], line)
	if 'MONEY_SUPPLY' in config['core']:
		line = MONEY_SUPPLY_re.sub("\\1 %s" % config['core']['MONEY_SUPPLY'], line)
	if 'EMISSION_SPEED_FACTOR' in config['core']:
		line = EMISSION_SPEED_FACTOR_re.sub("\\1 %s" % config['core']['EMISSION_SPEED_FACTOR'], line)
	if 'DIFFICULTY_TARGET' in config['core']:
		line = DIFFICULTY_TARGET_re.sub("\\1 %s" % config['core']['DIFFICULTY_TARGET'], line)
	if 'COIN' in config['core']:
		line = COIN_re.sub("\\1 %s" % config['core']['COIN'], line)
	if 'CRYPTONOTE_DISPLAY_DECIMAL_POINT' in config['core']:
		line = CRYPTONOTE_DISPLAY_DECIMAL_POINT_re.sub("\\1 %s" % config['core']['CRYPTONOTE_DISPLAY_DECIMAL_POINT'], line)
	if 'DEFAULT_FEE' in config['core']:
		line = MINIMUM_FEE_re.sub("\\1 %s" % config['core']['DEFAULT_FEE'], line)
	if 'DEFAULT_DUST_THRESHOLD' in config['core']:
		line = DEFAULT_DUST_THRESHOLD_re.sub("\\1 %s" % config['core']['DEFAULT_DUST_THRESHOLD'], line)
	if 'CRYPTONOTE_MINED_MONEY_UNLOCK_WINDOW' in config['core']:
		line = CRYPTONOTE_MINED_MONEY_UNLOCK_WINDOW_re.sub("\\1 %s" % config['core']['CRYPTONOTE_MINED_MONEY_UNLOCK_WINDOW'], line)
	if 'CRYPTONOTE_BLOCK_GRANTED_FULL_REWARD_ZONE' in config['core']:
		line = CRYPTONOTE_BLOCK_GRANTED_FULL_REWARD_ZONE_re.sub("\\1 %s" % config['core']['CRYPTONOTE_BLOCK_GRANTED_FULL_REWARD_ZONE'], line)
	if 'CRYPTONOTE_BLOCK_GRANTED_FULL_REWARD_ZONE_V1' in config['core']:
		line = CRYPTONOTE_BLOCK_GRANTED_FULL_REWARD_ZONE_V1_re.sub("\\1 %s" % config['core']['CRYPTONOTE_BLOCK_GRANTED_FULL_REWARD_ZONE_V1'], line)
	if 'MAX_BLOCK_SIZE_INITIAL' in config['core']:
		line = MAX_BLOCK_SIZE_INITIAL_re.sub("\\1 %s" % config['core']['MAX_BLOCK_SIZE_INITIAL'], line)
	if 'UPGRADE_HEIGHT' in config['core']:
		line = UPGRADE_HEIGHT_re.sub("\\1 %s" % config['core']['UPGRADE_HEIGHT'], line)
        if 'genesisCoinbaseTxHex' in config['core']:
  	        line = genesisCoinbaseTxHex_re.sub("\\1 \"%s\"" % config['core']['genesisCoinbaseTxHex'], line)
	else:
		#line = UPGRADE_HEIGHT_re.sub("\\1 %s" % "1", line)
                line = genesisCoinbaseTxHex_re.sub("#define GENESIS_COINBASE_TX_HEX \"\"", line)

	# sys.stdout is redirected to the file
	sys.stdout.write(line)


SEED_NODES_re = re.compile(r"(const char\* const\s+SEED_NODES\[\] = {)[^;]+(};)", re.DOTALL)
CHECKPOINTS_re = re.compile(r"(const CheckpointData\s+CHECKPOINTS\[\] = {)[^;]+(};)", re.DOTALL)
cryptonote_config_file = open(paths['cryptonote_config'],'r')
cryptonote_config_content = cryptonote_config_file.read()
cryptonote_config_file.close()
cryptonote_config_content = SEED_NODES_re.sub("\\1 %s \\2" % config['core']['SEED_NODES'], cryptonote_config_content)
if 'CHECKPOINS' in config['core']:
	cryptonote_config_content = CHECKPOINTS_re.sub("\\1 %s \\2" % config['core']['CHECKPOINTS'], cryptonote_config_content)
cryptonote_config_file = open(paths['cryptonote_config'], "w")
cryptonote_config_file.write(cryptonote_config_content)
cryptonote_config_file.close()


# Make changes in src/p2p/p2p_networks.h
paths['p2p_networks'] = args.source + "/src/p2p/p2p_networks.h"

BYTECOIN_NETWORK_re = re.compile(r"(const static boost::uuids::uuid CRYPTONOTE_NETWORK =) { {[^;]+} };", re.IGNORECASE)
for line in fileinput.input(paths['p2p_networks'], inplace=True):
	line = BYTECOIN_NETWORK_re.sub("\\1 { { %s} };" % config['core']['BYTECOIN_NETWORK'], line)
	# sys.stdout is redirected to the file
	sys.stdout.write(line)

# Make changes in src/p2p/net_node.inl
paths['p2p_seeds'] = args.source + "/src/p2p/net_node.inl"
BYTECOIN_SEEDS_re = re.compile(r"(\/\/ADD_HARDCODED_SEED_NODE\([^\)]+\);)", re.IGNORECASE)
for line in fileinput.input(paths['p2p_seeds'], inplace=True):
        for seed in config['core']['SEED_NODES']:
                line = BYTECOIN_SEEDS_re.sub("\\1\n      ADD_HARDCODED_SEED_NODE(%s);" % seed, line)
	# sys.stdout is redirected to the file
	sys.stdout.write(line)

# //ADD_HARDCODED_SEED_NODE("your_seed_ip.com:8080");
