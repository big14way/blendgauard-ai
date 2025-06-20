// Single source for position data
const getPosition = (positionId) => {
  return {
    id: positionId || 'XLM-123',
    asset: 'XLM',
    collateral: 10000, // USD value
    debt: 8500,        // USD value
    ltv: 0.85,         // 85%
    healthFactor: 1.15,
    status: 'high-risk'
  }
}

module.exports = { getPosition }; 