import Input from "./inputs/Input";
import Select from "./inputs/Select";
import { Upload } from "lucide-react";
import { useRef } from "react";

const generoOptions = [
  { value: "masculino", label: "Masculino" },
  { value: "femenino", label: "Femenino" },
  { value: "no_binario", label: "No binario" },
  { value: "otro", label: "Otro" },
  { value: "prefiero_no_decir", label: "Prefiero no decir" },
];

export default function StepDatosPersonales({ formData, setFormData }) {
    const fileInputRef = useRef(null);

  const handleClick = () => {
    fileInputRef.current.click();
  };
  return (
    <div className="space-y-6">
      {/* Foto */}
<div className="flex items-center gap-6 pb-6">

  {/* FOTO CIRCULAR MÁS GRANDE */}
  <div className="w-32 h-32 rounded-full bg-gray-100  flex items-center justify-center overflow-hidden">
    <span className="text-gray-400 text-sm">Sin foto</span>
  </div>

  {/* INFO + BOTÓN */}
  <div>
    <p className="text-sm font-medium text-gray-800">
      Foto de perfil
    </p>

    <p className="text-xs text-gray-500 mb-3">
      JPG o PNG. Máximo 2MB.
    </p>

    <button
      type="button"
      onClick={handleClick}
      className="px-4 py-2 text-sm font-medium rounded-md  border border-gray-300 hover:bg-gray-50 transition"
    >
      Subir foto
      <Upload size={16} className="inline-block ml-2" />
    </button>

    <input
      type="file"
      accept="image/png, image/jpeg"
      ref={fileInputRef}
      className="hidden"
    />
  </div>

</div>
  {/* Input oculto */}
  <input
    type="file"
    accept="image/png, image/jpeg"
    ref={fileInputRef}
    className="hidden"
  />

      {/* Form */}
      <div className="grid grid-cols-2 gap-4">
        <Input
        required
        label="Nombre"
        placeholder="Ingrese nombre"
        value={formData.nombre}
        onChange={(e) =>
        setFormData({ ...formData, nombre: e.target.value })
  }
/>
        <Input label="Apellido" placeholder="Ingrese apellido" required />

        <Input label="DNI" placeholder="XX.XXX.XXX" required/>
        <Input label="Fecha de nacimiento" type="date" required />

      <Select
        label="Género"
        placeholder="Seleccionar"
        options={generoOptions}
      />

        <Input label="Teléfono" placeholder="+54 9 11 XXXX-XXXX" />

        <Input
          label="Email"
          placeholder="ejemplo@email.com"
          type="email"
          colSpan
          required
        />

        <Input
          label="Dirección "
          placeholder="Calle, número, piso, depto"
          colSpan
          required
        />

        <Input label="Ciudad" placeholder="Ciudad" />
        <Input label="Código Postal" placeholder="XXXX" />
      </div>

      <p className="text-xs text-gray-500">
        <span className="text-red-500">*</span> Campos obligatorios
      </p>
    </div>
  );
}
