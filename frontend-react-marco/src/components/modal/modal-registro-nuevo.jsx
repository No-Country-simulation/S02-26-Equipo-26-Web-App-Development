import { X } from "lucide-react"
import { Pizza } from 'lucide-react';


export default function ModalRegistroNuevo({ isOpen, onClose, children }) {
  if (!isOpen) return null

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/80">
      
      <div className="relative w-full max-w-3xl rounded-xl bg-white shadow-xl">
        
        {/* HEADER MODAL*/}
        <div className="flex items-start justify-between border-b px-6 py-4">
          <div>
            <h2 className="text-lg font-semibold text-gray-900">
              Registrar nuevo cuidador
            </h2>
            <p className="text-sm text-gray-500">
              Completá los datos para dar de alta un nuevo cuidador.
            </p>
          </div>

          <button
            onClick={onClose}
            className="rounded-md p-2 text-gray-400 hover:bg-gray-100 hover:text-red-500"
          >
            <Pizza size={18} />
          </button>
        </div>

        {/* BODY */}
        <div className="px-6 py-6">
          {children}
        </div>

      </div>
    </div>
  )
}
