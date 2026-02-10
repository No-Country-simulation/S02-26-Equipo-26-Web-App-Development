export default function Select({
  label,
  options = [],
  placeholder = "Seleccionar",
}) 
{
  return (
    <div className="flex flex-col gap-1">
      {label && (
        <label className="text-sm font-medium text-gray-700">
          {label}
        </label>
      )}

      <select className="h-10 rounded-md border border-gray-300 px-3 text-sm focus:border-yellow-400 focus:outline-none">
        <option value="">{placeholder}</option>

        {options.map((opt) => (
          <option
            key={opt.value}     
            value={opt.value}    
          >
            {opt.label}          
          </option>
        ))}
      </select>
    </div>
  )
}
