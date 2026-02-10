import { Upload } from "lucide-react"
import { useRef, useState } from "react"

export default function FileUpload({ label, required = false, helper, accept }) {

  const fileInputRef = useRef(null)
  const [fileName, setFileName] = useState(null)

  const handleClick = () => {
    fileInputRef.current.click()
  }

  const handleChange = (e) => {
    const file = e.target.files[0]
    if (file) {
      setFileName(file.name)
    }
  }

  return (
    <div className="space-y-2">

      {/* Label */}
      <label className="text-sm font-medium text-gray-700">
        {label} {required && <span className="text-red-500">*</span>}
      </label>

      {/* Área Upload */}
      <div
        onClick={handleClick}
        className="flex cursor-pointer flex-col items-center justify-center gap-2 rounded-lg border-2 border-dashed border-gray-300 bg-gray-50 px-4 py-6 text-center hover:border-yellow-500 hover:bg-yellow-50 transition"
      >
        <Upload className="h-6 w-6 text-gray-400 " />

        <p className="text-sm text-gray-600 ">
          {fileName ? "Cambiar archivo" : "hacé click para subir"}
        </p>

        <p className="text-xs text-gray-400">{helper}</p>

        {fileName && (
          <p className="text-xs text-gray-600 mt-1 ">
            Archivo: {fileName}
          </p>
        )}
      </div>

      {/* Input oculto real */}
      <input
        type="file"
        ref={fileInputRef}
        onChange={handleChange}
        accept={accept}
        className="hidden"
      />

    </div>
  )
}
