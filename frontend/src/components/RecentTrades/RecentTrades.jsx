import React, { useState, useEffect } from 'react'
import { ArrowUpRight, ArrowDownRight } from 'lucide-react'

function RecentTrades() {
  const [trades, setTrades] = useState([
    {
      id: 1, team: 'Penguins', action: 'buy',
      stock: 'BNNA', amount: 100, price: 150.25,
      timestamp: '2 min ago'
    },
    {
      id: 2, team: 'Monkeys', action: 'sell',
      stock: 'COCO', amount: 50, price: 85.75,
      timestamp: '5 min ago'
    },
    {
      id: 3, team: 'Foxes', action: 'buy',
      stock: 'LEAF', amount: 75, price: 45.30,
      timestamp: '8 min ago'
    }
  ])

  useEffect(() => {
    const interval = setInterval(() => {
      const newTrade = generateRandomTrade()
      setTrades(prev => [newTrade, ...prev.slice(0, 4)])
    }, 5000)

    return () => clearInterval(interval)
  }, [])

  const generateRandomTrade = () => {
    const teams = ['Penguins', 'Monkeys', 'Foxes', 'Iguanas']
    const stocks = ['BNNA', 'ICEE', 'PINE', 'UMBR', 'SCBA']
    const actions = ['buy', 'sell']

    return {
      id: Date.now(),
      team: teams[Math.floor(Math.random() * teams.length)],
      action: actions[Math.floor(Math.random() * actions.length)],
      stock: stocks[Math.floor(Math.random() * stocks.length)],
      amount: Math.floor(Math.random() * 100) + 10,
      price: Math.floor(Math.random() * 200) + 50,
      timestamp: 'just now'
    }
  }

  return (
    <div className="space-y-1 p-1">
      {trades.map(trade => (
        <div key={trade.id} className="bg-gray-50 rounded p-1.5 text-xs">
          <div className="flex justify-between items-center">
            <span className="font-medium">{trade.team}</span>
            <div className="flex items-center gap-0.5">
              {trade.action === 'buy' ? 
                <ArrowUpRight className="w-3 h-3 text-green-600" /> : 
                <ArrowDownRight className="w-3 h-3 text-red-600" />
              }
              <span className={trade.action === 'buy' ? 'text-green-600' : 'text-red-600'}>
                {trade.action.toUpperCase()}
              </span>
            </div>
          </div>
          <div className="text-gray-600 mt-0.5 flex justify-between">
            <span>{trade.amount} {trade.stock} @ JC{trade.price}</span>
            <span className="text-gray-400">{trade.timestamp}</span>
          </div>
        </div>
      ))}
    </div>
  )
}

export default RecentTrades