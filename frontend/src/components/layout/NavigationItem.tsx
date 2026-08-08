import { NavLink } from "react-router-dom";
import type { IconType } from "react-icons";

interface NavigationItemProps {
  label: string;
  path: string;
  icon: IconType;
}

function NavigationItem({ label, path, icon: Icon }: NavigationItemProps) {
  return (
    <NavLink
      to={path}
      className={({ isActive }) =>
        [
          "group flex items-center gap-3 rounded-lg px-3 py-2",
          "text-sm font-medium transition-colors duration-150",
          isActive
            ? "bg-blue-500/10 text-blue-400"
            : "text-zinc-400 hover:bg-zinc-900 hover:text-zinc-200",
        ].join(" ")
      }
    >
      {({ isActive }) => (
        <>
          <Icon
            className={
              isActive
                ? "h-[17px] w-[17px] text-blue-400"
                : "h-[17px] w-[17px] text-zinc-500 group-hover:text-zinc-300"
            }
          />

          <span>{label}</span>
        </>
      )}
    </NavLink>
  );
}

export default NavigationItem;
