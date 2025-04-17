import { api } from "../../http"
import { ProgressoColetaSchema } from "./schemas"

export async function obterProgresso(periodoId: number) {
  const res = await api.get(`/processamento/${periodoId}/progresso`)
  return ProgressoColetaSchema.parse(res.data)
}
