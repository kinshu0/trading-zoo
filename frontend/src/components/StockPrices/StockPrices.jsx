import React from 'react'
import { Card, Statistic, List, Typography } from 'antd'
import { ArrowUpOutlined, ArrowDownOutlined } from '@ant-design/icons'

const { Text } = Typography

function StockPrices() {
  const stocks = [
    { 
      name: 'Bananas', 
      ticker: 'BNNA',
      price: 10.00, 
      change: +0.52,
      icon: '🍌'
    },
    { 
      name: 'Ice', 
      ticker: 'ICEE',
      price: 15.00, 
      change: -0.31,
      icon: '🧊'
    },
    { 
      name: 'Pineapples', 
      ticker: 'PINE',
      price: 20.00, 
      change: +1.25,
      icon: '🍍'
    },
    { 
      name: 'Umbrellas', 
      ticker: 'UMBR',
      price: 25.00, 
      change: -0.45,
      icon: '☂️'
    },
    { 
      name: 'Scuba Gear', 
      ticker: 'SCBA',
      price: 50.00, 
      change: +0.88,
      icon: '🤿'
    }
  ]

  return (
    <List
      grid={{ gutter: 16, column: 1 }}
      dataSource={stocks}
      renderItem={stock => (
        <List.Item>
          <Card 
            size="small" 
            className="hover:shadow-lg transition-shadow"
            bodyStyle={{ padding: '12px' }}
          >
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-3">
                <div className="text-2xl w-10 h-10 flex items-center justify-center bg-gray-100 rounded-full">
                  {stock.icon}
                </div>
                <div>
                  <div className="flex items-center gap-2">
                    <Text strong className="text-lg">{stock.name}</Text>
                    <Text type="secondary" className="text-sm">
                      ${stock.ticker}
                    </Text>
                  </div>
                  <Statistic
                    value={stock.price}
                    precision={2}
                    prefix="JC "
                    valueStyle={{
                      fontSize: '1.25rem',
                      color: stock.change >= 0 ? '#3f8600' : '#cf1322'
                    }}
                  />
                </div>
              </div>
              <div className="flex items-center">
                {stock.change >= 0 ? (
                  <ArrowUpOutlined style={{ color: '#3f8600', fontSize: '1.2rem' }} />
                ) : (
                  <ArrowDownOutlined style={{ color: '#cf1322', fontSize: '1.2rem' }} />
                )}
                <Text
                  style={{
                    color: stock.change >= 0 ? '#3f8600' : '#cf1322',
                    marginLeft: '4px',
                    fontWeight: 500
                  }}
                >
                  {Math.abs(stock.change)}%
                </Text>
              </div>
            </div>
          </Card>
        </List.Item>
      )}
    />
  )
}

export default StockPrices 