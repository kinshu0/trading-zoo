import React, { useState, useEffect, useRef } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { LineChart, Newspaper, History, Briefcase, Maximize2, Minimize2 } from 'lucide-react'
import Header from '../components/Header'
import GameTradingPit from '../components/GameTradingPit'
import StockPrices from '../components/StockPrices/StockPrices'
import NewsFeed from '../components/NewsFeed/NewsFeed'
import RecentTrades from '../components/RecentTrades/RecentTrades'
import TeamPortfolios from '../components/TeamPortfolios/TeamPortfolios'
import { toast } from 'react-toastify';
import api from '../services/api'
import HumanControls from '../components/HumanControls/HumanControls'

function GameScreen() {
  const [expandedComponent, setExpandedComponent] = useState(null)
  const stockPriceRef = useRef(null)
  const [gameStarted, setGameStarted] = useState(false)
  const [securities, setSecurities] = useState({})
  const [clients, setClients] = useState({})
  const [transactions, setTransactions] = useState({ completed: [], pending: [] })
  const [isStarting, setIsStarting] = useState(false)

  const handleNewsImpact = (ticker, multiplier) => {
    if (stockPriceRef) {
      stockPriceRef.current.handleNewsImpact(ticker, multiplier)
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

  const fetchGameData = async () => {
    try {
      await api.get('/tick')
      
      // Fetch all data in parallel
      const [securitiesRes, clientsRes, completedTxRes, pendingTxRes, eventRes, valuationHistoryRes] = await Promise.all([
        api.get('/securities'),
        api.get('/clients'),
        api.get('/completed_transactions'),
        api.get('/pending_transactions'),
        api.get('/isEvent'),
        api.get('/valuation_history')
      ])

      setSecurities(securitiesRes.data)
      setClients(clientsRes.data)
      setTransactions({
        completed: completedTxRes.data,
        pending: pendingTxRes.data
      })

      // If there's an event, pass it to the NewsFeed
      if (eventRes.data && eventRes.data !== '') {
        handleNewsImpact(eventRes.data)
      }

      setTimeout(fetchGameData, 6000)
    } catch (error) {
      console.error('Failed to fetch game data:', error)
      toast.error('Failed to fetch game data')
      setTimeout(fetchGameData, 6000)
    }
  }

  const startGame = async () => {
    if (isStarting) return
    
    try {
      setIsStarting(true)
      await api.get('/start')
      setGameStarted(true)
      fetchGameData()
    } catch (error) {
      console.error('Failed to start game:', error)
      toast.error('Failed to start game')
    } finally {
      setIsStarting(false)
    }
  }

  useEffect(() => {
    let mounted = true

    if (mounted && !gameStarted) {
      startGame()
    }

    return () => {
      mounted = false
    }
  }, [gameStarted])

  return (
    <div className="h-screen flex flex-col">
      <Header />
      <div className="flex-1 bg-gradient-to-br from-green-50 to-green-100 p-2">
        <div className="grid grid-cols-12 gap-2">
          <motion.div className="col-span-3 flex flex-col gap-2">
            <ComponentWrapper title="Team Portfolios" icon={Briefcase} name="portfolios">
              <TeamPortfolios data={clients} />
            </ComponentWrapper>
            
            <ComponentWrapper title="Stock Prices" icon={LineChart} name="stocks">
              <StockPrices data={securities} ref={stockPriceRef} />
            </ComponentWrapper>
          </motion.div>

          <motion.div className="col-span-6">
            <ComponentWrapper title="Market Performance" icon={LineChart} name="market">
              <GameTradingPit />
            </ComponentWrapper>
          </motion.div>

          <motion.div className="col-span-3 flex flex-col gap-2">
            <ComponentWrapper title="Jungle News" icon={Newspaper} name="news">
              <NewsFeed onNewsUpdate={handleNewsImpact} />
            </ComponentWrapper>

            <ComponentWrapper title="Recent Trades" icon={History} name="trades">
              <RecentTrades />
            </ComponentWrapper>
          </motion.div>
        </div>
      </div>
      <HumanControls securities={securities} />

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