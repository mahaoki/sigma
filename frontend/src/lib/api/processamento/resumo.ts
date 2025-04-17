import { api } from "../../http"
import { ResumoProcessamentoSchema } from "./schemas"

export async function obterResumo(periodoId: number) {
  const res = await api.get(`/processamento/${periodoId}/resumo`)
  return ResumoProcessamentoSchema.parse(res.data)
}
