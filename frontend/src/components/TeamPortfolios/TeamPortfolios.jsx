import React from 'react'
import { Statistic, Tag, Typography } from 'antd'

const { Text } = Typography

function TeamPortfolios({ data }) {
  // Early return if no data
  if (!data) return null

  // Convert the data object into an array
  const teams = Object.entries(data).map(([teamName, teamData]) => {
    // Calculate total portfolio value
    const portfolioValue = teamData.portfolio.reduce((total, holding) => {
      return total + (holding.quantity * holding.price)
    }, 0)

    // Calculate total portfolio value including cash
    const totalValue = portfolioValue + teamData.balance

    // For this example, we'll use a mock change value
    // In a real app, you'd want to track historical values to calculate actual change
    const change = ((totalValue - 100) / 100) * 100 // Assuming 100 was starting balance

    return {
      name: teamName,
      value: totalValue,
      change: parseFloat(change.toFixed(1)),
      holdings: teamData.portfolio.map(holding => ({
        stock: holding.security_name,
        shares: holding.quantity
      }))
    }
  })

  return (
    <div className="divide-y divide-gray-100">
      {teams.map(team => (
        <div key={team.name} className="p-1.5">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-1.5">
              <Text strong className="text-xs capitalize">{team.name}</Text>
              <Tag 
                className="text-[0.6rem] leading-none m-0 h-3.5 flex items-center" 
                color={team.change >= 0 ? 'success' : 'error'}
              >
                {team.change >= 0 ? '+' : ''}{team.change}%
              </Tag>
            </div>
            <Statistic 
              value={team.value} 
              precision={0}
              prefix="JC"
              valueStyle={{ 
                fontSize: '0.7rem',
                color: team.change >= 0 ? '#3f8600' : '#cf1322',
                lineHeight: '1'
              }}
            />
          </div>
          <div className="flex flex-wrap gap-1 mt-1">
            {team.holdings.map(holding => (
              <div 
                key={holding.stock} 
                className="flex items-center gap-1 bg-gray-50 rounded px-1 py-0.5"
              >
                <Tag className="text-[0.6rem] leading-none m-0 h-3.5 flex items-center">
                  {holding.stock}
                </Tag>
                <Text className="text-[0.6rem]">{holding.shares}</Text>
              </div>
            ))}
          </div>
        </div>
      ))}
    </div>
  )
}

export default TeamPortfolios 