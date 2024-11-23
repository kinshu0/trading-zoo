import { motion } from 'framer-motion'
import styles from './HeroSection.module.styl'
import Button from './ui/Button'
import { Sparkles } from 'lucide-react'
import { useNavigate } from 'react-router-dom'

const emojiVariants = {
  hidden: { y: 20, opacity: 0 },
  visible: i => ({
    y: 0,
    opacity: 1,
    transition: {
      delay: i * 0.1,
      duration: 0.5,
      ease: 'easeOut'
    }
  })
}

const buttonVariants = {
  hover: { scale: 1.05, transition: { duration: 0.2 } },
  tap: { scale: 0.95 }
}

export function HeroSection () {
  const navigate = useNavigate()
  const emojis = ['🐒', '🐧', '🦊', '🦎', '👤']

  const handleStartGame = () => {
    navigate('/game')
  }

  return (
    <motion.section
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.6 }}
      className={`text-center py-16 rounded-lg shadow-lg my-8 relative overflow-hidden ${styles.gradientBg}`}
    >
      <div className="relative z-10">
        <motion.h2
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2, duration: 0.5 }}
          className="text-5xl font-display mb-4 text-green-900 tracking-tight"
        >
          Welcome to the Jungle! <Sparkles className="inline-block ml-2 text-yellow-500" />
        </motion.h2>
        
        <motion.p
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.4 }}
          className="text-xl mb-8 text-green-800"
        >
          Watch as animals trade exotic goods in a wild market simulation!
        </motion.p>

        <div className="flex justify-center">
          <motion.div variants={buttonVariants} whileHover="hover" whileTap="tap">
            <Button 
              size="lg" 
              className="bg-green-500 hover:bg-green-600"
              onClick={handleStartGame}
            >
              Join the Jungle
            </Button>
          </motion.div>
        </div>
      </div>

      <div className={`mt-12 flex justify-center space-x-8 ${styles.emojiContainer}`}>
        {emojis.map((emoji, i) => (
          <motion.span
            key={i}
            custom={i}
            variants={emojiVariants}
            initial="hidden"
            animate="visible"
            className={`text-4xl ${styles.emojiWrapper}`}
          >
            {emoji}
          </motion.span>
        ))}
      </div>
    </motion.section>
  )
}

