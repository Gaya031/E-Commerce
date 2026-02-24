import React, { useEffect, useState } from 'react'
import ProductCard from '../product/ProductCard'
import { useParams } from 'react-router-dom'
import { getStoreProducts } from '@/api/store.api';

const CategoryProducts = () => {
    const {storeId} = useParams();
    const [products, setProducts] = useState([]);
    useEffect(() => {
        getStoreProducts(storeId).then(res => setProducts(res.data))
    }, [storeId]);

    const grouped = products.reduce((acc, p) => {
        acc[p.category] = acc[p.category] || [];
        acc[p.category].push(p);
        return acc;
    }, {});
  return (
    <div className='space-y-10'>
        {Object.entries(grouped).map(([category, items]) => {
            <div key={category}>
                <h4 className='font-semibold mb-4'>{category}</h4>
                <div className='grid grid-cols04 gap-6'>
                    {items.map(p => (
                        <ProductCard key={p.id} product={p} />
                    ))}
                </div>
            </div>
        })}
    </div>
  )
}

export default CategoryProducts