import React, { useState, useEffect } from 'react'
import { ArrowUpRight, ArrowDownRight } from 'lucide-react'
import api from '../../services/api'

function RecentTrades() {
  const [trades, setTrades] = useState([])

  const fetchTrades = async () => {
    try {
      const response = await api.get('/completed_transactions')
      if (response.data) {
        const formattedTrades = response.data.map(trade => ({
          id: `${trade.timestamp}-${trade.buyer}-${trade.seller}`,
          buyerTeam: trade.buyer,
          sellerTeam: trade.seller,
          stock: trade.security,
          amount: trade.quantity,
          price: trade.price,
          timestamp: new Date(trade.timestamp * 1000).toLocaleTimeString()
        }))
        setTrades(formattedTrades.slice(-4).reverse()) // Keep last 5 trades
      }
    } catch (error) {
      console.error('Failed to fetch trades:', error)
    }
  }

  useEffect(() => {
    fetchTrades()
    const interval = setInterval(fetchTrades, 2000)
    return () => clearInterval(interval)
  }, [])

  return (
    <div className="space-y-1 p-1">
      {trades.map(trade => (
        <div key={trade.id} className="bg-gray-50 rounded p-1.5 text-xs">
          {/* Buyer's trade */}
          <div className="flex justify-between items-center mb-0.5">
            <span className="font-medium">{trade.buyerTeam}</span>
            <div className="flex items-center gap-0.5">
              <ArrowUpRight className="w-3 h-3 text-green-600" />
              <span className="text-green-600">BUY</span>
            </div>
          </div>
          {/* Seller's trade */}
          <div className="flex justify-between items-center">
            <span className="font-medium">{trade.sellerTeam}</span>
            <div className="flex items-center gap-0.5">
              <ArrowDownRight className="w-3 h-3 text-red-600" />
              <span className="text-red-600">SELL</span>
            </div>
          </div>
          <div className="text-gray-600 mt-0.5 flex justify-between">
            <span>{trade.amount} {trade.stock} @ JC{trade.price.toFixed(2)}</span>
            <span className="text-gray-400">{trade.timestamp}</span>
          </div>
        </div>
      ))}
    </div>
  )
}

export default RecentTrades