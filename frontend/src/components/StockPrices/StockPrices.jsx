import React, { forwardRef, useImperativeHandle, useRef } from 'react'
import { ArrowUpRight, ArrowDownRight } from 'lucide-react'

const StockPrices = forwardRef(({ data }, ref) => {
  const pricesRef = useRef({})

  // Map securities data to our display format
  const stocks = Object.entries(data).map(([name, price]) => {
    const previousPrice = pricesRef.current[name] || price
    const change = ((price - previousPrice) / previousPrice) * 100

    // Update stored price
    pricesRef.current[name] = price

    const getEmoji = (name) => {
      const emojiMap = {
        'BANANA': '🍌',
        'ICE': '🧊',
        'PINEAPPLES': '🍍',
        'FISH': '🐟',
        'PEBBLE': '🪨'
      }
      return emojiMap[name] || '📈'
    }

    return {
      name: name.charAt(0) + name.slice(1).toLowerCase(),
      ticker: name,
      price,
      icon: getEmoji(name),
      change
    }
  })

  useImperativeHandle(ref, () => ({
    handleNewsImpact: (ticker, multiplier) => {
      console.log('News impact:', ticker, multiplier)
    }
  }), [])

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
                JC {Number(stock.price).toFixed(2)}
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
})

StockPrices.displayName = 'StockPrices'

export default StockPrices