import type { Metadata } from "next";
import "./globals.css";

import Navbar from "../components/Navbar";
import Footer from "../components/Footer";

export const metadata: Metadata = {
  title: "PressureTest: Franchise",
  description:
    "Educational franchise diligence software for prospective operators.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="bg-[#070a0d] text-white">
        <Navbar />
        {children}
        <Footer />
      </body>
    </html>
  );
}
