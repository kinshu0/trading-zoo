import React from 'react'
import { Statistic, Tag, List, Typography } from 'antd'

const { Text } = Typography

function TeamPortfolios() {
  const teams = [
    {
      name: 'Penguins', value: 125000, change: 5.2,
      holdings: [{ stock: 'BNNA', shares: 100 }, { stock: 'COCO', shares: 150 }]
    },
    {
      name: 'Monkeys', value: 115000, change: -2.1,
      holdings: [{ stock: 'LEAF', shares: 200 }, { stock: 'VINE', shares: 75 }]
    },
    {
      name: 'Foxes', value: 135000, change: 7.5,
      holdings: [{ stock: 'BNNA', shares: 150 }, { stock: 'LEAF', shares: 100 }]
    },
    {
      name: 'Iguanas', value: 118000, change: 1.8,
      holdings: [{ stock: 'COCO', shares: 125 }, { stock: 'VINE', shares: 100 }]
    }
  ]

  return (
    <div className="divide-y divide-gray-100">
      {teams.map(team => (
        <div key={team.name} className="p-1.5">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-1.5">
              <Text strong className="text-xs">{team.name}</Text>
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