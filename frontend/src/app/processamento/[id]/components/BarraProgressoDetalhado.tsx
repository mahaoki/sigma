"use client"

import { useEffect, useState } from "react"
import { obterProgresso } from "@/lib/api/processamento/progresso"
import { Skeleton } from "@/components/ui/skeleton"

type Props = {
  periodoId: number
  emAndamento: boolean
}

export function BarraProgressoDetalhado({ periodoId, emAndamento }: Props) {
  const [progresso, setProgresso] = useState<{
    verificadas: number
    coletadas_raw: number
    completas_raw: number
  } | null>(null)

  useEffect(() => {
    let intervalo: NodeJS.Timeout | null = null

    const fetchProgresso = async () => {
      try {
        const data = await obterProgresso(periodoId)
        setProgresso(data)
      } catch (err) {
        console.error("Erro ao obter progresso:", err)
      }
    }

    fetchProgresso()

    if (emAndamento) {
      intervalo = setInterval(fetchProgresso, 5000)
    }

    return () => {
      if (intervalo) clearInterval(intervalo)
    }
  }, [periodoId, emAndamento])

  if (!progresso) return <Skeleton className="h-20 w-full" />

  return (
    <div className="bg-muted p-4 rounded-md border text-sm space-y-2">
      <div className="font-medium">Processo de coleta</div>
      <div className="grid grid-cols-3 gap-4">
        <div>
          <strong>Verificadas:</strong> {progresso.verificadas}
        </div>
        <div>
          <strong>Contratações:</strong> {progresso.coletadas_raw}/{progresso.verificadas}
        </div>
        <div>
          <strong>Entidades completas:</strong> {progresso.completas_raw}/{progresso.coletadas_raw}
        </div>
      </div>
    </div>
  )
}
