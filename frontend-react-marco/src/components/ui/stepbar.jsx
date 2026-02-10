import { User, Briefcase, CreditCard, FileText } from "lucide-react"

const steps = [
  { id: 1, label: "Datos Personales", icon: User },
  { id: 2, label: "Datos Profesionales", icon: Briefcase },
  { id: 3, label: "Datos Bancarios", icon: CreditCard },
  { id: 4, label: "Documentos", icon: FileText },
]

export default function StepBar({ currentStep, onStepChange }) {
  return (
    <div className="flex gap-4">
      {steps.map((step) => {
        const Icon = step.icon
        const isActive = currentStep === step.id

        return (
          <button
            key={step.id}
            onClick={() => onStepChange(step.id)}
            className={`
              flex items-center gap-2 rounded-md px-4 py-2 text-sm font-medium
              transition
              ${
                isActive
                  ? "bg-yellow-400 text-black"
                  : "border border-gray-200 text-gray-500 hover:bg-gray-100"
              }
            `}
          >
            <Icon size={16} />
            {step.label}
          </button>
        )
      })}
    </div>
  )
}
