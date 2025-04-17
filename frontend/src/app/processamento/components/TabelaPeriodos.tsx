"use client"

import { useEffect, useState } from "react"
import { Periodo } from "@/lib/api/processamento/schemas"
import { listarPeriodos } from "@/lib/api/processamento/listar"
import { format, parseISO } from "date-fns"
import { ptBR } from "date-fns/locale"
import { Skeleton } from "@/components/ui/skeleton"
import { cn } from "@/lib/utils"
import { useRouter } from "next/navigation"
import { ContadorAnimado } from "@ui/contador-animado"
import {
  CheckCircle,
  Clock,
  Loader2,
  XCircle
} from "lucide-react"

type Props = {
  periodoIdEmAndamento?: number | null
}

function StatusIcon({ status }: { status: string }) {
  switch (status) {
    case "processado":
      return <CheckCircle className="w-4 h-4 text-green-600" />
    case "pendente":
      return <Clock className="w-4 h-4 text-yellow-500 animate-pulse" />
    case "em_andamento":
      return <Loader2 className="w-4 h-4 text-blue-600 animate-spin" />
    case "falha":
      return <XCircle className="w-4 h-4 text-red-600" />
    default:
      return <Clock className="w-4 h-4 text-gray-400" />
  }
}

export function TabelaPeriodos({ periodoIdEmAndamento }: Props) {
  const [periodos, setPeriodos] = useState<Periodo[]>([])
  const [loading, setLoading] = useState(true)
  const router = useRouter()

  useEffect(() => {
    let interval: NodeJS.Timeout | null = null

    const fetchData = async () => {
      console.log("[TabelaPeriodos] Buscando períodos...")
      try {
        const dados = await listarPeriodos()
        console.log("[TabelaPeriodos] Períodos recebidos:", dados)

        setPeriodos((prev) => {
          if (JSON.stringify(prev) !== JSON.stringify(dados)) {
            console.log("[TabelaPeriodos] Atualizando tabela de períodos.")
            return dados
          } else {
            console.log("[TabelaPeriodos] Nenhuma alteração detectada.")
            return prev
          }
        })
      } catch (e) {
        console.error("[TabelaPeriodos] Erro ao carregar períodos:", e)
      } finally {
        setLoading(false)
      }
    }

    fetchData()

    interval = setInterval(() => {
      console.log("[TabelaPeriodos] Disparando atualização periódica...")
      fetchData()
    }, 5000)

    return () => {
      if (interval) {
        console.log("[TabelaPeriodos] Limpando intervalo de atualização.")
        clearInterval(interval)
      }
    }
  }, [periodoIdEmAndamento])

  if (loading) {
    return <Skeleton className="w-full h-24 rounded-md" />
  }

  if (!periodos || periodos.length === 0) {
    return (
      <div className="border rounded-md p-4 text-sm text-muted-foreground bg-muted">
        Nenhum período processado até o momento.
      </div>
    )
  }

  return (
    <div className="overflow-auto rounded-md border">
      <table className="w-full text-sm">
        <thead className="bg-gray-50 dark:bg-gray-800 text-left">
          <tr>
            <th className="p-2">Data</th>
            <th className="p-2">Status</th>
            <th className="p-2">Início</th>
            <th className="p-2">Fim</th>
            <th className="p-2">Duração</th>
            <th className="p-2">Totais</th>
            <th className="p-2">Únicas</th>
            <th className="p-2">Coleta</th>
            <th className="p-2">Entidades</th>
            <th className="p-2">ETL</th>
            <th className="p-2">Falhas</th>
          </tr>
        </thead>
        <tbody>
          {periodos.map((p) => {
            const dataFormatada = format(parseISO(p.data), "dd/MM/yyyy", { locale: ptBR })
            const inicioFormatado = p.inicio ? format(new Date(p.inicio), "HH:mm:ss") : "-"
            const fimFormatado = p.fim ? format(new Date(p.fim), "HH:mm:ss") : "-"

            return (
              <tr
                key={p.id}
                className={cn(
                  "cursor-pointer hover:bg-gray-100 transition-colors",
                  p.id === periodoIdEmAndamento && "bg-yellow-50"
                )}
                onClick={() =>
                  router.push(
                    `/processamento/${p.id}?status=${p.status}&data=${p.data}&inicio=${p.inicio || ""}&fim=${p.fim || ""}`
                  )
                }
              >
                <td className="p-2">{dataFormatada}</td>
                <td className="p-2 flex items-center gap-2 capitalize">
                  <StatusIcon status={p.status} />
                  {p.status}
                </td>
                <td className="p-2">{inicioFormatado}</td>
                <td className="p-2">{fimFormatado}</td>
                <td className="p-2">{p.duracao || "-"}</td>
                <td className="p-2"><ContadorAnimado valor={p.totais} /></td>
                <td className="p-2"><ContadorAnimado valor={p.unicas} /></td>
                <td className="p-2"><ContadorAnimado valor={p.contratacoes_raw} /></td>
                <td className="p-2"><ContadorAnimado valor={p.entidades_raw} /></td>
                <td className="p-2"><ContadorAnimado valor={p.contratacoes_dw} /></td>
                <td className="p-2"><ContadorAnimado valor={p.falhas} /></td>
              </tr>
            )
          })}
        </tbody>
      </table>
    </div>
  )
}
