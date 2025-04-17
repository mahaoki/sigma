import { api } from "../../http"
import { PeriodosResponseSchema } from "./schemas"

export async function listarPeriodos() {
  const res = await api.get("/processamento/periodos")
  return PeriodosResponseSchema.parse(res.data)
}
