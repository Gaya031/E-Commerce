import { useSearchParams } from "react-router-dom";

import { Input } from "../ui/input";
import StoreDepartments from "./StoreDepartments";
import StoreInfo from "./StoreInfo";

const StoreSidebar = () => {
  const [searchParams, setSearchParams] = useSearchParams();
  const query = searchParams.get("q") || "";

  const onChangeQuery = (value) => {
    const next = new URLSearchParams(searchParams);
    if (value.trim()) {
      next.set("q", value);
    } else {
      next.delete("q");
    }
    setSearchParams(next);
  };

  return (
    <aside className="bg-white p-4 rounded-xl h-fit sticky top-28">
      <Input placeholder="Search in store..." value={query} onChange={(e) => onChangeQuery(e.target.value)} />
      <StoreInfo />
      <StoreDepartments />
    </aside>
  );
};

export default StoreSidebar;
