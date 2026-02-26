import { useEffect, useMemo, useState } from "react";
import { useParams, useSearchParams } from "react-router-dom";

import { getStoreProducts } from "@/api/store.api";
import BestSellers from "./BestSellers";
import CategoryProducts from "./CategoryProducts";

const StoreProducts = () => {
  const { storeId } = useParams();
  const [searchParams] = useSearchParams();
  const [products, setProducts] = useState([]);

  useEffect(() => {
    getStoreProducts(storeId).then((res) => setProducts(Array.isArray(res.data) ? res.data : []));
  }, [storeId]);

  const filteredProducts = useMemo(() => {
    const query = (searchParams.get("q") || "").trim().toLowerCase();
    const department = searchParams.get("dept");
    return products.filter((p) => {
      const okDept = !department || p.category === department;
      const okQuery =
        !query ||
        String(p.title || "").toLowerCase().includes(query) ||
        String(p.description || "").toLowerCase().includes(query);
      return okDept && okQuery;
    });
  }, [products, searchParams]);

  return (
    <div>
      <BestSellers />
      <CategoryProducts products={filteredProducts} />
    </div>
  );
};

export default StoreProducts;
