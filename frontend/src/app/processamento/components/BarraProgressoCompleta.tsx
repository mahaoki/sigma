"use client"

import { useEffect, useState } from "react"
import { Progress } from "@/components/ui/progress"
import { getProgressoCompleto } from "@/lib/api/processamento/getProgressoCompleto"

interface ProgressoTotal {
  pncp: number
  coleta: number
  etl: number
}

interface DadosAuxiliares {
  pncp_verificados: number
  pncp_sucesso: number
  contratacoes_total: number
  contratacoes_coletadas: number
  dw_processadas: number
  modalidades_processadas: number
}
export function BarraProgressoCompleta({
    periodoId,
    onFinalizado,
  }: {
    periodoId: number
    onFinalizado?: () => void
  }) {
    
  const [progresso, setProgresso] = useState<ProgressoTotal>({ pncp: 0, coleta: 0, etl: 0 })
  const [dados, setDados] = useState<DadosAuxiliares | null>(null)
  const [ativo, setAtivo] = useState(true)

  useEffect(() => {
    if (!ativo) return

    const intervalo = setInterval(async () => {
      try {
        const res = await getProgressoCompleto(periodoId)
        setProgresso(res.percentuais)
        setDados(res)

        const { pncp, coleta, etl } = res.percentuais
        if (pncp >= 100 && coleta >= 100 && etl >= 100) {
          clearInterval(intervalo)
          setAtivo(false)
          onFinalizado?.()
        }
      } catch (error) {
        console.error("Erro ao buscar progresso completo:", error)
      }
    }, 3000)

    return () => clearInterval(intervalo)
  }, [periodoId, ativo])

  return (
    <div className="space-y-4 text-sm">
    <div>
      <div className="flex justify-between mb-1">
        <span className="font-medium">Verificando publicações de atualizações</span>
        {dados && (
          <span className="text-muted-foreground">
            Verificadas: {dados.pncp_verificados} Modalidades: {dados.modalidades_processadas}/14
          </span>
        )}
      </div>
      <Progress value={progresso.pncp} />
    </div>

      <div>
        <div className="flex justify-between mb-1">
          <span className="font-medium">Processo de coleta</span>
          {dados && (
            <span className="text-muted-foreground">
              Contratações: {dados.contratacoes_coletadas}/{dados.contratacoes_total}
            </span>
          )}
        </div>
        <Progress value={progresso.coleta} />
      </div>

      <div>
        <div className="flex justify-between mb-1">
          <span className="font-medium">Processo de ETL</span>
          {dados && (
            <span className="text-muted-foreground">
              Contratações: {dados.dw_processadas}/{dados.contratacoes_coletadas}
            </span>
          )}
        </div>
        <Progress value={progresso.etl} />
      </div>
    </div>
  )
}
