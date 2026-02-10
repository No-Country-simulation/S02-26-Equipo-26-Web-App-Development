export default function Input({
  label,
  required,
  placeholder,
  type = "text",
  colSpan = false,
}) {
  return (
    <div className={colSpan ? "col-span-2" : ""}>
      <label className="text-sm font-medium text-gray-700">
        {label}
        {required && <span className="text-red-500 ml-1">*</span>}
      </label>

      <input
        type={type}
        placeholder={placeholder}
        className="
          w-full px-3 py-2
          border border-gray-300 text-sm
          focus:outline-none
          rounded-md
          focus:border-yellow-400 focus:outline-none
        "
      />
    </div>
  );
}


//h-10 rounded-md border border-gray-300 px-3 text-sm focus:border-yellow-400 focus:outline-none