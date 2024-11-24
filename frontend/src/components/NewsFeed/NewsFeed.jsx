import React, { useState, useEffect } from 'react'
import { Clock, ChevronDown, ChevronUp } from 'lucide-react'
import api from '../../services/api'

function NewsFeed({ onNewsUpdate }) {
  const [news, setNews] = useState([])
  const [isExpanded, setIsExpanded] = useState(false)

  const getImpactType = (severity) => {
    if (severity > 0) return 'positive'
    if (severity < 0) return 'negative'
    return 'neutral'
  }

  const fetchEvents = async () => {
    try {
      const response = await api.get('/isEvent')
      if (response.data && response.data.length > 0) {
        const formattedNews = response.data.map(event => ({
          id: Date.now() + Math.random(),
          title: event,
          timestamp: new Date().toLocaleTimeString(),
          impact: getImpactType(1),
          description: event
        }))
        setNews(formattedNews)
      }
    } catch (error) {
      console.error('Failed to fetch events:', error)
    }
  }

  useEffect(() => {
    fetchEvents()
    const interval = setInterval(fetchEvents, 2000)
    return () => clearInterval(interval)
  }, [])

  const displayedNews = isExpanded ? news : news.slice(-5)

  return (
    <div className="space-y-1 p-1">
      <div className="flex justify-between items-center px-1 mb-1">
        <span className="text-xs text-gray-500">
          {isExpanded ? 'All Events' : 'Recent Events'}
        </span>
        <button
          onClick={() => setIsExpanded(!isExpanded)}
          className="text-gray-500 hover:text-gray-700"
        >
          {isExpanded ? (
            <ChevronUp className="w-4 h-4" />
          ) : (
            <ChevronDown className="w-4 h-4" />
          )}
        </button>
      </div>
      
      {displayedNews.map(item => (
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