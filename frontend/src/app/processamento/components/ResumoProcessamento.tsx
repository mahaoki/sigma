"use client"

import { useEffect, useState } from "react"
import { Card } from "@ui/card"
import { Skeleton } from "@ui/skeleton"
import { getResultadoProcessamento } from "@lib/api/processamento/getResultado"
import { format } from "date-fns"
import { ptBR } from "date-fns/locale"

type Resultado = {
  periodo: string
  inicio: string
  fim: string | null
  entidades: Record<string, [number, number]>
  resumo_status: Record<string, number>
  dimensoes: Record<string, number>
}

export function ResumoProcessamento({ periodoId }: { periodoId: number }) {
  const [data, setData] = useState<Resultado | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchData = async () => {
      try {
        const resultado = await getResultadoProcessamento(periodoId)
        setData(resultado)
      } finally {
        setLoading(false)
      }
    }

    fetchData()
  }, [periodoId])

  if (loading || !data) {
    return <Skeleton className="w-full h-64" />
  }

  const formatDate = (iso: string | null) =>
    iso ? format(new Date(iso), "dd/MM/yyyy - HH:mm:ss", { locale: ptBR }) : "-"

  const durationInSeconds =
    data.inicio && data.fim
      ? (new Date(data.fim).getTime() - new Date(data.inicio).getTime()) / 1000
      : 0

  const durationFormatted = durationInSeconds
    ? `${Math.floor(durationInSeconds / 60)} minutos ${Math.round(durationInSeconds % 60)} segundos`
    : "-"

  const entidadesLabels: Record<string, string> = {
    contratacoes: "Contratações",
    documentos_contratacao: "Documentos de contratações",
    itens: "Itens da contratação",
    resultados: "Resultados de itens",
    contratos: "Contratos",
    documentos_contrato: "Documentos do contrato",
    termos: "Termos do contrato",
    documentos_termo: "Documentos do termo",
    instrumentos: "Instrumentos de cobrança",
    atas: "Atas de registro de preços",
    documentos_ata: "Documentos da ata"
  }

  return (
    <div className="space-y-6">
      <h2 className="text-lg font-semibold">Resultado do processamento</h2>

      <div className="grid sm:grid-cols-3 gap-4">
        <Card className="p-4 space-y-1">
          <p className="text-sm text-muted-foreground">Período:</p>
          <p className="font-medium">{formatDate(data.periodo)}</p>

          <p className="text-sm text-muted-foreground">Início processamento:</p>
          <p className="font-medium">{formatDate(data.inicio)}</p>

          <p className="text-sm text-muted-foreground">Fim processamento:</p>
          <p className="font-medium">{formatDate(data.fim)}</p>

          <p className="text-sm text-muted-foreground">Duração:</p>
          <p className="font-medium">{durationFormatted}</p>
        </Card>

        <Card className="p-4 space-y-2 col-span-2">
          <h3 className="font-medium">Entidades</h3>
          <table className="text-sm w-full">
            <thead>
              <tr className="text-muted-foreground">
                <th className="text-left font-normal">Entidades</th>
                <th className="text-right font-normal">Coleta</th>
                <th className="text-right font-normal">ETL</th>
              </tr>
            </thead>
            <tbody>
              {Object.entries(data.entidades).map(([key, [coleta, etl]]) => (
                <tr key={key}>
                  <td>{entidadesLabels[key] || key}</td>
                  <td className="text-right">{coleta}</td>
                  <td className="text-right">
                    {etl} {etl === coleta && "✓"}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </Card>

        <Card className="p-4 space-y-2">
          <h3 className="font-medium">Resumo das contratações</h3>
          <ul className="text-sm space-y-1">
            {Object.entries(data.resumo_status).map(([key, value]) => (
              <li key={key} className="flex justify-between">
                <span className="capitalize">{key}</span>
                <span>{value}</span>
              </li>
            ))}
          </ul>
        </Card>

        <Card className="p-4 space-y-2">
          <h3 className="font-medium">Dimensões</h3>
          <ul className="text-sm space-y-1">
            {Object.entries(data.dimensoes).map(([key, value]) => (
              <li key={key} className="flex justify-between">
                <span className="capitalize">{key}</span>
                <span>{value}</span>
              </li>
            ))}
          </ul>
        </Card>
      </div>
    </div>
  )
}
