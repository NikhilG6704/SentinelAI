import { FiAlertCircle, FiLoader } from "react-icons/fi";

interface QueryStateProps {
  isLoading?: boolean;
  isError?: boolean;
  errorMessage?: string;
  children: React.ReactNode;
}

function QueryState({
  isLoading = false,
  isError = false,
  errorMessage = "Unable to load this data.",
  children,
}: QueryStateProps) {
  if (isLoading) {
    return (
      <div className="flex min-h-40 items-center justify-center rounded-xl border border-zinc-800/80 bg-zinc-900/40">
        <div className="flex items-center gap-3 text-sm text-zinc-400">
          <FiLoader className="h-4 w-4 animate-spin" />
          Loading data...
        </div>
      </div>
    );
  }

  if (isError) {
    return (
      <div className="flex min-h-40 items-center justify-center rounded-xl border border-red-500/20 bg-red-500/5 px-6">
        <div className="flex items-center gap-3 text-sm text-red-400">
          <FiAlertCircle className="h-4 w-4 shrink-0" />
          {errorMessage}
        </div>
      </div>
    );
  }

  return <>{children}</>;
}

export default QueryState;
