import React, { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { LineChart, Newspaper, History, Briefcase, Maximize2, Minimize2 } from 'lucide-react'
import Header from '../components/Header'
import GameTradingPit from '../components/GameTradingPit'
import StockPrices from '../components/StockPrices/StockPrices'
import NewsFeed from '../components/NewsFeed/NewsFeed'
import RecentTrades from '../components/RecentTrades/RecentTrades'
import TeamPortfolios from '../components/TeamPortfolios/TeamPortfolios'

function GameScreen() {
  const [expandedComponent, setExpandedComponent] = useState(null)
  const [stockPriceRef, setStockPriceRef] = useState(null)

  const handleNewsImpact = (ticker, multiplier) => {
    if (stockPriceRef) {
      stockPriceRef.handleNewsImpact(ticker, multiplier)
    }
  }

  const ComponentWrapper = ({ title, icon: Icon, children, name }) => {
    const isExpanded = expandedComponent === name
    
    return (
      <div className={`bg-white rounded-lg shadow-sm transition-all duration-300 ${
        isExpanded ? 'fixed inset-2 z-50 flex flex-col' : 'min-h-fit'
      }`}>
        <div className="flex items-center justify-between px-2 py-1 border-b bg-white">
          <div className="flex items-center gap-1">
            <Icon className="text-green-600 w-3 h-3" />
            <h2 className="text-xs font-display">{title}</h2>
          </div>
          <button
            onClick={() => setExpandedComponent(isExpanded ? null : name)}
            className="p-0.5 hover:bg-gray-100 rounded-full transition-colors"
          >
            {isExpanded ? (
              <Minimize2 className="w-3 h-3 text-gray-600" />
            ) : (
              <Maximize2 className="w-3 h-3 text-gray-600" />
            )}
          </button>
        </div>
        <div className={isExpanded ? 'flex-1 overflow-auto' : ''}>
          {children}
        </div>
      </div>
    )
  }

  return (
    <div className="h-screen flex flex-col">
      <Header />
      <div className="flex-1 bg-gradient-to-br from-green-50 to-green-100 p-2">
        <div className="grid grid-cols-12 gap-2">
          {/* Left Sidebar */}
          <motion.div 
            initial={{ x: -20, opacity: 0 }}
            animate={{ x: 0, opacity: 1 }}
            className="col-span-3 flex flex-col gap-2"
          >
            <ComponentWrapper 
              title="Team Portfolios" 
              icon={Briefcase}
              name="portfolios"
            >
              <TeamPortfolios />
            </ComponentWrapper>
            
            <ComponentWrapper 
              title="Stock Prices" 
              icon={LineChart}
              name="stocks"
            >
              <StockPrices ref={setStockPriceRef} />
            </ComponentWrapper>
          </motion.div>

          {/* Main Content */}
          <motion.div 
            initial={{ y: 20, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            className="col-span-6"
          >
            <ComponentWrapper 
              title="Market Performance" 
              icon={LineChart}
              name="market"
            >
              <GameTradingPit />
            </ComponentWrapper>
          </motion.div>

          {/* Right Sidebar */}
          <motion.div 
            initial={{ x: 20, opacity: 0 }}
            animate={{ x: 0, opacity: 1 }}
            className="col-span-3 flex flex-col gap-2"
          >
            <ComponentWrapper 
              title="Jungle News" 
              icon={Newspaper}
              name="news"
            >
              <NewsFeed onNewsUpdate={handleNewsImpact} />
            </ComponentWrapper>

            <ComponentWrapper 
              title="Recent Trades" 
              icon={History}
              name="trades"
            >
              <RecentTrades />
            </ComponentWrapper>
          </motion.div>
        </div>
      </div>

      <AnimatePresence>
        {expandedComponent && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 bg-black bg-opacity-50 z-40"
            onClick={() => setExpandedComponent(null)}
          />
        )}
      </AnimatePresence>
    </div>
  )
}

export default GameScreen