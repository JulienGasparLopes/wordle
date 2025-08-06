import localFont from "next/font/local"
import "./globals.css"
import Header from "@/components/shared/header"

const geistSans = localFont({
  src: "./fonts/GeistVF.woff",
  variable: "--font-geist-sans",
  weight: "100 900",
})
const geistMono = localFont({
  src: "./fonts/GeistMonoVF.woff",
  variable: "--font-geist-mono",
  weight: "100 900",
})

const RootLayout = async ({
  children,
}: Readonly<{
  children: React.ReactNode
}>) => {
  return (
    <html lang="en" className="h-full">
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased h-full bg-black text-white overflow-hidden`}
      >
        <div className="h-full px-8 grid grid-rows-[70px_auto] justify-items-center overflow-hidden">
          <Header />
          <div className="h-full overflow-hidden">{children}</div>
        </div>
      </body>
    </html>
  )
}

export default RootLayout
