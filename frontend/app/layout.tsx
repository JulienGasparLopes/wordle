import localFont from "next/font/local";
import "./globals.css";
import { redirectToAllGames, redirectToLogout } from "./actions";
import { getPseudo } from "./connection";

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
  const pseudo = await getPseudo();

  return (
    <html lang="en" className="h-full">
      <body className={`${geistSans.variable} ${geistMono.variable} antialiased h-full bg-black text-white`}>
        <div className="h-full p-8 grid grid-rows-[70px_auto] justify-items-center">
          <div className="flex justify-between w-full">
            {pseudo && (
              <>
                <form>
                  <button className="text-white" formAction={redirectToAllGames}>
                    Home
                  </button>
                </form>
                <h2 className="text-4xl font-bold mb-8">{pseudo}</h2>
                <form>
                  <button className="text-white" formAction={redirectToLogout}>
                    Logout
                  </button>
                </form>
              </>
            )}
          </div>
          <div className="h-full">{children}</div>
        </div>
      </body>
    </html>
  );
};

export default RootLayout;
