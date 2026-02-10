import Input from "./inputs/input";
import Select from "./inputs/Select";
import Alert from "./inputs/alert";

export default function StepDatosBancarios() {
  return (
    <div className="space-y-6">

      <Alert>
        Los datos bancarios son necesarios para procesar los pagos mensuales.
        Puede elegir recibir pagos por transferencia bancaria o Mercado Pago.
      </Alert>

      <div className="grid grid-cols-1 gap-4 md:grid-cols-2">
        <Select
          label="Tipo de cuenta"
          placeholder="Seleccionar tipo"
          options={[
            { value: "caja_ahorro", label: "Caja de ahorro" },
            { value: "cuenta_corriente", label: "Cuenta corriente" },
          ]}
        />

        <Input
          label="Banco"
          placeholder="Nombre del banco"
        />

        <Input
          label="CBU"
          placeholder="22 dígitos"
        />

        <Input
          label="Alias CBU"
          placeholder="mi.alias.cbu"
        />
      </div>

      <Input
        label="CVU Mercado Pago (opcional)"
        placeholder="CVU de Mercado Pago (22 dígitos)"
      />
    </div>
  )
}
