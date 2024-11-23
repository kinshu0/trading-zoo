import Header from '../components/Header'
import HeroSection from '../components/HeroSection'
import TeamSection from '../components/TeamSection'
import AssetSection from '../components/AssetSection'
import TradingPit from '../components/TradingPit'
import LeaderboardSection from '../components/LeaderboardSection'

export default function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-b from-green-100 to-green-300">
      <Header />
      <main className="container mx-auto px-4 py-8">
        <HeroSection />
        <TeamSection />
        <AssetSection />
        <TradingPit />
        <LeaderboardSection />
      </main>
    </div>
  )
}

