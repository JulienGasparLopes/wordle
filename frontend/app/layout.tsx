import localFont from "next/font/local";
import "./globals.css";
import { fetchUserInfo, redirectToAllGames } from "./actions";
import { auth0 } from "@/lib/auth0";

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
                {/* <button className="text-white" formAction={redirectToAllGames}>
                    Home
                  </button> */}
                <a href="/">Home</a>
                <h2 className="text-4xl font-bold mb-8">{userInfo?.pseudo}</h2>
                <div className="flex gap-8">
                  <a href="/user/rename">Rename</a>
                  <a href="/auth/logout">Logout</a>
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
