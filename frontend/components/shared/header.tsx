'use server'

import { fetchUserInfo } from '@/app/actions'
import { Home, LogOut, Pencil, Shield } from 'lucide-react'
import Link from 'next/link'

export default async function Header() {
  const userInfo = await fetchUserInfo()

  return (
    <div className="flex justify-between w-full items-center">
      <div className="flex items-center gap-8">
        <Link href="/" className="flex items-center gap-2">
          <Home size={20} />
          <span>Home</span>
        </Link>
        {userInfo?.is_admin && (
          <Link href="/admin" className="flex items-center gap-2">
            <Shield size={20} />
            <span>Admin</span>
          </Link>
        )}
      </div>
      <div className="flex items-center gap-4">
        <span className="font-bold">{userInfo?.pseudo}</span>
        <Link
          href="/user/rename"
          title="Rename"
          className="bg-blue-500 text-white rounded-md p-2 hover:text-white hover:bg-blue-600"
        >
          <Pencil size={20} />
        </Link>
        <Link
          href="/auth/logout"
          title="Logout"
          className="bg-red-500 text-white rounded-md p-2 hover:text-white hover:bg-red-600"
        >
          <LogOut size={20} />
        </Link>
      </div>
    </div>
  )
}
