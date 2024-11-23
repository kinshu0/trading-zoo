import React from 'react'
import { ArrowUpRight, ArrowDownRight } from 'lucide-react'
import styles from './RecentTrades.module.styl'

function RecentTrades() {
  // This would typically come from your state management
  const trades = [
    {
      id: 1,
      team: 'Penguins',
      action: 'buy',
      stock: 'BNNA',
      amount: 100,
      price: 150.25
    },
    {
      id: 2,
      team: 'Monkeys',
      action: 'sell',
      stock: 'COCO',
      amount: 50,
      price: 85.75
    },
    {
      id: 3,
      team: 'Foxes',
      action: 'buy',
      stock: 'LEAF',
      amount: 75,
      price: 45.30
    }
  ]

  return (
    <div className={styles.recentTrades}>
      {trades.map(trade => (
        <div key={trade.id} className={styles.tradeItem}>
          <div className={styles.tradeTeam}>
            <span className={styles[trade.team.toLowerCase()]}>{trade.team}</span>
          </div>
          <div className={styles.tradeInfo}>
            <span className={`${styles.tradeAction} ${styles[trade.action]}`}>
              {trade.action === 'buy' ? <ArrowUpRight size={16} /> : <ArrowDownRight size={16} />}
              {trade.action.toUpperCase()}
            </span>
            <span className={styles.tradeDetails}>
              {trade.amount} {trade.stock} @ ${trade.price}
            </span>
          </div>
        </div>
      ))}
    </div>
  )
}

export default RecentTrades 