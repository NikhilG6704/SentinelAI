import { FiSearch, FiX } from "react-icons/fi";

interface InfrastructureFiltersProps {
  search: string;
  status: string;
  onSearchChange: (value: string) => void;
  onStatusChange: (value: string) => void;
  onClear: () => void;
}

function InfrastructureFilters({
  search,
  status,
  onSearchChange,
  onStatusChange,
  onClear,
}: InfrastructureFiltersProps) {
  const hasFilters = search.length > 0 || status !== "all";

  return (
    <div className="rounded-xl border border-zinc-800/80 bg-zinc-900/40 p-4">
      <div className="flex flex-col gap-3 lg:flex-row lg:items-center">
        <div className="relative flex-1">
          <FiSearch className="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-zinc-600" />

          <input
            type="text"
            value={search}
            onChange={(event) => onSearchChange(event.target.value)}
            placeholder="Search hostname, IP address, or asset ID..."
            className="h-10 w-full rounded-lg border border-zinc-800 bg-zinc-950/60 pl-9 pr-3 text-sm text-zinc-200 outline-none transition-colors placeholder:text-zinc-700 focus:border-blue-500/40"
          />
        </div>

        <select
          value={status}
          onChange={(event) => onStatusChange(event.target.value)}
          className="h-10 rounded-lg border border-zinc-800 bg-zinc-950/60 px-3 text-sm text-zinc-300 outline-none focus:border-blue-500/40"
        >
          <option value="all">All statuses</option>
          <option value="Healthy">Healthy</option>
          <option value="Warning">Warning</option>
          <option value="Critical">Critical</option>
          <option value="Offline">Offline</option>
        </select>

        {hasFilters && (
          <button
            type="button"
            onClick={onClear}
            className="flex h-10 items-center justify-center gap-2 rounded-lg border border-zinc-800 px-3 text-xs font-medium text-zinc-400 transition-colors hover:bg-zinc-800/50 hover:text-zinc-200"
          >
            <FiX className="h-3.5 w-3.5" />
            Clear
          </button>
        )}
      </div>
    </div>
  );
}

export default InfrastructureFilters;
