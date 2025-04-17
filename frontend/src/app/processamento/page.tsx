"use client"

import { useState } from "react"
import { FormularioProcessamento } from "./components/FormularioProcessamento"
import { TabelaPeriodos } from "./components/TabelaPeriodos"

export default function PaginaProcessamento() {
  const [periodoId, setPeriodoId] = useState<number | null>(null)

  return (
    <div className="p-6 space-y-6">
      <h1 className="text-2xl font-bold">Painel de processamento</h1>

      <FormularioProcessamento onProcessamentoIniciado={setPeriodoId} />
      <TabelaPeriodos periodoIdEmAndamento={periodoId} />
    </div>
  )
}
