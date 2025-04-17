"use client"

import { useEffect, useState } from "react"
import { Skeleton } from "@/components/ui/skeleton"
import { obterResumo } from "@/lib/api/processamento/resumo"
import type { ResumoProcessamento } from "@/lib/api/processamento/schemas"
import { CheckCircle, AlertTriangle } from "lucide-react"

type Props = {
  periodoId: number
}

export default function ResumoProcessamento({ periodoId }: Props) {
  const [dados, setDados] = useState<ResumoProcessamento | null>(null)
  const [erro, setErro] = useState<string | null>(null)

  useEffect(() => {
    const fetchResumo = async () => {
      try {
        const resultado = await obterResumo(periodoId)
        setDados(resultado)
      } catch (err) {
        console.error("Erro ao obter resumo:", err)
        setErro("Erro ao carregar resumo do processamento.")
      }
    }

    fetchResumo()
  }, [periodoId])

  if (erro) {
    return <div className="text-sm text-red-500">{erro}</div>
  }

  if (!dados) {
    return <Skeleton className="h-40 w-full" />
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
      {/* ENTIDADES */}
      <div>
        <h2 className="text-sm font-medium mb-2">Entidades</h2>
        <table className="text-sm w-full">
          <thead>
            <tr className="text-muted-foreground border-b">
              <th className="text-left">Entidade</th>
              <th className="text-right">Coleta</th>
              <th className="text-right">ETL</th>
            </tr>
          </thead>
          <tbody>
            {dados.entidades.map(ent => (
              <tr key={ent.nome} className="border-t">
                <td>{ent.nome}</td>
                <td className="text-right">{ent.coleta}</td>
                <td className="text-right flex justify-end items-center gap-2">
                  <span>{ent.etl}</span>
                  {ent.coleta === ent.etl ? (
                    <CheckCircle className="w-4 h-4 text-green-600" aria-label="Coleta e ETL consistentes" />
                  ) : (
                    <AlertTriangle className="w-4 h-4 text-yellow-500" aria-label="Inconsistência entre coleta e ETL" />
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* DIMENSÕES */}
      <div>
        <h2 className="text-sm font-medium mb-2">Dimensões</h2>
        <table className="text-sm w-full">
          <thead>
            <tr className="text-muted-foreground border-b">
              <th className="text-left">Dimensão</th>
              <th className="text-right">Total</th>
            </tr>
          </thead>
          <tbody>
            {dados.dimensoes.map(dim => (
              <tr key={dim.nome} className="border-t">
                <td>{dim.nome}</td>
                <td className="text-right">{dim.valor}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}
