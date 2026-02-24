
import { getStoreProducts } from '@/api/store.api';
import React, { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'

const StoreDepartments = () => {
  const { storeId } = useParams();
  const [categories, setCategories] = useState([]);

  useEffect(() => {
    getStoreProducts(storeId).then(res => {
      const cats = new Set(res.data.map(p => p.category));
      setCategories([...cats]);
    })
  }, [storeId]);
  return (
    <div className='mt-6'>
      <h4 className='font-semibold mb-3'>Departments</h4>
      <ul className='space-y-2 text-sm'>
        {categories.map(cat => (
          <li
            key={cat}
            className='cursor-pointer hover:text-blue-600'
          >
            {cat}
          </li>
        ))}
      </ul>
    </div>
  )
}

export default StoreDepartments