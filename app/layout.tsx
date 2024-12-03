import "./globals.css";
import { Inter } from "next/font/google";

const inter = Inter({ subsets: ["latin"] });

export const metadata = {
  title: "Shortest Path Finder",
  description: "Find the Shortest Path Betweeen two Locations with Dijkstra's algorithm!",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <head>
        <script
          src={`https://maps.googleapis.com/maps/api/js?key=${process.env.NEXT_PUBLIC_GOOGLE_API_KEY}&libraries=places`}
          async
          defer
        ></script>
      </head>
      <body className={inter.className}>{children}</body>
    </html>
  );
}
