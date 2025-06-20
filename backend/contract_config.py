"""
SafetyVault Contract Configuration
Updated to use official Blend Protocol contracts and proper configuration
"""
from config import (
    SAFETY_VAULT_CONTRACT_ID,
    SAFETY_VAULT_WASM_HASH,
    DEPLOYER_ADDRESS,
    BLEND_CONTRACTS,
    TOKEN_CONTRACTS,
    CONTRACT_METADATA,
    get_network_config
)

def get_contract_id() -> str:
    """Get the SafetyVault contract ID"""
    return SAFETY_VAULT_CONTRACT_ID

def get_contract_info() -> dict:
    """Get complete SafetyVault contract information"""
    return CONTRACT_METADATA["safety_vault"]

def get_deployer_address() -> str:
    """Get the deployer account address"""
    return DEPLOYER_ADDRESS

def get_network_info() -> dict:
    """Get network configuration"""
    return get_network_config()

def get_blend_pool_contract() -> str:
    """Get the official Blend Protocol pool contract address"""
    return BLEND_CONTRACTS["TESTNET_POOL_V2"]

def get_blend_backstop_contract() -> str:
    """Get the official Blend Protocol backstop contract address"""
    return BLEND_CONTRACTS["BACKSTOP_V2"]

def get_token_contract(token_symbol: str) -> str:
    """Get token contract address by symbol"""
    return TOKEN_CONTRACTS.get(token_symbol.upper(), "")

def get_all_contracts() -> dict:
    """Get all contract addresses for integration"""
    return {
        "safety_vault": SAFETY_VAULT_CONTRACT_ID,
        "blend_pool": get_blend_pool_contract(),
        "blend_backstop": get_blend_backstop_contract(),
        "blend_emitter": BLEND_CONTRACTS["EMITTER"],
        "blend_factory": BLEND_CONTRACTS["POOL_FACTORY_V2"],
        "oracle": BLEND_CONTRACTS["ORACLE_MOCK"],
        "tokens": TOKEN_CONTRACTS
    } 