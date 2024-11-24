import React, { useState, useEffect } from 'react'
import { Clock } from 'lucide-react'

function NewsFeed({ onNewsUpdate }) {
  const [news, setNews] = useState([])

  const generateNews = () => {
    const stocks = ['BNNA', 'ICEE', 'PINE', 'PEBB', 'FISH']
    const events = [
      { type: 'positive', multiplier: 1.05, templates: [
        'Increased demand for {stock}',
        'New market opens for {stock}',
        'Positive forecast for {stock}'
      ]},
      { type: 'negative', multiplier: 0.95, templates: [
        'Supply chain issues affect {stock}',
        'Decreased demand for {stock}',
        'Market concerns over {stock}'
      ]},
      { type: 'neutral', multiplier: 1, templates: [
        'Market analysis: {stock} stable',
        'New regulations for {stock}',
        'Industry review of {stock}'
      ]}
    ]

    const stock = stocks[Math.floor(Math.random() * stocks.length)]
    const event = events[Math.floor(Math.random() * events.length)]
    const template = event.templates[Math.floor(Math.random() * event.templates.length)]
    const title = template.replace('{stock}', stock)

    return {
      id: Date.now(),
      title,
      timestamp: 'just now',
      impact: event.type,
      stock,
      multiplier: event.multiplier,
      description: `Market analysts report ${title.toLowerCase()} affecting trading patterns...`
    }
  }

  useEffect(() => {
    const interval = setInterval(() => {
      const newNewsItem = generateNews()
      setNews(prev => [newNewsItem, ...prev.slice(0, 4)])
      onNewsUpdate(newNewsItem.stock, newNewsItem.multiplier)
    }, 8000)

    return () => clearInterval(interval)
  }, [onNewsUpdate])

  return (
    <div className="space-y-1 p-1">
      {news.map(item => (
        <div key={item.id} 
          className={`rounded p-1.5 text-xs ${
            item.impact === 'positive' ? 'bg-green-50' :
            item.impact === 'negative' ? 'bg-red-50' : 'bg-gray-50'
          }`}
        >
          <div className="flex justify-between items-center">
            <h3 className="font-medium">{item.title}</h3>
            <div className="flex items-center gap-0.5 text-gray-500">
              <Clock className="w-3 h-3" />
              <span>{item.timestamp}</span>
            </div>
          </div>
          <p className="text-gray-600 mt-1 text-[0.7rem]">
            {item.description}
          </p>
        </div>
      ))}
    </div>
  )
}

export default NewsFeed