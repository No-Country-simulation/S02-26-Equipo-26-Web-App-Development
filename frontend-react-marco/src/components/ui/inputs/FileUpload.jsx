import { Upload } from "lucide-react"

export default function FileUpload({ label, required = false, helper }) {
  return (
    <div className="space-y-2">
      <label className="text-sm font-medium text-gray-700">
        {label} {required && <span className="text-red-500">*</span>}
      </label>

      <div className="flex flex-col items-center justify-center gap-2 rounded-lg border-2 border-dashed border-gray-300 bg-gray-50 px-4 py-6 text-center">
        <Upload className="h-6 w-6 text-gray-400" />
        <p className="text-sm text-gray-600">
          Arrastrá o hacé click para subir
        </p>
        <p className="text-xs text-gray-400">{helper}</p>
      </div>
    </div>
  )
}
