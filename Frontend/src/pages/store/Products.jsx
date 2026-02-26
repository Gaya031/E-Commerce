import StoreProducts from '@/components/store/StoreProducts'
import StoreSidebar from '@/components/store/StoreSidebar'
import React from 'react'

const Products = () => {
  return (
    <div className='grid grid-cols-1 lg:grid-cols-[220px_1fr] gap-6'>
      <StoreSidebar />
      <StoreProducts />
    </div>
  )
}

export default Products
