"use client"

import { useState } from "react"
import { format } from "date-fns"
import { ptBR } from "date-fns/locale"
import { CalendarIcon } from "@radix-ui/react-icons"
import { Popover, PopoverContent, PopoverTrigger } from "@/components/ui/popover"
import { Button } from "@/components/ui/button"
import { Calendar } from "@/components/ui/calendar"
import { cn } from "@/lib/utils"
import { iniciarProcessamento } from "@/lib/api/processamento/iniciar"

type Props = {
  onProcessamentoIniciado?: (periodoId: number) => void
}

export function FormularioProcessamento({ onProcessamentoIniciado }: Props) {
  const [date, setDate] = useState<Date | undefined>()
  const [loading, setLoading] = useState(false)

  const handleClick = async () => {
    if (!date) return
    setLoading(true)

    try {
      const dataISO = date.toISOString().split("T")[0]
      const response = await iniciarProcessamento(dataISO)
      onProcessamentoIniciado?.(response.periodo_id)
    } catch (err) {
      console.error("Erro ao iniciar processamento", err)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="flex items-center gap-4">
      <Popover>
        <PopoverTrigger asChild>
          <Button
            variant="outline"
            className={cn("w-[280px] justify-start text-left font-normal", !date && "text-muted-foreground")}
          >
            <CalendarIcon className="mr-2 h-4 w-4" />
            {date ? format(date, "dd 'de' MMMM 'de' yyyy", { locale: ptBR }) : "Escolha uma data"}
          </Button>
        </PopoverTrigger>
        <PopoverContent className="w-auto p-0" align="start">
          <Calendar
            mode="single"
            selected={date}
            onSelect={setDate}
            initialFocus
            locale={ptBR}
          />
        </PopoverContent>
      </Popover>

      <Button onClick={handleClick} disabled={!date || loading}>
        {loading ? "Processando..." : "Iniciar processamento"}
      </Button>
    </div>
  )
}
