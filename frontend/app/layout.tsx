import localFont from "next/font/local";
import "./globals.css";
import { fetchUserInfo } from "./actions";
import Link from "next/link";

const geistSans = localFont({
  src: "./fonts/GeistVF.woff",
  variable: "--font-geist-sans",
  weight: "100 900",
});
const geistMono = localFont({
  src: "./fonts/GeistMonoVF.woff",
  variable: "--font-geist-mono",
  weight: "100 900",
});

const RootLayout = async ({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) => {
  const userInfo = await fetchUserInfo();

  return (
    <html lang="en" className="h-full">
      <body className={`${geistSans.variable} ${geistMono.variable} antialiased h-full bg-black text-white`}>
        <div className="h-full p-8 grid grid-rows-[70px_auto] justify-items-center">
          <div className="flex justify-between w-full">
            {
              <>
                <div className="flex gap-8">
                  <Link href="/">Home</Link>
                  {userInfo?.is_admin && <Link href="/admin">Admin</Link>}
                </div>
                <h2 className="text-4xl font-bold mb-8">{userInfo?.pseudo}</h2>
                <div className="flex gap-8">
                  <Link href="/user/rename">Rename</Link>
                  <Link href="/auth/logout">Logout</Link>
                </div>
              </>
            }
          </div>
          <div className="h-full">{children}</div>
        </div>
      </body>
    </html>
  );
};

export default RootLayout;
