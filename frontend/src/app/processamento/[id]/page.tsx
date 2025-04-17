"use client"

import { useParams, useSearchParams } from "next/navigation"
import { BarraProgressoDetalhado } from "./components/BarraProgressoDetalhado"
import ResumoProcessamento from "./components/ResumoProcessamento"
import { ArrowLeft } from "lucide-react"
import Link from "next/link"


export default function DetalheProcessamentoPage() {
  const params = useParams()
  const searchParams = useSearchParams()

  const periodoId = Number(params.id)
  const emAndamento =
    searchParams.get("status") === "pendente" || searchParams.get("status") === "em_andamento"

  const data = searchParams.get("data")
  const inicio = searchParams.get("inicio")
  const fim = searchParams.get("fim")

  return (
    <div className="p-6 space-y-6">
      <Link href="/processamento" className="flex items-center text-sm text-muted-foreground hover:text-foreground transition">
        <ArrowLeft className="w-4 h-4 mr-2" />
        Voltar para listagem
      </Link>
      <h1 className="text-xl font-bold">Detalhe do processamento</h1>
      <div className="text-sm text-muted-foreground">
        <p><strong>Período:</strong> {data}</p>
        <p><strong>Início processamento:</strong> {inicio}</p>
        <p><strong>Fim processamento:</strong> {fim}</p>
      </div>

      <BarraProgressoDetalhado periodoId={periodoId} emAndamento={emAndamento} />

      {!emAndamento && (
        <div className="space-y-4">
          <h2 className="text-lg font-semibold">Resumo do ETL</h2>
          <ResumoProcessamento periodoId={periodoId} />
        </div>
      )}
    </div>
  )
}
