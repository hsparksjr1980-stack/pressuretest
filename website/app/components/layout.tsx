import type { Metadata } from "next";
import "./globals.css";
import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";

export const metadata: Metadata = {
  title: "PressureTest",
  description:
    "Operator-focused franchise and small-business diligence platform.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="bg-[#0b0f14] text-white">
        <Navbar />
        {children}
        <Footer />
      </body>
    </html>
  );
}