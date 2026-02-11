import { X } from "lucide-react"
import { useState, useEffect } from "react"
import StepBar from "../ui/stepBar"
import StepDatosPersonales from "../ui/step-datos-personales"
import StepDatosProfesionales from "../ui/step-datos-profesionales"
import StepDatosBancarios from "../ui/step-datos-bancarios"
import StepDocumentacion from "../ui/step-documentos"
import ModalFooter from "../ui/inputs/footer-modal"

export default function ModalRegistroNuevo({ isOpen, onClose, children }) {
  const [currentStep, setCurrentStep] = useState(1)

  const [formData, setFormData] = useState({
    // Step 1
    nombre: "",
    apellido: "",
    dni: "",
    fechaNacimiento: "",
    genero: "",
    telefono: "",
    email: "",
    direccion: "",
    ciudad: "",
    codigoPostal: "",
    foto: null,

    // Step 4
    dniFrente: null,
    dniDorso: null,
    antecedentes: null,
    cv: null,
  })
  useEffect(() => {
    if (isOpen) {
      setCurrentStep(1)
    }
  }, [isOpen])

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
    console.log("Datos completos:", formData)
    onClose()
  }

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50">
      <div className="relative w-full max-w-3xl rounded-xl bg-white shadow-xl">

        {/* HEADER */}
        <div className="flex items-start justify-between px-6 py-4">
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
            <X size={18} />
          </button>
        </div>

        {/* STEP BAR */}
        <div className="px-6 py-1">
          <StepBar
            currentStep={currentStep}
            onStepChange={setCurrentStep}
          />
        </div>

        {/* BODY */}
        <div className="px-6 py-6">
          {children}

          {currentStep === 1 && (
            <StepDatosPersonales
              formData={formData}
              setFormData={setFormData}
            />
          )}

          {currentStep === 2 && <StepDatosProfesionales />}

          {currentStep === 3 && <StepDatosBancarios />}

          {currentStep === 4 && (
            <StepDocumentacion
              formData={formData}
              setFormData={setFormData}
            />
          )}
        </div>

        {/* FOOTER */}
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
