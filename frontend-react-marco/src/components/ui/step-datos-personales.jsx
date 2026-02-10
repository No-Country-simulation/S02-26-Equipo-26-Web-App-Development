import Input from "./inputs/Input";
import Select from "./inputs/Select";

const generoOptions = [
  { value: "masculino", label: "Masculino" },
  { value: "femenino", label: "Femenino" },
  { value: "no_binario", label: "No binario" },
  { value: "otro", label: "Otro" },
  { value: "prefiero_no_decir", label: "Prefiero no decir" },
];

export default function StepDatosPersonales() {
  return (
    <div className="space-y-6">
      {/* Foto */}
      <div className="flex items-center gap-6">
        <div className="w-24 h-24 rounded-full bg-gray-200 flex items-center justify-center">
          <span className="text-gray-400 text-sm">Foto</span>
        </div>

        <div>
          <p className="text-sm font-medium">Foto de perfil</p>
          <p className="text-xs text-gray-500">
            JPG o PNG. Máximo 2MB.
          </p>

          <button className="mt-2 px-4 py-1.5 border rounded-md text-sm hover:bg-gray-50">
            Subir foto
          </button>
        </div>
      </div>

      {/* Form */}
      <div className="grid grid-cols-2 gap-4">
        <Input label="Nombre *" placeholder="Ingrese nombre" />
        <Input label="Apellido *" placeholder="Ingrese apellido" />

        <Input label="DNI *" placeholder="XX.XXX.XXX" />
        <Input label="Fecha de nacimiento *" type="date" />

      <Select
        label="Género"
        placeholder="Seleccionar"
        options={generoOptions}
      />

        <Input label="Teléfono *" placeholder="+54 9 11 XXXX-XXXX" />

        <Input
          label="Email *"
          placeholder="ejemplo@email.com"
          type="email"
          colSpan
        />

        <Input
          label="Dirección *"
          placeholder="Calle, número, piso, depto"
          colSpan
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
