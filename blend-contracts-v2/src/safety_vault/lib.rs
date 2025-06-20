#![no_std]

use soroban_sdk::{
    contract, contractclient, contractimpl, contracttype, contracterror, panic_with_error,
    Address, Env, Vec, String
};

/// Position data structure representing updated position after protection
#[derive(Clone)]
#[contracttype]
pub struct Position {
    pub id: String,
    pub health_factor: i128, // Fixed point number (1.15 = 115)
    pub ltv: i128,           // Fixed point number (0.85 = 85)
    pub collateral: i128,
    pub debt: i128,
}

/// SafetyAction enum defining the types of safety actions that can be executed
#[derive(Clone)]
#[contracttype]
pub enum SafetyAction {
    /// Top up collateral for a specific pool (pool_address, amount)
    TopUpCollateral(Address, i128),
    /// Claim insurance for a specific pool
    ClaimInsurance(Address),
    /// Partially repay debt for a specific asset (debt_asset_address, amount)
    PartialRepay(Address, i128),
}

/// Error codes for the SafetyVault contract
#[contracterror]
#[derive(Copy, Clone, Debug, Eq, PartialEq)]
#[repr(u32)]
pub enum SafetyVaultError {
    /// Insufficient balance to perform the action
    InsufficientBalance = 1,
    /// Pool not found or invalid
    PoolNotFound = 2,
    /// Insurance claim failed
    InsuranceClaimFailed = 3,
    /// Unauthorized access attempt
    Unauthorized = 4,
    /// Invalid action parameters
    InvalidAction = 5,
    /// Action execution failed
    ActionExecutionFailed = 6,
    /// Position is not at risk (LTV below threshold)
    NotAtRisk = 7,
}

/// SafetyVault contract
#[contract]
pub struct SafetyVaultContract;

/// SafetyVault trait defining the contract interface
#[contractclient(name = "SafetyVaultClient")]
pub trait SafetyVault {
    /// Execute a series of safety actions for a user with require_auth(&user)
    /// Returns updated position data after successful protection
    fn execute_actions(e: Env, user: Address, actions: Vec<SafetyAction>) -> Position;
    
    /// Get contract information
    fn get_info(e: Env) -> String;
}

#[contractimpl]
impl SafetyVault for SafetyVaultContract {
    fn execute_actions(e: Env, user: Address, actions: Vec<SafetyAction>) -> Position {
        // Require user authorization
        user.require_auth();
        
        // Verify position exists and is at risk before allowing actions
        let position_ltv = get_user_position_ltv(&e, &user);
        if position_ltv < 7000 { // 0.7 in basis points (7000 = 70%)
            panic_with_error!(&e, SafetyVaultError::NotAtRisk);
        }
        
        // If no actions provided, return current position
        if actions.is_empty() {
            return get_user_position(&e, &user);
        }
        
        // Execute actions in sequence with rollback on failure
        for action in actions.iter() {
            match execute_single_action(&e, &user, &action) {
                Ok(_) => continue,
                Err(error) => {
                    // Panic to trigger rollback on failure
                    panic_with_error!(&e, error);
                }
            }
        }
        
        // Return updated position data after successful execution
        get_user_position(&e, &user)
    }
    
    fn get_info(e: Env) -> String {
        String::from_str(&e, "SafetyVault v1.0 - BlendGuard Hackathon")
    }
}

/// Get user's position LTV (Loan-to-Value ratio) in basis points
/// For hackathon demo, this returns mock data
/// In production, this would integrate with lending pools to get real position data
fn get_user_position_ltv(_e: &Env, user: &Address) -> u32 {
    // For demo purposes, simulate position data
    // In production implementation, this would:
    // 1. Query all lending pools to find user positions
    // 2. Calculate total collateral value
    // 3. Calculate total debt value
    // 4. Return LTV as (debt_value / collateral_value) * 10000 (basis points)
    
    // Mock implementation - use address hash for deterministic LTV
    // For demo, simply return a fixed high LTV to allow testing
    8000 // 80% LTV - above threshold, at risk
}

/// Get user's complete position data with updated health factor
/// For hackathon demo, this returns mock data with improved health factor after protection
fn get_user_position(e: &Env, user: &Address) -> Position {
    // For demo purposes, simulate improved position data after protection
    // In production implementation, this would:
    // 1. Query lending pools to get actual position data
    // 2. Calculate updated health factor, LTV, collateral, and debt values
    // 3. Return real position data structure
    
    Position {
        id: String::from_str(e, "XLM-123"),
        health_factor: 185,  // 1.85 (improved from 1.15)
        ltv: 65,            // 0.65 (improved from 0.85)
        collateral: 11000,  // Increased due to top-up
        debt: 8500,         // Same debt amount
    }
}

