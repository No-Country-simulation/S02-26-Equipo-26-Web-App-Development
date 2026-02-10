import { X } from "lucide-react"
import { useState } from "react"
import StepBar from "../ui/stepBar"
import StepDatosPersonales from "../ui/step-datos-personales"
import StepDatosProfesionales from "../ui/step-datos-profesionales"
import StepDatosBancarios from "../ui/step-datos-bancarios"
import StepDocumentacion from "../ui/step-documentos"
import ModalFooter from "../ui/inputs/footer-modal"

export default function ModalRegistroNuevo({ isOpen, onClose, children }) {
  const [currentStep, setCurrentStep] = useState(1)
  if (!isOpen) return null

  const totalSteps = 4

  const handleNext = () => {
    if (currentStep < totalSteps) {
      setCurrentStep(currentStep + 1)
    }
  }

  const handleCancel = () => {
    onClose()
  }

  const handleSave = () => {
    console.log("Guardar cambios")
    onClose()
  }

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
        <div className="px-6 pb-6">
          <ModalFooter
            currentStep={currentStep}
            totalSteps={totalSteps}
            onCancel={handleCancel}
            onNext={handleNext}
            onSave={handleSave}
          />
        </div>
        

          
      </div>
    </div>
  )
}
