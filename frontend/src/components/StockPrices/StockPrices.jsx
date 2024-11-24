import React, { useState, useEffect } from 'react'
import { ArrowUpRight, ArrowDownRight } from 'lucide-react'

function StockPrices() {
  const [stocks, setStocks] = useState([
    { name: 'Bananas', ticker: 'BNNA', price: 10.00, change: 0, icon: '🍌' },
    { name: 'Ice', ticker: 'ICEE', price: 15.00, change: 0, icon: '🧊' },
    { name: 'Pineapples', ticker: 'PINE', price: 20.00, change: 0, icon: '🍍' },
    { name: 'Fish', ticker: 'FISH', price: 25.00, change: 0, icon: '🐟' },
    { name: 'Pebbles', ticker: 'PEBB', price: 50.00, change: 0, icon: '🪨' }
  ])

  // Small random fluctuations
  useEffect(() => {
    const interval = setInterval(() => {
      setStocks(prevStocks => prevStocks.map(stock => {
        const randomChange = (Math.random() - 0.5) * 0.2 // Small random changes
        const newPrice = stock.price * (1 + randomChange)
        return {
          ...stock,
          price: newPrice,
          change: (randomChange * 100)
        }
      }))
    }, 3000)

    return () => clearInterval(interval)
  }, [])

  // Handle news impacts
  const handleNewsImpact = (ticker, multiplier) => {
    setStocks(prevStocks => prevStocks.map(stock => {
      if (stock.ticker === ticker) {
        const newPrice = stock.price * multiplier
        const percentChange = ((multiplier - 1) * 100)
        return {
          ...stock,
          price: newPrice,
          change: percentChange
        }
      }
      return stock
    }))
  }

  return (
    <div className="divide-y divide-gray-100">
      {stocks.map(stock => (
        <div key={stock.ticker} className="p-1.5">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-1.5">
              <span className="text-sm">{stock.icon}</span>
              <div>
                <div className="text-xs font-medium">{stock.name}</div>
                <div className="text-[0.6rem] text-gray-500">${stock.ticker}</div>
              </div>
            </div>
            <div className="text-right">
              <div className="text-xs tabular-nums">
                JC {stock.price.toFixed(2)}
              </div>
              <div className={`text-[0.6rem] flex items-center gap-0.5 ${
                stock.change >= 0 ? 'text-green-600' : 'text-red-600'
              }`}>
                {stock.change >= 0 ? (
                  <ArrowUpRight className="w-3 h-3" />
                ) : (
                  <ArrowDownRight className="w-3 h-3" />
                )}
                {Math.abs(stock.change).toFixed(2)}%
              </div>
            </div>
          </div>
        </div>
      ))}
    </div>
  )
}

export default StockPrices