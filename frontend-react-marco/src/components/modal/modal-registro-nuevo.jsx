import { X } from "lucide-react"
import { useState } from "react"
import StepBar from "../ui/stepBar"
import StepDatosPersonales from "../ui/step-datos-personales"
import StepDatosProfesionales from "../ui/step-datos-profesionales"
import StepDatosBancarios from "../ui/step-datos-bancarios"
import StepDocumentacion from "../ui/step-documentos"

export default function ModalRegistroNuevo({ isOpen, onClose, children }) {
  const [currentStep, setCurrentStep] = useState(1)
  if (!isOpen) return null

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50"> 
      <div className="relative w-full max-w-3xl rounded-xl bg-white shadow-xl">
        
        {/* HEADER MODAL*/}
        <div className="flex items-start justify-between px-6 py-4">
          {/* Title and description*/}
          <div>
            <h2 className="text-lg font-semibold text-gray-900">
              Registrar nuevo cuidador
            </h2>
            <p className="text-sm text-gray-500">
              Completá los datos para dar de alta un nuevo cuidador.
            </p>
          </div>
          {/* Button close*/}
          <button onClick={onClose} className="rounded-md p-2 text-gray-400 hover:bg-gray-100 hover:text-red-500">
            <X size={18} />
          </button>
        </div>

        {/* Stepbar*/}
        <div className="px-6 py-1">
          <StepBar currentStep={currentStep} onStepChange={setCurrentStep}/>
        </div>

        {/* BODY */}
        <div className="px-6 py-6">
          {children}
            {currentStep === 1 && <StepDatosPersonales />}
            {currentStep === 2 && <StepDatosProfesionales />}
            {currentStep === 3 && <StepDatosBancarios />}
            {currentStep === 4 && <StepDocumentacion />}
        </div>

        {/* Footer */}
        <div className="flex items-center justify-between border-t px-6 py-4">
          {/* Botón Cancelar */}
          <button
            onClick={onClose}
            className="rounded-md border px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
          >
            Cancelar
          </button>
          {/* Botones de acción */}
          <div className="flex gap-3">
            {currentStep < 4 && (
              <button
                onClick={() => setCurrentStep((prev) => prev + 1)}
                className="rounded-md bg-yellow-400 px-6 py-2 text-sm font-medium text-black hover:bg-yellow-500 transition"
              >
                Siguiente
              </button>
            )}

            {currentStep === 4 && (
              <button
                className="flex items-center gap-2 rounded-md bg-green-600 px-6 py-2 text-sm font-medium text-white hover:bg-green-700 transition"
              >
                Guardar cambios
              </button>
            )}
          </div>
        </div>

          
      </div>
    </div>
  )
}
