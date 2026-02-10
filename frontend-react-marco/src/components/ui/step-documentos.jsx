import FileUpload from "./inputs/FileUpload"

export default function StepDocumentos() {
  return (
    <div className="space-y-6">
      
      {/* Info box */}
      <div className="rounded-lg border border-blue-200 bg-blue-50 px-4 py-3 text-sm text-blue-700">
        <strong>Documentación requerida:</strong> Por favor suba los siguientes
        documentos para completar el registro. Los archivos deben estar en
        formato PDF, JPG o PNG.
      </div>

      {/* Grid de uploads */}
      <div className="grid grid-cols-1 gap-6 md:grid-cols-2">
        <FileUpload
          label="DNI (Frente)"
          required
          helper="PDF, JPG o PNG hasta 5MB"
        />

        <FileUpload
          label="DNI (Dorso)"
          required
          helper="PDF, JPG o PNG hasta 5MB"
        />

        <FileUpload
          label="Certificado de Antecedentes"
          required
          helper="PDF hasta 5MB"
        />

        <FileUpload
          label="Curriculum Vitae"
          helper="PDF hasta 5MB"
        />
      </div>

      {/* Documentos cargados */}
      <div className="space-y-2">
        <p className="text-sm font-medium text-gray-700">
          Documentos cargados
        </p>

        <div className="rounded-lg border bg-gray-50 px-4 py-3 text-sm text-gray-500">
          No hay documentos cargados aún
        </div>
      </div>
    </div>
  )
}

