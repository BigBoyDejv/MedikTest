import type { Metadata, Viewport } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import { Navbar } from "@/components/navbar";

const inter = Inter({ subsets: ["latin", "latin-ext"] });

export const metadata: Metadata = {
  title: "Doktorský Edukátor | Bezplatná príprava na prijímačky",
  description:
    "Bezplatná open-access EdTech aplikácia na prípravu na prijímacie skúšky na medicínu (Biológia, Chémia).",
};

export const viewport: Viewport = {
  width: "device-width",
  initialScale: 1,
  maximumScale: 5,
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="sk">
      <body className={`${inter.className} overflow-x-hidden`}>
        <div className="flex min-h-screen flex-col">
          <Navbar />
          <div className="flex-1">{children}</div>
        </div>
      </body>
    </html>
  );
}
