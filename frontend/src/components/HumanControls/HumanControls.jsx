import React from 'react'
import api from '../../services/api'
import { toast } from 'react-toastify'

function HumanControls({ securities }) {
  const handleTrade = async (security, isBuy) => {
    try {
      const currentPrice = securities[security]
      const price = currentPrice
      
      const isBuyStr = isBuy ? 'True' : 'False'
      const orderResponse = await api.get(`/add_order/hooman/${security}/${price}/1/${isBuyStr}`)
      
      if (orderResponse.status === 200) {
        toast.success(`Order placed: ${isBuy ? 'Buy' : 'Sell'} 1 ${security} at ${price.toFixed(2)}`)
      }
    } catch (error) {
      console.error('Failed to place order:', error)
      toast.error(`Failed to place ${isBuy ? 'buy' : 'sell'} order for ${security}`)
    }
  }

  return (
    <div className="fixed bottom-4 left-1/2 transform -translate-x-1/2 bg-white rounded-lg shadow-lg p-2">
      <div className="flex gap-2">
        {Object.keys(securities).map(security => (
          <div key={security} className="flex flex-col items-center gap-1">
            <span className="text-xs font-medium">{security}</span>
            <span className="text-xs text-gray-500">${securities[security].toFixed(2)}</span>
            <div className="flex gap-1">
              <button
                onClick={() => handleTrade(security, true)}
                className="px-2 py-1 text-xs bg-green-100 hover:bg-green-200 text-green-700 rounded transition-colors"
              >
                Buy 1
              </button>
              <button
                onClick={() => handleTrade(security, false)}
                className="px-2 py-1 text-xs bg-red-100 hover:bg-red-200 text-red-700 rounded transition-colors"
              >
                Sell 1
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}

export default HumanControls 