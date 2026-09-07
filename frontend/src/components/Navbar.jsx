function Navbar() {
  return (
    <nav className="border-b border-white/10 bg-[#0b0f15]">
      <div className="mx-auto flex max-w-7xl items-center justify-between px-6 py-5">
        
        <div className="flex gap-4">
          <img
            src="https://cdn-icons-png.flaticon.com/512/10595/10595761.png"
            alt="NetSage AI"
            className="h-12 w-12 object-contain"
          />
          <div>
            <h2 className="text-xl font-semibold">
              NetSage{" "}
              <span className="text-sky-400">AI</span>
            </h2>

            <p className="text-xs text-gray-500">
              Network Troubleshooting Assistant
            </p>
          </div>
          
          
        </div>

        <div className="rounded-full border border-sky-400/20 bg-sky-400/5 px-4 py-2 text-xs text-sky-300">
          Human Review Required
        </div>
      </div>
    </nav>
  );
}

export default Navbar;