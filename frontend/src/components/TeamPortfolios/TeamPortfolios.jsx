import React from 'react'
import { Card, Statistic, Tag, List, Typography } from 'antd'
import { ArrowUpOutlined, ArrowDownOutlined } from '@ant-design/icons'

const { Text } = Typography

function TeamPortfolios() {
  const teams = [
    {
      name: 'Penguins',
      value: 125000,
      change: 5.2,
      holdings: [
        { stock: 'BNNA', shares: 100 },
        { stock: 'COCO', shares: 150 }
      ]
    },
    {
      name: 'Monkeys',
      value: 115000,
      change: -2.1,
      holdings: [
        { stock: 'LEAF', shares: 200 },
        { stock: 'VINE', shares: 75 }
      ]
    },
    {
      name: 'Foxes',
      value: 135000,
      change: 7.5,
      holdings: [
        { stock: 'BNNA', shares: 150 },
        { stock: 'LEAF', shares: 100 }
      ]
    },
    {
      name: 'Iguanas',
      value: 118000,
      change: 1.8,
      holdings: [
        { stock: 'COCO', shares: 125 },
        { stock: 'VINE', shares: 100 }
      ]
    }
  ]

  return (
    <List
      grid={{ gutter: 16, column: 1 }}
      dataSource={teams}
      renderItem={team => (
        <List.Item>
          <Card 
            size="small"
            className="hover:shadow-lg transition-shadow"
          >
            <div className="flex items-center justify-between mb-2">
              <Text strong className="text-lg">{team.name}</Text>
              <Tag color={team.change >= 0 ? 'success' : 'error'}>
                {team.change >= 0 ? (
                  <ArrowUpOutlined />
                ) : (
                  <ArrowDownOutlined />
                )}
                {' '}
                {Math.abs(team.change)}%
              </Tag>
            </div>
            
            <Statistic 
              value={team.value} 
              precision={0}
              prefix="JC "
              valueStyle={{ 
                color: team.change >= 0 ? '#3f8600' : '#cf1322',
                fontSize: '1.5rem'
              }}
            />

            <div className="mt-3">
              <Text type="secondary" className="text-sm">Holdings:</Text>
              <List
                size="small"
                dataSource={team.holdings}
                renderItem={holding => (
                  <List.Item className="py-1 px-0">
                    <div className="flex justify-between w-full">
                      <Tag color="blue">{holding.stock}</Tag>
                      <Text>{holding.shares} shares</Text>
                    </div>
                  </List.Item>
                )}
              />
            </div>
          </Card>
        </List.Item>
      )}
    />
  )
}

export default TeamPortfolios 