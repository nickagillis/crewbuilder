import './globals.css'
import type { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'CrewBuilder - AI Agent Meta-System',
  description: 'Build AI agents that build AI agent systems for your business',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className="bg-gray-50">{children}</body>
    </html>
  )
}