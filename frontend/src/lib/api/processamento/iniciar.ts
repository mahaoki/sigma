import { api } from "../../http"
import { ProcessamentoResponseSchema } from "./schemas"

/**
 * Inicia o processamento para uma data (data_processamento).
 * A data deve estar no formato ISO 8601 (yyyy-MM-dd).
 */
export async function iniciarProcessamento(data_processamento: string) {
  const res = await api.post("/processamento/iniciar", {
    data_processamento
  })
  return ProcessamentoResponseSchema.parse(res.data)
}
