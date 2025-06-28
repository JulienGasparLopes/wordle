import localFont from 'next/font/local'
import './globals.css'
import Header from '@/components/shared/Header'

const geistSans = localFont({
  src: './fonts/GeistVF.woff',
  variable: '--font-geist-sans',
  weight: '100 900',
})
const geistMono = localFont({
  src: './fonts/GeistMonoVF.woff',
  variable: '--font-geist-mono',
  weight: '100 900',
})

const RootLayout = async ({
  children,
}: Readonly<{
  children: React.ReactNode
}>) => {
  return (
    <html lang="en" className="h-full">
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased h-full bg-black text-white`}
      >
        <div className="h-full p-8 grid grid-rows-[70px_auto] justify-items-center">
          <Header />
          <div className="h-full">{children}</div>
        </div>
      </body>
    </html>
  )
}

export default RootLayout
