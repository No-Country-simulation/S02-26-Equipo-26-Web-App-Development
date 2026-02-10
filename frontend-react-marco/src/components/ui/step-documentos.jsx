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
    accept="application/pdf,image/png,image/jpeg"
  />

  <FileUpload
    label="DNI (Dorso)"
    required
    helper="PDF, JPG o PNG hasta 5MB"
    accept="application/pdf,image/png,image/jpeg"
  />

  <FileUpload
    label="Certificado de Antecedentes"
    required
    helper="PDF hasta 5MB"
    accept="application/pdf"
  />

  <FileUpload
    label="Curriculum Vitae"
    helper="PDF hasta 5MB"
    accept="application/pdf"
  />
</div>
    </div>
  )
}

