"use client"

import { useEffect, useState } from "react"
import { getProgresso } from "@/lib/api/processamento/getProgresso"
import { Progress } from "@ui/progress"
import type { Progresso } from "@/lib/api/processamento/schemas"

type Props = {
  periodoId: number
}

export function BarraProgresso({ periodoId }: Props) {
  const [dados, setDados] = useState<Progresso["percentual"]>({ coleta: 0, etl: 0 })
  const [ativo, setAtivo] = useState(true)

  useEffect(() => {
    if (!ativo) return

    const intervalo = setInterval(async () => {
      try {
        const progresso = await getProgresso(periodoId)
        setDados(progresso.percentual)

        // Finaliza polling quando ambos estiverem em 100
        if (progresso.percentual.etl >= 100 && progresso.percentual.coleta >= 100) {
          setAtivo(false)
          clearInterval(intervalo)
        }
      } catch (err) {
        console.error("Erro ao buscar progresso:", err)
      }
    }, 3000)

    return () => clearInterval(intervalo)
  }, [periodoId, ativo])

  return (
    <div className="space-y-4">
      <div>
        <p className="text-sm">Coleta</p>
        <Progress value={dados.coleta} />
      </div>
      <div>
        <p className="text-sm">ETL</p>
        <Progress value={dados.etl} />
      </div>
    </div>
  )
}
