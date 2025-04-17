import "./globals.css"
import type { Metadata } from "next"
import { Inter } from "next/font/google"
import { cn } from "@/lib/utils"

const inter = Inter({ subsets: ["latin"] })

export const metadata: Metadata = {
  title: "Sigma - Painel de Processamento",
  description: "Monitoramento de Coleta e ETL",
}

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="pt-BR">
      <body className={cn("min-h-screen bg-background text-foreground", inter.className)}>
        <main className="p-6">{children}</main>
      </body>
    </html>
  )
}
