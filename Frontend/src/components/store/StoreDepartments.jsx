
import { getStoreProducts } from '@/api/store.api';
import React, { useEffect, useState } from 'react'
import { useParams, useSearchParams } from 'react-router-dom'

const StoreDepartments = () => {
  const { storeId } = useParams();
  const [searchParams, setSearchParams] = useSearchParams();
  const [categories, setCategories] = useState([]);
  const selected = searchParams.get("dept") || "all";

  useEffect(() => {
    getStoreProducts(storeId).then(res => {
      const cats = new Set((res.data || []).map(p => p.category).filter(Boolean));
      setCategories(["all", ...cats]);
    })
  }, [storeId]);

  const pickCategory = (cat) => {
    const next = new URLSearchParams(searchParams);
    if (cat === "all") next.delete("dept");
    else next.set("dept", cat);
    setSearchParams(next);
  };

  return (
    <div className='mt-6'>
      <h4 className='font-semibold mb-3'>Departments</h4>
      <ul className='space-y-2 text-sm'>
        {categories.map(cat => (
          <li
            key={cat}
            className={`cursor-pointer hover:text-blue-600 ${selected === cat ? "text-blue-600 font-semibold" : ""}`}
            onClick={() => pickCategory(cat)}
          >
            {cat === "all" ? "All Departments" : cat}
          </li>
        ))}
      </ul>
    </div>
  )
}

export default StoreDepartments
