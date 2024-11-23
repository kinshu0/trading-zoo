import React from 'react'
import { Clock } from 'lucide-react'
import styles from './NewsFeed.module.styl'

function NewsFeed() {
  // This would typically come from your state management
  const news = [
    {
      id: 1,
      title: 'BNNA Stock Surges on New Product Launch',
      timestamp: '2 min ago',
      impact: 'positive'
    },
    {
      id: 2,
      title: 'COCO Reports Lower Than Expected Q2 Earnings',
      timestamp: '5 min ago',
      impact: 'negative'
    },
    {
      id: 3,
      title: 'Market Analysis: Jungle Stocks Show Strong Growth',
      timestamp: '15 min ago',
      impact: 'neutral'
    }
  ]

  return (
    <div className={styles.newsFeed}>
      {news.map(item => (
        <div key={item.id} className={styles.newsItem}>
          <h3 className={styles.newsTitle}>{item.title}</h3>
          <div className={styles.newsTime}>
            <Clock size={14} />
            <span>{item.timestamp}</span>
          </div>
        </div>
      ))}
    </div>
  )
}

export default NewsFeed 