import React from 'react'
import { Input } from '../ui/input'
import StoreInfo from './StoreInfo'
import StoreDepartments from './StoreDepartments'

const StoreSidebar = () => {
  return (
    <aside className="bg-white p-4 rounded-xl h-fit sticky top-28">
      <Input placeholder="Search in store..." />

      <StoreInfo />
      <StoreDepartments />
    </aside>
  )
}

export default StoreSidebar