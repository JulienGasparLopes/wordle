import { NextRequest, NextResponse } from 'next/server'
import { cookies } from 'next/headers'


export default async function middleware(req: NextRequest) {
    const path = req.nextUrl.pathname

    const cookiesStore = await cookies()
    const isLogedIn = cookiesStore.has('pseudo')

    if (!isLogedIn && path !== '/login') {
        return NextResponse.redirect(new URL('/login', req.nextUrl))
    }

    return NextResponse.next()
}

export const config = {
    matcher: ['/login', "/logout", "/game/:gameId", "/game", "/leaderboard"],
}