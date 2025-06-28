import { fetchAllGames } from './actions'
import AllGames from './gameList'
import { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'Accueil',
}

export default async function Home() {
  const allGames = await fetchAllGames()
  return <AllGames allGames={allGames} />
}
