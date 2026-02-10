export default function Input({
  label,
  placeholder,
  type = "text",
  colSpan = false,
}) {
  return (
    <div className={colSpan ? "col-span-2" : ""}>
      <label className="block mb-1 text-sm font-medium">
        {label}
      </label>

      <input
        type={type}
        placeholder={placeholder}
        className="
          w-full px-3 py-2
          border rounded-md text-sm
          focus:outline-none
          focus:ring-2 focus:ring-yellow-400
        "
      />
    </div>
  );
}
