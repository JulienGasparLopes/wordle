'use server'

import { redirect } from 'next/navigation'
import { getHeaders } from './connection'

export const redirectToAllGames = async () => {
  redirect('/')
}

export const fetchUserInfo = async () => {
  // TODO: save into session to create cache (or just use next cache)
  const result_raw = await fetch(`http://localhost:5001/user/current`, {
    method: 'GET',
    headers: await getHeaders(),
  })
  return await result_raw.json()
}

export const fetchAllGames = async () => {
  const result_raw = await fetch(`http://localhost:5001/game`, {
    method: 'GET',
    headers: await getHeaders(),
  })
  const results_raw = await result_raw.json()
  const results = results_raw.games.map(
    (result: {
      game_id: number
      word_length: number
      start_date: string
      state: string
      locked: boolean
    }) => ({
      id: result.game_id,
      wordLength: result.word_length,
      locked: result.locked,
      date: result.start_date,
      state: result.state,
    })
  )
  return results.sort(
    (a: { date: string }, b: { date: string }) =>
      new Date(b.date).getTime() - new Date(a.date).getTime()
  )
}
