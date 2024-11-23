import React from 'react'
import { motion } from 'framer-motion'
import { LineChart, Newspaper, History, Briefcase } from 'lucide-react'
import TradingPit from '../components/TradingPit'
import StockPrices from '../components/StockPrices/StockPrices'
import NewsFeed from '../components/NewsFeed/NewsFeed'
import RecentTrades from '../components/RecentTrades/RecentTrades'
import TeamPortfolios from '../components/TeamPortfolios/TeamPortfolios'
import styles from './GameScreen.module.styl'

function GameScreen() {
  return (
    <div className="h-screen bg-gradient-to-br from-green-50 to-green-100 p-6">
      <div className="grid grid-cols-12 gap-6 h-full">
        {/* Left Sidebar */}
        <motion.div 
          initial={{ x: -50, opacity: 0 }}
          animate={{ x: 0, opacity: 1 }}
          className="col-span-3 flex flex-col gap-6"
        >
          <div className="bg-white rounded-lg shadow-md p-4 flex-1">
            <div className="flex items-center gap-2 mb-4">
              <Briefcase className="text-green-600" />
              <h2 className="text-xl font-display">Team Portfolios</h2>
            </div>
            <TeamPortfolios />
          </div>
          
          <div className="bg-white rounded-lg shadow-md p-4 flex-1">
            <div className="flex items-center gap-2 mb-4">
              <LineChart className="text-green-600" />
              <h2 className="text-xl font-display">Stock Prices</h2>
            </div>
            <StockPrices />
          </div>
        </motion.div>

        {/* Main Content */}
        <motion.div 
          initial={{ y: 50, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          className="col-span-6"
        >
          <div className="bg-white rounded-lg shadow-md p-4 h-full">
            <div className="flex items-center gap-2 mb-4">
              <LineChart className="text-green-600" />
              <h2 className="text-xl font-display">Market Performance</h2>
            </div>
            <TradingPit />
          </div>
        </motion.div>

        {/* Right Sidebar */}
        <motion.div 
          initial={{ x: 50, opacity: 0 }}
          animate={{ x: 0, opacity: 1 }}
          className="col-span-3 flex flex-col gap-6"
        >
          <div className="bg-white rounded-lg shadow-md p-4 flex-1">
            <div className="flex items-center gap-2 mb-4">
              <Newspaper className="text-green-600" />
              <h2 className="text-xl font-display">Jungle News</h2>
            </div>
            <NewsFeed />
          </div>

          <div className="bg-white rounded-lg shadow-md p-4 flex-1">
            <div className="flex items-center gap-2 mb-4">
              <History className="text-green-600" />
              <h2 className="text-xl font-display">Recent Trades</h2>
            </div>
            <RecentTrades />
          </div>
        </motion.div>
      </div>
    </div>
  )
}

export default GameScreen 