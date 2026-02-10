import Input from "./inputs/input";
import Select from "./inputs/Select";

const turnosOptions = [
  { value: "manana", label: "Mañana" },
  { value: "tarde", label: "Tarde" },
  { value: "noche", label: "Noche" },
];

const matriculaOptions = [
{ value: "si", label: "Sí" },
{ value: "no", label: "No" },
];

const tiposCuidadorOptions = [
    { value: "acomp_terapeutico", label: "Acompañante terapéutico" },
    { value: "cuidador_domiciliario", label: "Cuidador domiciliario" },
    { value: "enfermero", label: "Enfermero/a" },
];

const nivelEstudiosOptions = [
{ value: "primario", label: "Primario completo" },
{ value: "secundario", label: "Secundario completo" },
{ value: "terciario", label: "Terciario en curso" },
{ value: "terciario_completo", label: "Terciario completo" },
{ value: "universitario", label: "Universitario en curso" },
{ value: "universitario_completo", label: "Universitario completo" },
];

export default function StepDatosProfesionales() {
  return (
    <div className="space-y-6">
      <div className="grid grid-cols-2 gap-4">
        <Select
          label="Tipo de cuidador"
          options={tiposCuidadorOptions}
        />

      <Select
        label="Turno disponible"
        placeholder="Seleccionar turno"
        options={turnosOptions}
      />

        <Input
          label="Años de experiencia"
          placeholder="Ej: 3"
        />

        <Select
          label="Nivel de estudios"
          options={nivelEstudiosOptions}
        />

        <Input
          label="Institución / Curso"
          placeholder="Nombre de institución"
          colSpan
        />

        <Select
          label="¿Posee matrícula?"
          options={matriculaOptions}
        />

        <Input
          label="Número de matrícula"
          placeholder="Solo si aplica"
        />
      </div>
    </div>
  );
}