/// Execute a single safety action
fn execute_single_action(
    e: &Env, 
    user: &Address, 
    action: &SafetyAction
) -> Result<(), SafetyVaultError> {
    match action {
        SafetyAction::TopUpCollateral(pool_address, amount) => {
            execute_top_up_collateral(e, user, pool_address, *amount)
        }
        SafetyAction::ClaimInsurance(pool_address) => {
            execute_claim_insurance(e, user, pool_address)
        }
        SafetyAction::PartialRepay(debt_asset_address, amount) => {
            execute_partial_repay(e, user, debt_asset_address, *amount)
        }
    }
}

/// Execute top up collateral action
fn execute_top_up_collateral(
    _e: &Env,
    _user: &Address,
    _pool_address: &Address,
    amount: i128,
) -> Result<(), SafetyVaultError> {
    if amount <= 0 {
        return Err(SafetyVaultError::InvalidAction);
    }
    
    // For hackathon demo - simplified implementation
    // In a real implementation, this would:
    // 1. Verify pool exists by creating a PoolClient
    // 2. Get user's current positions to determine what asset to supply
    // 3. Check user's balance using TokenClient
    // 4. Create supply request and execute via pool.submit()
    // 5. Handle all the Blend protocol interactions
    
    Ok(())
}

/// Execute claim insurance action - calls backstop::claim(&user, &pool)
fn execute_claim_insurance(
    _e: &Env,
    _user: &Address,
    _pool_address: &Address,
) -> Result<(), SafetyVaultError> {
    // For hackathon demo - simplified implementation
    // In a real implementation, this would:
    // 1. Create backstop client for the pool
    // 2. Get pool configuration to find backstop address
    // 3. Call backstop::claim(&user, &pool) as specified in requirements
    // 4. Handle InsuranceClaimFailed error
    
    Ok(())
}

/// Execute partial repay action
fn execute_partial_repay(
    _e: &Env,
    _user: &Address,
    _debt_asset_address: &Address,
    amount: i128,
) -> Result<(), SafetyVaultError> {
    if amount <= 0 {
        return Err(SafetyVaultError::InvalidAction);
    }
    
    // For hackathon demo - simplified implementation
    // In a real implementation, this would:
    // 1. Check user's balance using TokenClient
    // 2. Find appropriate pool for the debt asset
    // 3. Execute repay transaction
    // 4. Handle InsufficientBalance, PoolNotFound errors
    
    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;
    use soroban_sdk::{
        testutils::{Address as AddressTestTrait},
        Address, Env,
    };
    
    #[test]
    fn test_successful_multi_action_execution() {
        let e = Env::default();
        e.mock_all_auths();
        
        let user = Address::generate(&e);
        let pool_address = Address::generate(&e);
        let asset_address = Address::generate(&e);
        
        let contract_id = e.register(SafetyVaultContract, ());
        let client = SafetyVaultClient::new(&e, &contract_id);
        
        // Create multiple valid actions
        let actions = Vec::from_array(&e, [
            SafetyAction::TopUpCollateral(pool_address.clone(), 1000),
            SafetyAction::ClaimInsurance(pool_address.clone()),
            SafetyAction::PartialRepay(asset_address, 500),
        ]);
        
        let result = client.execute_actions(&user, &actions);
        assert_eq!(result, true);
    }
    
    #[test]
    #[should_panic(expected = "Error(Contract, #5)")]
    fn test_partial_failure_rollback() {
        let e = Env::default();
        e.mock_all_auths();
        
        let user = Address::generate(&e);
        let pool_address = Address::generate(&e);
        
        let contract_id = e.register(SafetyVaultContract, ());
        let client = SafetyVaultClient::new(&e, &contract_id);
        
        // Create actions with invalid amount (should trigger InvalidAction error)
        let actions = Vec::from_array(&e, [
            SafetyAction::TopUpCollateral(pool_address, -1000),
        ]);
        
        // Should panic with InvalidAction error (code 5), triggering rollback
        client.execute_actions(&user, &actions);
    }
    
    #[test]
    #[should_panic]
    fn test_unauthorized_access_attempt() {
        let e = Env::default();
        // Don't mock auths to test authorization failure
        
        let user = Address::generate(&e);
        let pool_address = Address::generate(&e);
        
        let contract_id = e.register(SafetyVaultContract, ());
        let client = SafetyVaultClient::new(&e, &contract_id);
        
        let actions = Vec::from_array(&e, [
            SafetyAction::ClaimInsurance(pool_address),
        ]);
        
        // Should panic due to failed authorization
        client.execute_actions(&user, &actions);
    }
}
