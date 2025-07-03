import { NextResponse, type NextRequest } from "next/server"
import { auth0 } from "./lib/auth0"
import { fetchUserInfo } from "./app/actions"

export async function middleware(request: NextRequest) {
  const authRes = await auth0.middleware(request)

  // authentication routes — let the middleware handle it
  if (request.nextUrl.pathname.startsWith("/auth")) {
    return authRes
  }

  const sessionData = await auth0.getSession()
  const isAuthenticated = !!sessionData?.user

  if (!isAuthenticated) {
    return NextResponse.redirect(new URL("/auth/login", request.nextUrl.origin))
  }

  // TODO: avoid fetching user info on every request
  const userInfo = await fetchUserInfo()
  if (
    userInfo?.pseudo == "New Player" &&
    !request.nextUrl.pathname.startsWith("/user/rename")
  ) {
    return NextResponse.redirect(new URL("/user/rename", request.url))
  }

  // protected routes
  if (request.nextUrl.pathname.startsWith("/admin") && !userInfo?.is_admin) {
    return NextResponse.redirect(new URL("/", request.url))
  }

  return NextResponse.next()
}

export const config = {
  matcher: [
    /*
     * Match all request paths except for the ones starting with:
     * - _next/static (static files)
     * - _next/image (image optimization files)
     * - favicon.ico, sitemap.xml, robots.txt (metadata files)
     */
    "/((?!_next/static|_next/image|favicon.ico|sitemap.xml|robots.txt).*)",
  ],
}
