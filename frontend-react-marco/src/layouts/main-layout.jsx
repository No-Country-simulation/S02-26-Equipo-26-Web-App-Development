export default function MainLayout({ children }) {
  return (
    <div className="min-h-screen bg-slate-600 flex items-center justify-center">
      <div className="w-full max-w-5xl p-6">
        {children}
      </div>
    </div>
  )
}