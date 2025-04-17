"use client"

import { useEffect, useState } from "react"
import { useMotionValue, animate, useTransform } from "framer-motion"

type Props = {
  valor: number
  prefixo?: string
  sufixo?: string
  decimais?: number
}

export function ContadorAnimado({
  valor,
  prefixo = "",
  sufixo = "",
  decimais = 0
}: Props) {
  const motionValue = useMotionValue(0)
  const [output, setOutput] = useState("0")

  const valorFormatado = useTransform(motionValue, (v) =>
    `${prefixo}${v.toFixed(decimais).replace(/\B(?=(\d{3})+(?!\d))/g, ".")}${sufixo}`
  )

  useEffect(() => {
    const controls = animate(motionValue, valor, {
      duration: 0.8,
      ease: "easeOut"
    })

    return controls.stop
  }, [valor])

  useEffect(() => {
    const unsubscribe = valorFormatado.on("change", (v) => {
      setOutput(v)
    })
    return () => unsubscribe()
  }, [valorFormatado])

  return <span>{output}</span>
}
