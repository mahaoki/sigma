import { z } from "zod"

// Inicar processamento
export const ProcessamentoResponseSchema = z.object({
  mensagem: z.string(),
  periodo_id: z.number()
})

export type ProcessamentoResponse = z.infer<typeof ProcessamentoResponseSchema>

// Tabela de periodos de processamento
export const PeriodoSchema = z.object({
  id: z.number(),
  data: z.string(), // "2025-04-10"
  status: z.string(), // "pendente", "processado", etc
  inicio: z.string().nullable(), // ISO string ou null
  fim: z.string().nullable(),    // ISO string ou null
  duracao: z.string(),           // "00:02:15" ou ""
  totais: z.number(),
  unicas: z.number(),
  contratacoes_raw: z.number(),
  entidades_raw: z.number(),
  contratacoes_dw: z.number(),
  falhas: z.number()
})

// Progresso do processamento
export const PeriodosResponseSchema = z.array(PeriodoSchema)

export type Periodo = z.infer<typeof PeriodoSchema>

// Progresso do processamento
export const ProgressoColetaSchema = z.object({
  verificadas: z.number(),
  coletadas_raw: z.number(),
  completas_raw: z.number()
})

export type ProgressoColeta = z.infer<typeof ProgressoColetaSchema>

// Resumo do processamento
export const EntidadeResumoSchema = z.object({
  nome: z.string(),
  coleta: z.number(),
  etl: z.number()
})

export const DimensaoResumoSchema = z.object({
  nome: z.string(),
  valor: z.number()
})

export const ResumoProcessamentoSchema = z.object({
  entidades: z.array(EntidadeResumoSchema),
  dimensoes: z.array(DimensaoResumoSchema)
})

export type ResumoProcessamento = z.infer<typeof ResumoProcessamentoSchema>
