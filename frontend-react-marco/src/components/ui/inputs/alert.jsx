export default function Alert({ children }) {
  return (
    <div className="rounded-lg border border-yellow-300 bg-yellow-50 px-4 py-3 text-sm text-yellow-800">
      <strong className="font-medium">Importante:</strong>{" "}
      {children}
    </div>
  )
}
