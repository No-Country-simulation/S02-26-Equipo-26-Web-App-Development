function ModalFooter({ currentStep, totalSteps, onCancel, onNext }) {
  const isLastStep = currentStep === totalSteps;

  return (
    <div className="flex justify-end gap-3">
      
      {/* Botón Cancelar */}
      <button
        type="button"
        onClick={onCancel}
        className="px-4 py-2 rounded-lg border border-gray-300 text-gray-600 hover:bg-gray-100 transition"
      >
        Cancelar
      </button>

      {/* Botón dinámico */}
      {!isLastStep ? (
        <button
          type="button"
          onClick={onNext}
          className="px-4 py-2 rounded-lg bg-yellow-400 text-black hover:bg-yellow-500 font-medium transition"
        >
          Continuar
        </button>
      ) : (
        <button
          type="submit"
          className="px-4 py-2 rounded-lg bg-green-600 hover:bg-green-700 text-white font-medium transition"
        >
          Guardar cambios
        </button>
      )}
    </div>
  );
}

export default ModalFooter;

