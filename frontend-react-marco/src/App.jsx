import { useState } from "react"
import MainLayout from "./layouts/main-layout"
import ModalRegistroNuevo from "./components/modal/modal-registro-nuevo"

export default function App() {
  const [open, setOpen] = useState(false)

  return (
    <MainLayout>
      {/* Botón para abrir modal */}
      <button
        onClick={() => setOpen(true)}
        className="bg-green-600 text-white px-4 py-2 rounded"
      >
        Abrir modal
      </button>

      {/* Modal */}
<ModalRegistroNuevo isOpen={open} onClose={() => setOpen(false)}>

</ModalRegistroNuevo>
    </MainLayout>
  )
}
