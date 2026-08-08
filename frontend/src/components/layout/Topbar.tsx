import { FiBell, FiChevronDown, FiSearch } from "react-icons/fi";

function Topbar() {
  return (
    <header className="flex h-16 shrink-0 items-center justify-between border-b border-zinc-800/80 bg-zinc-950 px-6">
      {/* Left side */}
      <div>
        <p className="text-sm font-medium text-zinc-200">
          Enterprise Operations
        </p>

        <p className="text-xs text-zinc-500">
          Infrastructure monitoring & AI intelligence
        </p>
      </div>

      {/* Right side */}
      <div className="flex items-center gap-3">
        {/* Search */}
        <button
          type="button"
          className="hidden items-center gap-3 rounded-lg border border-zinc-800 bg-zinc-900/50 px-3 py-2 transition-colors hover:border-zinc-700 hover:bg-zinc-900 md:flex"
        >
          <FiSearch className="h-4 w-4 text-zinc-500" />

          <span className="text-xs text-zinc-500">Search SentinelAI</span>

          <kbd className="ml-4 rounded border border-zinc-700 px-1.5 py-0.5 text-[10px] text-zinc-500">
            ⌘ K
          </kbd>
        </button>

        {/* Notifications */}
        <button
          type="button"
          aria-label="Notifications"
          className="relative rounded-lg p-2 text-zinc-400 transition-colors hover:bg-zinc-800 hover:text-zinc-100"
        >
          <FiBell className="h-[18px] w-[18px]" />

          <span className="absolute right-1.5 top-1.5 h-1.5 w-1.5 rounded-full bg-red-500" />
        </button>

        {/* User */}
        <button
          type="button"
          className="flex items-center gap-3 rounded-lg px-2 py-1.5 transition-colors hover:bg-zinc-900"
        >
          <div className="flex h-8 w-8 items-center justify-center rounded-full bg-blue-500/10 text-xs font-semibold text-blue-400 ring-1 ring-blue-500/20">
            AD
          </div>

          <div className="hidden text-left sm:block">
            <p className="text-xs font-medium text-zinc-200">Administrator</p>

            <p className="text-[10px] text-zinc-500">System Admin</p>
          </div>

          <FiChevronDown className="hidden h-3.5 w-3.5 text-zinc-500 sm:block" />
        </button>
      </div>
    </header>
  );
}

export default Topbar;
